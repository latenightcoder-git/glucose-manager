import copy, numpy as np, torch
import torch.nn as nn, torch.optim as optim

class MLP(nn.Module):
    def __init__(self, in_dim, out_dim, hidden=(256,256), out_act=nn.Identity):
        super().__init__()
        layers = []; last = in_dim
        for h in hidden:
            layers += [nn.Linear(last, h), nn.ReLU()]; last = h
        layers += [nn.Linear(last, out_dim), out_act()]
        self.net = nn.Sequential(*layers)
    def forward(self, x): return self.net(x)

class DDPGAgent:
    def __init__(self, obs_dim, act_dim, act_low, act_high, actor_lr=1e-3, critic_lr=1e-3, gamma=0.99, tau=0.005, device="cpu"):
        self.device = torch.device(device)
        self.gamma, self.tau = gamma, tau
        self.act_low = torch.tensor(act_low, device=self.device, dtype=torch.float32)
        self.act_high = torch.tensor(act_high, device=self.device, dtype=torch.float32)
        self.actor = MLP(obs_dim, act_dim, out_act=nn.Tanh).to(self.device)
        self.critic = MLP(obs_dim + act_dim, 1).to(self.device)
        self.target_actor = copy.deepcopy(self.actor).to(self.device)
        self.target_critic = copy.deepcopy(self.critic).to(self.device)
        self.pi_opt = optim.Adam(self.actor.parameters(), lr=actor_lr)
        self.q_opt = optim.Adam(self.critic.parameters(), lr=critic_lr)

    def select_action(self, obs, noise_std=0.1, deterministic=False):
        self.actor.eval()
        with torch.no_grad():
            o = torch.as_tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            a = self.actor(o)
            a = (a + 1) * 0.5 * (self.act_high - self.act_low) + self.act_low
            if not deterministic and noise_std > 0:
                a = a + torch.normal(0, noise_std, size=a.shape, device=self.device)
            a = torch.clamp(a, self.act_low, self.act_high)
        self.actor.train()
        return a.squeeze(0).cpu().numpy()

    def train_step(self, batch):
        obs = torch.as_tensor(batch["obs"], dtype=torch.float32, device=self.device)
        act = torch.as_tensor(batch["act"], dtype=torch.float32, device=self.device)
        rew = torch.as_tensor(batch["rew"], dtype=torch.float32, device=self.device).unsqueeze(-1)
        next_obs = torch.as_tensor(batch["next_obs"], dtype=torch.float32, device=self.device)
        done = torch.as_tensor(batch["done"], dtype=torch.float32, device=self.device).unsqueeze(-1)
        with torch.no_grad():
            na = self.target_actor(next_obs)
            na = (na + 1) * 0.5 * (self.act_high - self.act_low) + self.act_low
            q_targ = self.target_critic(torch.cat([next_obs, na], dim=-1))
            y = rew + self.gamma * (1 - done) * q_targ
        q = self.critic(torch.cat([obs, act], dim=-1))
        q_loss = nn.functional.mse_loss(q, y)
        self.q_opt.zero_grad(); q_loss.backward(); self.q_opt.step()
        a = self.actor(obs)
        a = (a + 1) * 0.5 * (self.act_high - self.act_low) + self.act_low
        pi_loss = -self.critic(torch.cat([obs, a], dim=-1)).mean()
        self.pi_opt.zero_grad(); pi_loss.backward(); self.pi_opt.step()
        with torch.no_grad():
            for p, tp in zip(self.actor.parameters(), self.target_actor.parameters()):
                tp.data.mul_(1 - self.tau).add_(self.tau * p.data)
            for p, tp in zip(self.critic.parameters(), self.target_critic.parameters()):
                tp.data.mul_(1 - self.tau).add_(self.tau * p.data)

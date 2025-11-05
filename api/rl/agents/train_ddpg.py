import gymnasium as gym
import numpy as np
from collections import deque
from envs.glucose_env import GlucoseEnv  # or switch to PatientEnv
from agents.ddpg import DDPGAgent

class Replay:
    def __init__(self, cap=300000):
        self.buf = deque(maxlen=cap)
    def add(self, o,a,r,no,d): self.buf.append((o,a,r,no,d))
    def sample(self, bs):
        idx = np.random.randint(0, len(self.buf), size=bs)
        o,a,r,no,d = zip(*[self.buf[i] for i in idx])
        return {
            "obs": np.array(o, np.float32),
            "act": np.array(a, np.float32),
            "rew": np.array(r, np.float32),
            "next_obs": np.array(no, np.float32),
            "done": np.array(d, np.float32),
        }

def train(env_name="glucose", seed=0, steps=200_000, start_steps=2_000, batch_size=256, eval_every=10_000, use_patient=False, sensitivity=1.0):
    # Select environment
    if use_patient:
        from envs.patient_env import PatientEnv
        env = PatientEnv(sensitivity=sensitivity, seed=seed)
    else:
        env = GlucoseEnv(seed=seed)

    obs, _ = env.reset(seed=seed)
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]

    agent = DDPGAgent(
        obs_dim=obs_dim,
        act_dim=act_dim,
        act_low=env.action_space.low,
        act_high=env.action_space.high,
    )
    rb = Replay(300000)

    ep_ret, ep_len = 0.0, 0
    total_steps = 0
    while total_steps < steps:
        if total_steps < start_steps:
            action = env.action_space.sample()
        else:
            action = agent.select_action(obs, noise_std=0.2)

        next_obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        rb.add(obs, action, reward, next_obs, float(done))

        obs = next_obs
        ep_ret += reward
        ep_len += 1
        total_steps += 1

        if done:
            obs, _ = env.reset()
            ep_ret, ep_len = 0.0, 0

        if len(rb.buf) >= batch_size:
            batch = rb.sample(batch_size)
            agent.train_step(batch)

        if total_steps % eval_every == 0:
            print(f"[eval] steps={total_steps}")

    return agent

if __name__ == "__main__":
    train()

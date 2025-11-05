from fastapi import APIRouter, Depends
import threading
from auth import get_current_role
from routers.recommend import MODEL

router = APIRouter(prefix="/api", tags=["train"])

@router.post("/train")
def trigger_train(steps: int = 50000, role: str = Depends(get_current_role)):
    def runner():
        from rl.envs.glucose_env import GlucoseEnv
        from rl.agents.ddpg import DDPGAgent
        import numpy as np
        env = GlucoseEnv(seed=0)
        obs, _ = env.reset()
        agent = DDPGAgent(obs_dim=env.observation_space.shape[0],
                            act_dim=env.action_space.shape[0],
                            act_low=env.action_space.low,
                            act_high=env.action_space.high)
        from collections import deque
        rb = deque(maxlen=200000)
        for t in range(steps):
            a = env.action_space.sample() if t < 1000 else agent.select_action(obs)
            no, r, term, trunc, _ = env.step(a)
            rb.append((obs,a,r,no,float(term or trunc)))
            obs = no
            if term or trunc: obs, _ = env.reset()
            if len(rb) >= 512:
                idx = np.random.randint(0, len(rb), size=256)
                batch = {"obs": np.array([rb[i][0] for i in idx], np.float32),
                            "act": np.array([rb[i][1] for i in idx], np.float32),
                            "rew": np.array([rb[i][2] for i in idx], np.float32),
                            "next_obs": np.array([rb[i][3] for i in idx], np.float32),
                            "done": np.array([rb[i][4] for i in idx], np.float32)}
                agent.train_step(batch)
        MODEL["agent"] = agent
    threading.Thread(target=runner, daemon=True).start()
    return {"started": True}

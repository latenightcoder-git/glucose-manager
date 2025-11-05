import gymnasium as gym
import numpy as np
from gymnasium import spaces

class GlucoseEnv(gym.Env):
    metadata = {"render_modes": []}
    def __init__(self, seed: int | None = None):
        super().__init__()
        self.rng = np.random.default_rng(seed)
        low = np.array([40.0, 0.0, 0.0, 0.0], dtype=np.float32)
        high = np.array([500.0, 20.0, 200.0, 1.0], dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        self.action_space = spaces.Box(low=np.array([0.0], dtype=np.float32),
                                       high=np.array([10.0], dtype=np.float32), dtype=np.float32)
        self.state = None; self.t = 0

    def reset(self, *, seed: int | None = None, options=None):
        super().reset(seed=seed)
        self.t = 0
        glucose = self.rng.normal(150, 20)
        self.state = np.array([glucose, 0.0, 0.0, 0.0], dtype=np.float32)
        return self.state, {}

    def step(self, action: np.ndarray):
        insulin = float(np.clip(action[0], self.action_space.low[0], self.action_space.high[0]))
        glucose, iob, carbs, activity = self.state
        d_glucose = -insulin * 12.0 + carbs * 3.0 - activity * 8.0 + np.random.normal(0, 3.0)
        glucose_next = np.clip(glucose + d_glucose, 40, 500)
        iob_next = np.clip(iob * 0.8 + insulin, 0, 20)
        carbs_next = max(0.0, carbs - 10.0)
        activity_next = max(0.0, activity - 0.1)
        self.state = np.array([glucose_next, iob_next, carbs_next, activity_next], dtype=np.float32)
        self.t += 1
        target_low, target_high = 90.0, 140.0
        if glucose_next < target_low:
            band_penalty = -2.0 * (target_low - glucose_next)
        elif glucose_next > target_high:
            band_penalty = -1.0 * (glucose_next - target_high)
        else:
            band_penalty = 0.0
        reward = float(band_penalty - 0.05 * insulin)
        terminated = False
        truncated = self.t >= 288
        info = {"glucose": float(glucose_next), "insulin": insulin}
        return self.state, reward, terminated, truncated, info

    def set_meal_and_activity(self, carbs_g: float, activity_level: float):
        g, iob, _, _ = self.state
        self.state = np.array([g, iob, float(carbs_g), float(activity_level)], dtype=np.float32)

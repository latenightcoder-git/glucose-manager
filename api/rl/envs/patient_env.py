import gymnasium as gym
import numpy as np
from gymnasium import spaces

class PatientEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, sensitivity: float = 1.0, seed: int | None = None):
        super().__init__()
        self.rng = np.random.default_rng(seed)
        self.sensitivity = float(sensitivity)
        # Observation: [glucose, insulin_on_board, carbs, activity, sensitivity]
        low = np.array([40.0, 0.0, 0.0, 0.0, 0.3], dtype=np.float32)
        high = np.array([500.0, 20.0, 300.0, 1.0, 2.0], dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        # Action: insulin units (continuous)
        self.action_space = spaces.Box(low=np.array([0.0], dtype=np.float32),
                                       high=np.array([15.0], dtype=np.float32),
                                       dtype=np.float32)
        self.state = None
        self.t = 0

    def reset(self, *, seed: int | None = None, options=None):
        super().reset(seed=seed)
        self.t = 0
        glucose = float(self.rng.normal(160, 25))
        iob = 0.0
        carbs = 0.0
        activity = 0.0
        self.state = np.array([glucose, iob, carbs, activity, self.sensitivity], dtype=np.float32)
        return self.state, {}

    def step(self, action: np.ndarray):
        insulin = float(np.clip(action[0], self.action_space.low[0], self.action_space.high[0]))
        glucose, iob, carbs, activity, sens = self.state

        # Simplified glucose dynamics for simulation
        d_glucose = -insulin * 10.0 * sens + carbs * 3.0 - activity * 10.0 + self.rng.normal(0, 4.0)
        glucose_next = float(np.clip(glucose + d_glucose, 40, 500))
        iob_next = float(np.clip(iob * 0.85 + insulin, 0, 20))
        carbs_next = float(max(0.0, carbs - 12.0))
        activity_next = float(max(0.0, activity - 0.1))

        self.state = np.array([glucose_next, iob_next, carbs_next, activity_next, sens], dtype=np.float32)
        self.t += 1

        # Reward closer to target is better; light penalty for insulin usage
        target = 110.0
        reward = -abs(glucose_next - target) - 0.02 * insulin

        terminated = False
        truncated = self.t >= 288  # e.g., one day at 5-min steps
        info = {"glucose": glucose_next, "insulin": insulin}
        return self.state, float(reward), terminated, truncated, info

    def set_meal_and_activity(self, carbs_g: float, activity_level: float):
        g, iob, _, _, sens = self.state
        self.state = np.array([g, iob, float(carbs_g), float(activity_level), sens], dtype=np.float32)

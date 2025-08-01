from __future__ import annotations

from typing import Literal

import gymnasium as gym
import humanoid_bench  # noqa: F401
import numpy as np
from gymnasium import spaces


class HumanoidBenchEnv(gym.Env):
    def __init__(self, env_id: str, seed: int, image_size: tuple[int, int], obs_type: Literal["rgb", "proprio"]):
        self.env = gym.make(env_id, render_mode="rgb_array", width=image_size[0], height=image_size[1])
        self._obs_type = obs_type
        if obs_type == "rgb":
            self._obs_space = spaces.Box(low=-0.5, high=0.5, shape=(3, image_size[0], image_size[1]), dtype=np.float32)
        elif obs_type == "proprio":
            self._obs_space = self.env.observation_space
        self._action_space = self.env.action_space
        self._obs_space.seed(seed)
        self._action_space.seed(seed)

    def _get_rgb(self):
        obs = self.env.render()
        obs = np.transpose(obs, (2, 0, 1)).copy() / 255.0 - 0.5  # (H, W, 3) -> (3, H, W)
        return obs

    def reset(self) -> tuple[np.ndarray, dict]:
        obs, _ = self.env.reset()
        if self._obs_type == "rgb":
            obs = self._get_rgb()
        return obs, {}

    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, bool, dict]:
        obs, reward, terminated, truncated, info = self.env.step(action)
        if self._obs_type == "rgb":
            obs = self._get_rgb()
        return obs, reward, terminated, truncated, info

    def render(self) -> np.ndarray:
        return self.env.render()

    def close(self) -> None:
        self.env.close()

    @property
    def observation_space(self):
        return self._obs_space

    @property
    def action_space(self):
        return self._action_space

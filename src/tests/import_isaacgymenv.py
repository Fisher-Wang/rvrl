import isaacgym
import rootutils
import torch

rootutils.setup_root(__file__, pythonpath=True)
from src.envs.isaacgym_env import IsaacGymEnv

env = IsaacGymEnv(task_name="Cartpole", num_envs=1, seed=0, device="cuda")
print(env.envs)

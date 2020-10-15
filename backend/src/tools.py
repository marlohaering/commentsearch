import numpy as np

def unit_normalize(vec: np.ndarray) -> np.ndarray:
    return vec / np.linalg.norm(vec)
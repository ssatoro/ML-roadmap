import numpy as np


scores = np.array([95, 82, 67, 50, 73, 40])
print(scores[np.logical_and(scores >= 60, scores <= 90)])

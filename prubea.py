import numpy as np
from models.individualModel import Individual
a= Individual(np.random.randint(0,2,(5, 10))[0])


print(a, type(a))

import random

_RANDOM_SEED = 1234
random.seed(_RANDOM_SEED)

_INTEGER_NAMES = [str(i) for i in range(100)]


def create_name_dict(name, nnodes = 100):
  
  if name == "integer":
    names_list = _INTEGER_NAMES
  else:
    raise ValueError(f"Unknown approach: {name}")
  name_dict = {}
  for ind, value in enumerate(names_list):
    name_dict[ind] = value
  return name_dict

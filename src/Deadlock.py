import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from collections import deque
from .PetriNet import PetriNet
import numpy as np

def deadlock_reachable_marking(
    pn: PetriNet, 
    bdd: BinaryDecisionDiagram, 
) -> Optional[List[int]]:
    if hasattr(bdd, "is_zero") and bdd.is_zero():
        return None
    I = np.array(pn.I, dtype=int)
    O = np.array(pn.O, dtype=int)
    n_trans, n_places = I.shape
    if hasattr(pn, "place_names"):
        place_names = list(pn.place_names)
        if len(place_names) != n_places:
            place_names = [f"p{i+1}" for i in range(n_places)]
    else:
        place_names = [f"p{i+1}" for i in range(n_places)]
    place_index = {str(name): i for i, name in enumerate(place_names)}
    def is_fireable(M: np.ndarray, t_index: int) -> bool:
        pre = I[t_index, :]
        post = O[t_index, :]
        if any(M < pre):
            return False
        M_new = M - pre + post
        if any(M_new > 1):
            return False
        return True
    for point in bdd.satisfy_all():
        M = np.zeros(n_places, int)
        for var_obj, val in point.items():
            name = str(var_obj)
            idx = place_index.get(name)
            if idx is not None:
                M[idx] = int(val)
        any_fireable  = False
        for i in range(n_trans):
            if(is_fireable(M, i)):
                any_fireable = True
                break
        if not any_fireable:
            return M.tolist()
    return None
    pass
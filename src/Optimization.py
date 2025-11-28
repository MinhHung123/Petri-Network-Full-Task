import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from collections import deque
import numpy as np

def max_reachable_marking(
    place_ids: List[str], 
    bdd: BinaryDecisionDiagram, 
    c: np.ndarray
) -> Tuple[Optional[List[int]], Optional[int]]:
    n = len(place_ids)
    if n==0:
        return [], 0
    name_to_idx = {name: i for i, name in enumerate(place_ids)}
    if hasattr(bdd, "is_zero") and bdd.is_zero():
        return None, None
    if hasattr(bdd, "is_one") and bdd.is_one():
        best_marking = [1 if c[i] >= 0 else 0 for i in range(n)]
        best_value = int(np.dot(best_marking, c))
        return best_marking, best_value
    best_marking: Optional[List[int]] = None
    best_value: Optional[int] = None
    try:
        assignments = bdd.satisfy_all()
    except AttributeError:
        assignments = bdd.to_expr().satisfy_all()
    for point in assignments:
        marking = [0] * n
        assigned_indices = set()
        for var_obj, val in point.items():
            name = str(var_obj)
            idx = name_to_idx.get(name)
            if idx is not None:
                marking[idx] = int(val)
                assigned_indices.add(idx)
        for i in range(n):
            if i not in assigned_indices:
                marking[i] = 1 if c[i] >= 0 else 0
        value = int(np.dot(marking, c))
        if best_value is None or value > best_value:
            best_value = value
            best_marking = marking
    if best_marking is None:
        return None, None
    return best_marking, best_value
    pass
import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from .PetriNet import PetriNet
from collections import deque
import numpy as np

def bdd_reachable(pn: PetriNet) -> Tuple[BinaryDecisionDiagram, int]:
    I = pn.I
    O = pn.O
    M0 = pn.M0
    num_transitions = I.shape[0]
    visited: Set[Tuple[int, ...]] = set()
    start = tuple(M0.tolist())
    visited.add(start)
    q = deque([M0.copy()])
    while q:
        M = q.popleft()
        for i in range(num_transitions):
            pre = I[i, :]
            post = O[i, :]
            if(np.all(M >= pre)):
                M_new = M - pre + post
                if any(M_new > 1):
                    continue
                M_new_tuple = tuple(M_new.tolist())
                if M_new_tuple not in visited:
                    visited.add(M_new_tuple)
                    q.append(M_new)
    n_places = len(M0)
    place_names = None
    for attr in  ["P", "places", "place_names"]:
        if hasattr(pn, attr):
            place_names = list(getattr(pn, attr))
            break
    if place_names is None or len(place_names) != n_places:
        place_names = [f"p{i+1}" for i in range(n_places)]
    vars_expr = [exprvar(name) for name in place_names]
    total_expr = None
    for e_reachable in visited:
        term = vars_expr[0] if e_reachable[0] else ~vars_expr[0]
        for i in range(1, n_places):
            term &= vars_expr[i] if e_reachable[i] else ~vars_expr[i]
        total_expr = term if total_expr is None else (total_expr | term)
    bdd = expr2bdd(total_expr)
    count = bdd.satisfy_count()
    return bdd, count
    pass
from collections import deque
import numpy as np
from .PetriNet import PetriNet
from typing import Set, Tuple

def bfs_reachable(pn: PetriNet) -> Set[Tuple[int, ...]]:
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
    return visited
    pass    
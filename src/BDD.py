import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from .PetriNet import PetriNet
from collections import deque
import numpy as np

def build_bdd(pn: PetriNet) -> Tuple[BinaryDecisionDiagram, int]:
    # Ma trận tiền điều kiện (input) và hậu điều kiện (output) của Petri net
    I = pn.I
    O = pn.O
    M0 = pn.M0
    # Số lượng transition
    num_transitions = I.shape[0]
    # visited chứa các Marking reachable
    visited: Set[Tuple[int, ...]] = set()
    start = tuple(M0.tolist())
    visited.add(start)
    # Hàng đợi queue để chứa các reachable marking
    q = deque([M0.copy()])
    while q:
        M = q.popleft()
        # Thử bắn từng transition
        for i in range(num_transitions):
            pre = I[i, :]
            post = O[i, :]
            # Kiểm tra xem transition i có bắn được từ marking M không
            # (M phải có đủ token ở tất cả các place theo pre)
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
    # Lấy tên các place từ thuộc tính của pn 
    for attr in  ["P", "places", "place_names"]:
        if hasattr(pn, attr):
            place_names = list(getattr(pn, attr))
            break
     # Nếu không có tên place, hoặc số lượng không khớp, tự sinh tên p1, p2, ...
    if place_names is None or len(place_names) != n_places:
        place_names = [f"p{i+1}" for i in range(n_places)]
    # total_expr là biểu thức logic biểu diễn tập tất cả các marking reachable
    vars_expr = [exprvar(name) for name in place_names]
    total_expr = None
    # Với mỗi marking reachable, tạo ra một "minterm" tương ứng
    # Ví dụ: M = (1, 0, 1) -> p1 & ~p2 & p3
    for e_reachable in visited:
        # Bắt đầu từ place đầu tiên
        term = vars_expr[0] if e_reachable[0] else ~vars_expr[0]
        for i in range(1, n_places):
            term &= vars_expr[i] if e_reachable[i] else ~vars_expr[i]
        total_expr = term if total_expr is None else (total_expr | term)
    # Chuyển biểu thức Boolean thành BDD
    bdd = expr2bdd(total_expr)
    # Đếm số lượng các biểu thức sinh ra 
    count = bdd.satisfy_count()
    return bdd, count
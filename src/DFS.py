from collections import deque
import numpy as np
from .PetriNet import PetriNet
from typing import Set, Tuple

def dfs_reachable(pn: PetriNet) -> Set[Tuple[int, ...]]:
    # Ma trận tiền điều kiện (input) và hậu điều kiện (output) của Petri net
    I = pn.I
    O = pn.O
    M0 = pn.M0
    
    # Số lượng transition
    num_transition = I.shape[0]
    
    # visited để chứa các reachable marking
    visited: Set[Tuple[int, ...]] = set()
    start = tuple(M0.tolist())
    visited.add(start)
    
    # Ngăn xếp để duyệt các trạng thái có thể có
    stack = [M0.copy()]
    
    # Duyệt DFS các reachable marking
    while(stack):
        # Lấy phần từ ở đầu stack
        M = stack.pop()
        
        # Bắn các transition
        for i in range(num_transition):
            # pre và post lần lượt là các hàng thứ i của I và O tương ứng với một transition
            pre = I[i, :]
            post = O[i, :]
            
            # Xét xem có thỏa mãn điều kiện là reachable marking không
            if np.all(M >= pre):
                M_new = M - pre + post
                # Vì là 1-safe nên phần tử lớn hơn 1 thì loại
                if np.any(M_new > 1):
                    continue
                M_new_tuple = tuple(M_new.tolist())
                # Nếu reachable marking chưa được thăm thì thêm vào visited
                if M_new_tuple not in visited:
                    visited.add(M_new_tuple)
                    stack.append(M_new)
    return visited
    pass
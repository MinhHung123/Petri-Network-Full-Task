import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from collections import deque
from .PetriNet import PetriNet
import numpy as np

def deadlock_detection(
    pn: PetriNet, 
    bdd: BinaryDecisionDiagram, 
) -> Optional[List[int]]:
    # Nếu BDD rỗng (không có trạng thái reachable nào) thì không thể có deadlock
    if hasattr(bdd, "is_zero") and bdd.is_zero():
        return None
    
    # Ma trận input (I) và output (O) của Petri net
    I = np.array(pn.I, dtype=int)
    O = np.array(pn.O, dtype=int)
    
    # n_trans và place lần lượt là số lượng transition và places
    n_trans, n_places = I.shape
    
    # Lấy tên các place nếu có; nếu không thì tự sinh p1, p2, ...
    if hasattr(pn, "place_names"):
        place_names = list(pn.place_names)
        if len(place_names) != n_places:
            place_names = [f"p{i+1}" for i in range(n_places)]
    else:
        place_names = [f"p{i+1}" for i in range(n_places)]
    place_index = {str(name): i for i, name in enumerate(place_names)}
    
    # Hàm kiểm tra transition t_index có bắn được từ marking M hay không
    def is_fireable(M: np.ndarray, t_index: int) -> bool:
        # pre và post là các hàng của ma trận I và O tương ứng với mỗi hàng là transitioin
        pre = I[t_index, :]
        post = O[t_index, :]
        # Nếu M không đủ token so với pre thì không bắn được
        if any(M < pre):
            return False
        # Tính marking mới
        M_new = M - pre + post
        # Ràng buộc: không cho phép place nào có > 1 token (1-safe)
        if any(M_new > 1):
            return False
        return True
    
    # Duyệt qua TẤT CẢ các biểu thức thỏa BDD (tức là tất cả marking reachable)
    for point in bdd.satisfy_all():
        # M là reachable marking hiện tại
        M = np.zeros(n_places, int)
        
        # Duyệt qua reachable marking, name là tên place, val là số token của place
        for var_obj, val in point.items():
            name = str(var_obj)
            idx = place_index.get(name)
            if idx is not None:
                M[idx] = int(val)
                
        # Kiểm tra xem tại marking M có transition nào bắn được không
        any_fireable  = False
        for i in range(n_trans):
            if(is_fireable(M, i)):
                any_fireable = True
                break

        # Nếu không có transition nào bắn được -> đây là deadlock marking
        if not any_fireable:
            return M.tolist()
    return None
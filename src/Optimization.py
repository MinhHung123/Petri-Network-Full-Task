import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from collections import deque
import numpy as np

def Optimize_max_reachable_marking(
    place_ids: List[str], 
    bdd: BinaryDecisionDiagram, 
    c: np.ndarray
) -> Tuple[Optional[List[int]], Optional[int]]:
    # Số lượng các place
    n = len(place_ids)
    
    # Nếu không có place nào, trả về marking rỗng và giá trị 0
    if n==0:
        return [], 0
    
    #  Tạo bản đồ từ tên place → vị trí (index) trong mảng đó.
    name_to_idx = {name: i for i, name in enumerate(place_ids)}
    
    # Nếu BDD là 0 (rỗng, không có assignment nào thỏa), không có marking hợp lệ
    if hasattr(bdd, "is_zero") and bdd.is_zero():
        return None, None
    
    # Nếu BDD là 1 (tất cả assignment đều thỏa),
    # thì các biến không bị ràng buộc – ta chọn marking tối ưu trực tiếp từ c
    if hasattr(bdd, "is_one") and bdd.is_one():
        # Với từng place i:
        # - nếu c[i] >= 0 thì chọn 1 để tăng giá trị
        # - nếu c[i] < 0  thì chọn 0 để tránh bị trừ
        best_marking = [1 if c[i] >= 0 else 0 for i in range(n)]
        best_value = int(np.dot(best_marking, c))
        return best_marking, best_value
    
    # Khởi tạo best_marking để lưu reachable marking đạt giá trị max
    # khởi tạo best_value để lưu giá trị max
    best_marking: Optional[List[int]] = None
    best_value: Optional[int] = None
    
    # Gán assignments là tất cả các biểu thức của BDD
    try:
        assignments = bdd.satisfy_all()
    except AttributeError:
        assignments = bdd.to_expr().satisfy_all()
        
    # Mỗi phần tử trong assignments là một dict: { biến -> True/False }  
    # Duyệt qua từng biểu thức của BDD  
    for point in assignments:
        # khởi tạo marking 
        marking = [0] * n
        assigned_indices = set()
        
        # Gán các biến đã được BDD chỉ định trong point
        # Duyệt qua reachable marking, name là tên place, val là số token của place
        for var_obj, val in point.items():
            name = str(var_obj)
            idx = name_to_idx.get(name)
            if idx is not None:
                marking[idx] = int(val)
                assigned_indices.add(idx)
                
        # Với các place không xuất hiện trong assignment (không bị BDD ràng buộc),
        # ta được quyền chọn 0 hoặc 1 sao cho tối ưu giá trị c^T * marking:
        # - nếu c[i] >= 0 -> chọn 1
        # - nếu c[i] < 0  -> chọn 0
        for i in range(n):
            if i not in assigned_indices:
                marking[i] = 1 if c[i] >= 0 else 0
        value = int(np.dot(marking, c))
        
        # Cập nhật giá trị lớn nhất
        if best_value is None or value > best_value:
            best_value = value
            best_marking = marking
            
    # Nếu không tìm được marking nào (trường hợp BDD rỗng sau khi lặp),
    # trả về None, None
    if best_marking is None:
        return None, None
    
    return best_marking, best_value
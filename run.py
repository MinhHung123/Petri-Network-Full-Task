# # from src.PetriNet import PetriNet
# # from src.BDD import build_bdd
# # from src.Optimization import Optimize_max_reachable_marking
# # from src.BFS import bfs_reachable
# # from src.DFS import dfs_reachable
# # from src.Deadlock import deadlock_detection
# # from pyeda.inter import * 
# # import numpy as np
# # import pm4py
# # # from graphviz import Source
# # from pm4py.objects.petri_net.importer import importer as pnml_importer
# # from pm4py.visualization.petri_net import visualizer as pn_vis


# # # ---------------------- CẤU HÌNH HỆ SỐ c ----------------------
# # # Nhớ đảm bảo chiều dài c khớp với số place trong Petri net
# # c = np.array([1, -2, 3, -1, 1, 2])


# # # ---------------------- CÁC HÀM CHO TỪNG TASK ----------------------
# # def task_print_pn(pn):
# #     print("\n--- Thông tin Petri Net ---")
# #     print(pn)


# # def task_bfs(pn):
# #     print("\n--- BFS Reachable Markings ---")
# #     bfs_set = bfs_reachable(pn)
# #     for m in bfs_set:
# #         print(np.array(m))
# #     print("Total BFS reachable =", len(bfs_set))


# # def task_dfs(pn):
# #     print("\n--- DFS Reachable Markings ---")
# #     dfs_set = dfs_reachable(pn)
# #     for m in dfs_set:
# #         print(np.array(m))
# #     print("Total DFS reachable =", len(dfs_set))


# # def task_bdd(pn):
# #     print("\n--- BDD Reachable ---")
# #     bdd, count = build_bdd(pn)
# #     sats = list(bdd.satisfy_all())
# #     print("Satisfying all:", sats)
# #     expr = bdd2expr(bdd)
# #     if not bdd.inputs or len(sats) == 0:
# #         print("Minimized = (biểu thức hằng, không cần tối thiểu hóa):", expr)
# #     else:
# #         print("Minimized =", espresso_exprs(expr))

# #     print("BDD reachable markings =", count)
# #     return bdd, count


# # def task_deadlock(pn, cached_bdd=None):
# #     print("\n--- Deadlock reachable marking ---")
# #     if cached_bdd is None:
# #         bdd, _ = build_bdd(pn)
# #     else:
# #         bdd = cached_bdd

# #     dead = deadlock_detection(pn, bdd)
# #     if dead is not None:
# #         print("Deadlock marking:", dead)
# #     else:
# #         print("No deadlock reachable.")


# # def task_optimize(pn, cached_bdd=None):
# #     print("\n--- Optimize c·M ---")

# #     if cached_bdd is None:
# #         bdd, _ = build_bdd(pn)
# #     else:
# #         bdd = cached_bdd

# #     max_mark, max_val = Optimize_max_reachable_marking(
# #         pn.place_names, bdd, c
# #     )
# #     print("c:", c)
# #     print("Max marking:", max_mark)
# #     print("Max value:", max_val)


# # def task_draw_pnml(filename):
# #     print("\n=== DRAWING PETRI NET WITH PM4PY – Task 3 ===")
# #     try:
# #         pnml_path = filename  # dùng lại file PNML ở trên

# #         # pm4py đọc PNML
# #         pn_net, im, fm = pnml_importer.apply(pnml_path)

# #         # Tạo graph
# #         gviz = pn_vis.apply(pn_net, im, fm)

# #         # Lưu ra file ảnh
# #         output_img = "petri_net.png"
# #         pn_vis.save(gviz, output_img)
# #         print(f"Petri net image saved to: {output_img}")

# #         # KHÔNG auto mở nữa cho đỡ lỗi
# #         # pn_vis.view(gviz)

# #     except Exception as e:
# #         print("Không thể vẽ Petri net bằng pm4py. Chi tiết lỗi:")
# #         print(e)


# # # --------- HÀM CHẠY TẤT CẢ CÁC TASK THEO THỨ TỰ ---------
# # def task_run_all(pn, filename):
# #     """
# #     Chạy lần lượt:
# #     1. In PN
# #     2. BFS
# #     3. DFS
# #     4. BDD
# #     5. Deadlock (dùng BDD)
# #     6. Optimize (dùng BDD)
# #     7. Vẽ Petri net bằng PM4PY
# #     """
# #     print("\n========== RUN ALL TASKS ==========")

# #     task_print_pn(pn)
# #     task_bfs(pn)
# #     task_dfs(pn)

# #     bdd, count = task_bdd(pn)

# #     task_deadlock(pn, bdd)
# #     task_optimize(pn, bdd)

# #     task_draw_pnml(filename)

# #     print("\n========== DONE ALL TASKS ==========")
# #     # trả về BDD để main có thể cache nếu muốn
# #     return bdd, count


# # # ---------------------- HÀM MAIN VỚI MENU TASK ----------------------
# # def main():
# #     # 1. Load Petri Net từ file PNML
# #     #filename = input("Nhập tên file PNML (vd: Input.pnml): ").strip()
# #     filename = "test_PNML/Input.pnml"
# #     print("Loading PNML:", filename)

# #     pn = PetriNet.build_pnml(filename)
# #     print("\n--- Petri Net Loaded ---")

# #     # cache BDD để các task dùng chung (đỡ build nhiều lần)
# #     cached_bdd = None
# #     cached_bdd_count = None

# #     while True:
# #         print("\n================= MENU CHỌN TASK =================")
# #         print("1. In thông tin Petri Net")
# #         print("2. BFS reachable")
# #         print("3. DFS reachable")
# #         print("4. BDD reachable")
# #         print("5. Deadlock detection (dùng BDD)")
# #         print("6. Tối ưu hóa c·M (dùng BDD)")
# #         print("7. Vẽ Petri Net bằng PM4PY")
# #         print("8. Chạy TẤT CẢ các task (1→7)")
# #         print("0. Thoát")
# #         print("=================================================")

# #         choice = input("Chọn task: ").strip()

# #         if choice == "1":
# #             task_print_pn(pn)

# #         elif choice == "2":
# #             task_bfs(pn)

# #         elif choice == "3":
# #             task_dfs(pn)

# #         elif choice == "4":
# #             # xây BDD và cache lại
# #             cached_bdd, cached_bdd_count = task_bdd(pn)

# #         elif choice == "5":
# #             # nếu chưa có BDD thì build trước
# #             if cached_bdd is None:
# #                 cached_bdd, cached_bdd_count = build_bdd(pn)
# #             task_deadlock(pn, cached_bdd)

# #         elif choice == "6":
# #             # nếu chưa có BDD thì build trước
# #             if cached_bdd is None:
# #                 cached_bdd, cached_bdd_count = build_bdd(pn)
# #             task_optimize(pn, cached_bdd)

# #         elif choice == "7":
# #             task_draw_pnml(filename)

# #         elif choice == "8":
# #             # chạy hết, đồng thời update cache BDD
# #             cached_bdd, cached_bdd_count = task_run_all(pn, filename)

# #         elif choice == "0":
# #             print("Kết thúc chương trình.")
# #             break

# #         else:
# #             print("Lựa chọn không hợp lệ, vui lòng nhập lại.")


# # if __name__ == "__main__":
# #     main()

# from src.PetriNet import PetriNet
# from src.BDD import build_bdd
# from src.Optimization import Optimize_max_reachable_marking
# from src.BFS import bfs_reachable
# from src.DFS import dfs_reachable
# from src.Deadlock import deadlock_detection
# from pyeda.inter import * 
# import numpy as np
# import pm4py
# # from graphviz import Source
# from pm4py.objects.petri_net.importer import importer as pnml_importer
# from pm4py.visualization.petri_net import visualizer as pn_vis

# def main():
#     # ------------------------------------------------------
#     # 1. Load Petri Net từ file PNML
#     # ------------------------------------------------------
#     #filename = "Input.pnml"   # đổi file tại đây
    
#     filename = input("Nhập tên file: ").strip()
#     # filename = "ShareMemory_v2.pnml"
#     # filename = "philo.pnml"
#     print("Loading PNML:", filename)

#     pn = PetriNet.build_pnml(filename)
#     print("\n--- Petri Net Loaded ---")
#     print(pn)

#     # ------------------------------------------------------
#     # 2. BFS reachable
#     # ------------------------------------------------------
#     print("\n--- BFS Reachable Markings ---")
#     bfs_set = bfs_reachable(pn)
#     for m in bfs_set:
#         print(np.array(m))
#     print("Total BFS reachable =", len(bfs_set))

#     # ------------------------------------------------------
#     # 3. DFS reachable
#     # ------------------------------------------------------
#     print("\n--- DFS Reachable Markings ---")
#     dfs_set = dfs_reachable(pn)
#     for m in dfs_set:
#         print(np.array(m))
#     print("Total DFS reachable =", len(dfs_set))

#     # ------------------------------------------------------
#     # 4. BDD reachable
#     # ------------------------------------------------------
#     print("\n--- BDD Reachable ---")
#     bdd, count = build_bdd(pn)
#     sats = list(bdd.satisfy_all())
#     print("Satisfying all:", sats)
#     expr = bdd2expr(bdd)
#     # Nếu BDD không có biến đầu vào hoặc không có nghiệm thì KHÔNG gọi espresso_exprs
#     if not bdd.inputs or len(sats) == 0:
#         print("Minimized = (biểu thức hằng, không cần tối thiểu hóa):", expr)
#     else:
#         print("Minimized =", espresso_exprs(expr))
#     print("BDD reachable markings =", count)
#     ## Source(bdd.to_dot()).render("bdd", format="png", cleanup=True)

#     # ------------------------------------------------------
#     # 5. Deadlock detection
#     # ------------------------------------------------------
#     print("\n--- Deadlock reachable marking ---")
#     dead = deadlock_detection(pn, bdd)
#     if dead is not None:
#         print("Deadlock marking:", dead)
#     else:
#         print("No deadlock reachable.")

#     # ------------------------------------------------------
#     # 6. Optimization: maximize c·M
#     # ------------------------------------------------------
#     c = np.array([1, -2, 3, -1, 1, 2])
#     # c = np.array([
#     #  1, -2,  3,  0,  5,
#     # -1,  2, -3,  4,  1,
#     #  0, -2,  3,  5, -4,
#     #  2, -1,  0,  4, -3,
#     #  1,  2, -2,  3,  0,
#     # -1,  4, -4,  2,  1
#     # ])
#     #c = np.array([1, -2, 3, -1, 1, 2, 1, -3, 3])
#     # c = np.array([
#     #  2, -1,  3,  0, -4, 
#     #  1,  5, -2,  0,  3,
#     # -3,  2,  1, -1,  4,
#     #  0, -2,  2
#     # ])
    
#     print("\n--- Optimize c·M ---")
#     max_mark, max_val = Optimize_max_reachable_marking(
#         pn.place_names, bdd, c
#     )
#     print("c:", c)
#     print("Max marking:", max_mark)
#     print("Max value:", max_val)
#     # ------------------------------------------------------
#     # 7. VẼ HÌNH PETRI NET BẰNG PM4PY (TASK 3)
#     # ------------------------------------------------------
#     print("\n=== DRAWING PETRI NET WITH PM4PY – Task 3 ===")
#     try:
#         pnml_path = filename  # dùng lại file PNML ở trên

#         # pm4py đọc PNML
#         pn_net, im, fm = pnml_importer.apply(pnml_path)

#         # Tạo graph
#         gviz = pn_vis.apply(pn_net, im, fm)

#         # Lưu ra file ảnh
#         output_img = "petri_net.png"
#         pn_vis.save(gviz, output_img)
#         print(f"Petri net image saved to: {output_img}")

#         # KHÔNG auto mở nữa cho đỡ lỗi
#         # pn_vis.view(gviz)

#     except Exception as e:
#         print("Không thể vẽ Petri net bằng pm4py. Chi tiết lỗi:")
#         print(e)



# if __name__ == "__main__":
#     main()

from src.PetriNet import PetriNet
from src.BDD import build_bdd
from src.Optimization import Optimize_max_reachable_marking
from src.BFS import bfs_reachable
from src.DFS import dfs_reachable
from src.Deadlock import deadlock_detection
from pyeda.inter import *
import numpy as np
import pm4py
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.visualization.petri_net import visualizer as pn_vis


# ================== CẤU HÌNH VECTOR c (cho task Optimize) ==================
# NHỚ chỉnh lại cho đúng số place trong Petri net của bạn
c = np.array([1, -2, 3, -1, 1, 2])


# ================== CÁC HÀM CHO TỪNG TASK ==================

def task_print_pn(pn: PetriNet):
    print("\n--- Thông tin Petri Net ---")
    print(pn)


def task_bfs(pn: PetriNet):
    print("\n--- BFS Reachable Markings ---")
    bfs_set = bfs_reachable(pn)
    for m in bfs_set:
        print(np.array(m))
    print("Total BFS reachable =", len(bfs_set))


def task_dfs(pn: PetriNet):
    print("\n--- DFS Reachable Markings ---")
    dfs_set = dfs_reachable(pn)
    for m in dfs_set:
        print(np.array(m))
    print("Total DFS reachable =", len(dfs_set))


def task_bdd(pn: PetriNet):
    print("\n--- BDD Reachable ---")
    bdd, count = build_bdd(pn)

    sats = list(bdd.satisfy_all())
    print("Satisfying all:", sats)

    expr = bdd2expr(bdd)
    # Nếu BDD không có biến đầu vào hoặc không có nghiệm thì KHÔNG gọi espresso_exprs
    if not bdd.inputs or len(sats) == 0:
        print("Minimized = (biểu thức hằng, không cần tối thiểu hóa):", expr)
    else:
        print("Minimized =", espresso_exprs(expr))

    print("BDD reachable markings =", count)

    return bdd, count


def task_deadlock(pn: PetriNet, cached_bdd=None):
    """
    Task DEADLOCK (task 4):
    - Dùng BDD (cache nếu có, không thì build mới)
    - In ra TẤT CẢ các deadlock marking
    - Nếu mảng rỗng thì in 'Không có deadlock reachable.'
    """
    print("\n--- Deadlock reachable markings ---")
    if cached_bdd is None:
        bdd, _ = build_bdd(pn)
    else:
        bdd = cached_bdd

    deadlocks = deadlock_detection(pn, bdd)
    # deadlocks có thể là None hoặc [] tùy cách bạn viết; xử lý cả 2
    if not deadlocks:  # None, [] đều vào đây
        print("No Deadlock")
        return

    print(f"Tổng số deadlock = {len(deadlocks)}")
    for i, m in enumerate(deadlocks, start=1):
        print(f"Deadlock {i}:", np.array(m))


def task_optimize(pn: PetriNet, cached_bdd=None):
    print("\n--- Optimize c·M ---")

    if cached_bdd is None:
        bdd, _ = build_bdd(pn)
    else:
        bdd = cached_bdd

    # Check chiều dài c cho chắc
    if len(c) != len(pn.place_names):
        print("Warning: Length vector c unavailable!")
        print(f"Số place = {len(pn.place_names)}, len(c) = {len(c)}")
        return

    max_mark, max_val = Optimize_max_reachable_marking(
        pn.place_names, bdd, c
    )
    print("c:", c)
    print("Max marking:", max_mark)
    print("Max value:", max_val)


def task_draw_pnml(filename: str):
    print("\n=== DRAWING PETRI NET WITH PM4PY ===")
    try:
        pnml_path = filename

        # pm4py đọc PNML
        pn_net, im, fm = pnml_importer.apply(pnml_path)

        # Tạo graph
        gviz = pn_vis.apply(pn_net, im, fm)

        # Lưu ra file ảnh
        output_img = "petri_net.png"
        pn_vis.save(gviz, output_img)
        print(f"Petri net image saved to: {output_img}")

        # Không tự mở hình để tránh lỗi môi trường
        # pn_vis.view(gviz)

    except Exception as e:
        print("Can not draw Petri Net. Detail:")
        print(e)


def task_run_all(pn: PetriNet, filename: str):
    """
    Chạy lần lượt:
    1. In PN
    2. BFS
    3. DFS
    4. BDD
    5. Deadlock (dùng BDD)
    6. Optimize (dùng BDD)
    7. Vẽ Petri net bằng PM4PY
    """
    print("\n========== RUN ALL TASKS ==========")

    task_print_pn(pn)
    task_bfs(pn)
    task_dfs(pn)

    bdd, count = task_bdd(pn)

    task_deadlock(pn, bdd)
    task_optimize(pn, bdd)

    task_draw_pnml(filename)

    print("\n========== DONE ALL TASKS ==========")
    return bdd, count


# ================== HÀM MAIN VỚI MENU ==================

def main():
    # 1. Nhập file PNML
    filename = "test_PNML/Input.pnml"
    print("Loading PNML:", filename)

    pn = PetriNet.build_pnml(filename)
    print("\n--- Petri Net Loaded ---")

    # Cache BDD để dùng lại cho các task 4–6
    cached_bdd = None
    cached_bdd_count = None

    while True:
        print("\n================= MENU TASK =================")
        print("1. Task 1")
        print("2. Task 2 BFS")
        print("3. Task 2 DFS")
        print("4. Task 3")
        print("5. Task 4")
        print("6. Task 5")
        print("7. Draw Petri Net")
        print("8. Run All Task")
        print("0. Exit")
        print("=================================================")

        choice = input("Choose task: ").strip()

        if choice == "1":
            task_print_pn(pn)

        elif choice == "2":
            task_bfs(pn)

        elif choice == "3":
            task_dfs(pn)

        elif choice == "4":
            # BDD reachable
            cached_bdd, cached_bdd_count = task_bdd(pn)

        elif choice == "5":
            # Deadlock detection – yêu cầu BDD
            if cached_bdd is None:
                cached_bdd, cached_bdd_count = build_bdd(pn)
            task_deadlock(pn, cached_bdd)

        elif choice == "6":
            # Optimize – yêu cầu BDD
            if cached_bdd is None:
                cached_bdd, cached_bdd_count = build_bdd(pn)
            task_optimize(pn, cached_bdd)

        elif choice == "7":
            task_draw_pnml(filename)

        elif choice == "8":
            # Chạy tất cả và update cache BDD
            cached_bdd, cached_bdd_count = task_run_all(pn, filename)

        elif choice == "0":
            print("Program Finished.")
            break

        else:
            print("Invalid Input. Please try again")


if __name__ == "__main__":
    main()

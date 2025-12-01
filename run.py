from src.PetriNet import PetriNet
from src.BDD import build_bdd
from src.Optimization import Optimize_max_reachable_marking
from src.BFS import bfs_reachable
from src.DFS import dfs_reachable
from src.Deadlock import deadlock_detection
from pyeda.inter import * 
import numpy as np
## from graphviz import Source

def main():
    # ------------------------------------------------------
    # 1. Load Petri Net từ file PNML
    # ------------------------------------------------------
    filename = "Input_pnml_file.pnml"   # đổi file tại đây
    print("Loading PNML:", filename)

    pn = PetriNet.build_pnml(filename)
    print("\n--- Petri Net Loaded ---")
    print(pn)

    # ------------------------------------------------------
    # 2. BFS reachable
    # ------------------------------------------------------
    print("\n--- BFS Reachable Markings ---")
    bfs_set = bfs_reachable(pn)
    for m in bfs_set:
        print(np.array(m))
    print("Total BFS reachable =", len(bfs_set))

    # ------------------------------------------------------
    # 3. DFS reachable
    # ------------------------------------------------------
    print("\n--- DFS Reachable Markings ---")
    dfs_set = dfs_reachable(pn)
    for m in dfs_set:
        print(np.array(m))
    print("Total DFS reachable =", len(dfs_set))

    # ------------------------------------------------------
    # 4. BDD reachable
    # ------------------------------------------------------
    print("\n--- BDD Reachable ---")
    bdd, count = build_bdd(pn)
    print("Satisfying all:", list(bdd.satisfy_all()))
    print("Minimized =", espresso_exprs(bdd2expr(bdd)))
    print("BDD reachable markings =", count)
    ## Source(bdd.to_dot()).render("bdd", format="png", cleanup=True)

    # ------------------------------------------------------
    # 5. Deadlock detection
    # ------------------------------------------------------
    print("\n--- Deadlock reachable marking ---")
    dead = deadlock_detection(pn, bdd)
    if dead is not None:
        print("Deadlock marking:", dead)
    else:
        print("No deadlock reachable.")

    # ------------------------------------------------------
    # 6. Optimization: maximize c·M
    # ------------------------------------------------------
    c = np.array([1, -2, 3, -1])
    # c = np.array([
    #  1, -2,  3,  0,  5,
    # -1,  2, -3,  4,  1,
    #  0, -2,  3,  5, -4,
    #  2, -1,  0,  4, -3,
    #  1,  2, -2,  3,  0,
    # -1,  4, -4,  2,  1
    # ])
    #c = np.array([1, -2, 3, -1, 1, 2, 1, -3, 3])
    # c = np.array([
    #  2, -1,  3,  0, -4, 
    #  1,  5, -2,  0,  3,
    # -3,  2,  1, -1,  4,
    #  0, -2,  2
    # ])
    print("\n--- Optimize c·M ---")
    max_mark, max_val = Optimize_max_reachable_marking(
        pn.place_names, bdd, c
    )
    print("c:", c)
    print("Max marking:", max_mark)
    print("Max value:", max_val)


if __name__ == "__main__":
    main()

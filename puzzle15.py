"""P02 starter: 15-puzzle representation, scrambler and Manhattan heuristic. State: tuple of 16, 0 = blank."""
import random
import time
GOAL = tuple(list(range(1, 16)) + [0])
GOAL_POS = {v: divmod(i, 4) for i, v in enumerate(GOAL)}
NEIGHBOURS = {i: [j for j in (i - 4, i + 4, i - 1 if i % 4 else -1, i + 1 if i % 4 < 3 else -1) if 0 <= j < 16]
              for i in range(16)}

def successors(state):
    b = state.index(0)
    for j in NEIGHBOURS[b]:
        s = list(state); s[b], s[j] = s[j], s[b]
        yield tuple(s)

def manhattan(state):
    return sum(abs(i // 4 - GOAL_POS[v][0]) + abs(i % 4 - GOAL_POS[v][1]) for i, v in enumerate(state) if v)



'''def linear_conflict(state):
    md = manhattan(state)
    conflicts = 0

    # Check conflicts in rows
    for row in range(4):
        for i in range(4):
            for j in range(i + 1, 4):

                tile1 = state[row * 4 + i]
                tile2 = state[row * 4 + j]

                if tile1 != 0 and tile2 != 0:
                    goal_row1, goal_col1 = GOAL_POS[tile1]
                    goal_row2, goal_col2 = GOAL_POS[tile2]

                    if goal_row1 == row and goal_row2 == row:
                        if goal_col1 > goal_col2:
                            conflicts += 1

    # Check conflicts in columns
    for col in range(4):
        for i in range(4):
            for j in range(i + 1, 4):

                tile1 = state[i * 4 + col]
                tile2 = state[j * 4 + col]

                if tile1 != 0 and tile2 != 0:
                    goal_row1, goal_col1 = GOAL_POS[tile1]
                    goal_row2, goal_col2 = GOAL_POS[tile2]

                    if goal_col1 == col and goal_col2 == col:
                        if goal_row1 > goal_row2:
                            conflicts += 1

    return md + 2 * conflicts
'''

def linear_conflict(state):
    md = manhattan(state)

    def max_disjoint_conflicts(pairs):
        best = 0

        def find(pairs_left, used):
            nonlocal best

            if not pairs_left:
                best = max(best, len(used) // 2)
                return

            a, b = pairs_left[0]

            # Option 1: Skip this conflict
            find(pairs_left[1:], used)

            # Option 2: Use this pair if neither tile is used
            if a not in used and b not in used:
                find(pairs_left[1:], used | {a, b})

        find(pairs, set())
        return best

    conflicts = 0

    # Row conflicts
    for row in range(4):
        pairs = []

        for i in range(4):
            for j in range(i + 1, 4):
                t1 = state[row * 4 + i]
                t2 = state[row * 4 + j]

                if t1 and t2:
                    r1, c1 = GOAL_POS[t1]
                    r2, c2 = GOAL_POS[t2]

                    if r1 == row and r2 == row and c1 > c2:
                        pairs.append((t1, t2))

        conflicts += max_disjoint_conflicts(pairs)

    # Column conflicts
    for col in range(4):
        pairs = []

        for i in range(4):
            for j in range(i + 1, 4):
                t1 = state[i * 4 + col]
                t2 = state[j * 4 + col]

                if t1 and t2:
                    r1, c1 = GOAL_POS[t1]
                    r2, c2 = GOAL_POS[t2]

                    if c1 == col and c2 == col and r1 > r2:
                        pairs.append((t1, t2))

        conflicts += max_disjoint_conflicts(pairs)

    return md + 2 * conflicts


from collections import deque

def build_pattern_database(pattern):
    """Build one additive pattern database using 0-1 BFS."""

    # Abstract goal: blank position followed by pattern tile positions
    goal_state = (15,) + tuple(GOAL.index(tile) for tile in pattern)

    distances = {goal_state: 0}
    queue = deque([goal_state])

    while queue:
        current = queue.popleft()
        blank = current[0]
        current_distance = distances[current]

        for next_pos in NEIGHBOURS[blank]:
            new_state = list(current)
            new_state[0] = next_pos

            move_cost = 0

            # Check whether the moved position contains a pattern tile
            for i in range(1, len(current)):
                if current[i] == next_pos:
                    new_state[i] = blank
                    move_cost = 1
                    break

            new_state = tuple(new_state)
            new_distance = current_distance + move_cost

            if new_distance < distances.get(new_state, float("inf")):
                distances[new_state] = new_distance

                if move_cost == 0:
                    queue.appendleft(new_state)
                else:
                    queue.append(new_state)

    return distances


def build_additive_pdb():
    """Build five disjoint patterns containing three tiles each."""

    patterns = [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (10, 11, 12),
        (13, 14, 15)
    ]

    databases = []

    for pattern in patterns:
        print("Building pattern:", pattern)
        database = build_pattern_database(pattern)
        databases.append(database)
        print("States stored:", len(database))

    return patterns, databases


def pdb_heuristic(state, patterns, databases):
    """Calculate the sum of additive pattern database values."""

    blank = state.index(0)
    total = 0

    for pattern, database in zip(patterns, databases):
        abstract_state = (blank,) + tuple(
            state.index(tile) for tile in pattern
        )

        total += database[abstract_state]

    return total

def scramble(k, seed):
    """Random walk of k moves from the goal (never undoing the last move); always solvable."""
    rng = random.Random(seed); s = list(GOAL); b, prev = 15, -1
    for _ in range(k):
        j = rng.choice([x for x in NEIGHBOURS[b] if x != prev])
        s[b], s[j] = s[j], s[b]; prev, b = b, j
    return tuple(s)

def ida_star(start, h=manhattan):
    """IDA* search. Returns (solution_path, expanded_nodes)."""

    threshold = h(start)
    path = [start]
    visited = {start}
    expanded = 0

    def search(state, g, threshold):
        nonlocal expanded

        f = g + h(state)

        # Prune this path if its estimated cost exceeds the threshold
        if f > threshold:
            return f

        # Goal test
        if state == GOAL:
            return True

        expanded += 1
        minimum = float("inf")

        # Explore all possible next states
        for next_state in successors(state):

            # Avoid revisiting a state already on the current path
            if next_state not in visited:
                visited.add(next_state)
                path.append(next_state)

                result = search(next_state, g + 1, threshold)

                if result is True:
                    return True

                minimum = min(minimum, result)

                # Backtrack
                path.pop()
                visited.remove(next_state)

        return minimum

    while True:
        result = search(start, 0, threshold)

        if result is True:
            return path, expanded

        if result == float("inf"):
            return None, expanded

        # Increase the threshold to the smallest exceeded f-value
        threshold = result

# TODO (students): linear_conflict(state), ida_star(start, h), a pattern database (e.g. 7-8 split)

'''if __name__ == "__main__":
    for seed in range(3):
        s = scramble(60, seed)
        print(seed, s, "h_MD =", manhattan(s))'''
def validate_solution(path):
    if path is None:
        return False

    for i in range(len(path) - 1):
        if path[i + 1] not in successors(path[i]):
            return False

    return path[-1] == GOAL
if __name__ == "__main__":
    for seed in range(3):
        s = scramble(60, seed)
        print(seed, s, "h_MD =", manhattan(s))

    print("\nTesting IDA*:")

    start = (1, 2, 3, 4,
             5, 6, 7, 8,
             9, 10, 11, 12,
             13, 14, 0, 15)

    solution, nodes = ida_star(start)

    print("Moves:", len(solution) - 1)
    print("Expanded nodes:", nodes)
    
    test_state =(2, 3, 1, 4,
              5, 6, 7, 8,
              9, 10, 11, 12,
              13, 14, 15, 0)

    print("\nHeuristic comparison:")
    print("Manhattan Distance:", manhattan(test_state))
    print("Manhattan + Linear Conflict:", linear_conflict(test_state))
    
    print("\nComparing IDA* heuristics:")

    solution1, nodes1 = ida_star(test_state, manhattan)
    solution2, nodes2 = ida_star(test_state, linear_conflict)

    print("Manhattan - Moves:", len(solution1)-1,
          "Expanded:", nodes1)

    print("MD + LC - Moves:", len(solution2)-1,
          "Expanded:", nodes2)
    
    print("\nBuilding Pattern Databases:")

    start_time = time.perf_counter()
    patterns, databases = build_additive_pdb()
    build_time = time.perf_counter() - start_time

    print("PDB build time:", round(build_time, 2), "seconds")

    print("\nPDB Heuristic Comparison:")

    pdb_value = pdb_heuristic(test_state, patterns, databases)

    print("Manhattan Distance:", manhattan(test_state))
    print("Linear Conflict:", linear_conflict(test_state))
    print("Pattern Database:", pdb_value)

    print("\nTesting IDA* with PDB:")

    solution3, nodes3 = ida_star(
        test_state,
        lambda s: pdb_heuristic(s, patterns, databases)
    )

    print("PDB - Moves:", len(solution3) - 1)
    print("PDB - Expanded nodes:", nodes3)
    
    print("\nFINAL EXPERIMENTS")

    test_cases = [
        ("Easy", 20, 10),
        ("Medium", 30, 20),
        ("Hard", 40, 30)
    ]

    heuristics = [
        ("Manhattan", manhattan),
        ("Linear Conflict", linear_conflict),
        ("PDB", lambda s: pdb_heuristic(s, patterns, databases))
    ]

    for difficulty, scramble_moves, seed in test_cases:

        state = scramble(scramble_moves, seed)

        print("\nDifficulty:", difficulty)
        print("Initial Manhattan:", manhattan(state))

        for name, heuristic in heuristics:

            start_time = time.perf_counter()

            solution, expanded = ida_star(state, heuristic)
            print("Valid solution:", validate_solution(solution))
            elapsed = time.perf_counter() - start_time

            if solution is not None:
                moves = len(solution) - 1
            else:
                moves = "Not solved"

            print(
                name,
                "| Moves:", moves,
                "| Expanded:", expanded,
                "| Time:", round(elapsed, 4), "seconds"
            )





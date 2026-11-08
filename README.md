# P02 – The 15-Puzzle: Better Heuristics, Less Search

**EC3161 – Artificial Intelligence Mini Project**

**KOLLIPARA SAI SPOORTHI** | **624132**  
Electronics and Communication Engineering  
National Institute of Technology Andhra Pradesh

> **Key Result:** Additive Pattern Database (PDB) reduced IDA* node expansions by up to **79.7%** compared with Manhattan Distance in the tested instances.

## Overview

This project implements and compares three heuristics for solving the 15-puzzle using **Iterative Deepening A* (IDA*)**:

- Manhattan Distance
- Linear Conflict
- Additive Pattern Database (PDB)

The objective is to reduce the number of search nodes expanded while finding solutions of the same length.

## Problem

The 15-puzzle consists of a 4 × 4 board containing 15 numbered tiles and one blank space (`0`).

**Goal state:**

```text
1  2  3  4
5  6  7  8
9 10 11 12
13 14 15  0
```

- **State:** A tuple of 16 integers.
- **Actions:** Move the blank up, down, left, or right.
- **Move cost:** 1 per move.
- **Objective:** Reach the goal state using the minimum number of moves.

## Methods

All three heuristics are evaluated using IDA* with:

\[
f(n)=g(n)+h(n)
\]

| Heuristic | Description |
|---|---|
| Manhattan Distance | Sum of horizontal and vertical distances of tiles from their goal positions. |
| Linear Conflict | Manhattan Distance plus 2 for each selected non-overlapping linear conflict pair. |
| Additive PDB | Sum of precomputed distances from five disjoint tile patterns. |

### Additive Pattern Database

Five disjoint patterns are used:

```python
(1, 2, 3)
(4, 5, 6)
(7, 8, 9)
(10, 11, 12)
(13, 14, 15)
```

- Each pattern contains 3 numbered tiles and the blank.
- Each database contains 43,680 abstract states.
- Total database entries: **218,400**.
- Databases are constructed using reverse **0–1 BFS**.
- Pattern tile moves have cost 1; non-pattern tile moves have cost 0.
- The final heuristic is the sum of all five pattern database values.

## Experimental Results

Three test instances were generated using fixed random seeds.

| Test | Scramble moves | Seed |
|---|---:|---:|
| Easy | 20 | 10 |
| Medium | 30 | 20 |
| Hard | 40 | 30 |

*Easy, Medium, and Hard are experiment labels; scramble length does not necessarily equal optimal solution depth.*

### Results comparison

| Test | Heuristic | Solution moves | Expanded nodes | Time (s) |
|---|---|---:|---:|---:|
| Easy | Manhattan | 20 | 31 | 0.0004 |
| | Linear Conflict | 20 | 31 | 0.0037 |
| | Additive PDB | 20 | **30** | 0.0006 |
| Medium | Manhattan | 30 | 16,550 | 0.1626 |
| | Linear Conflict | 30 | 9,527 | 0.4765 |
| | Additive PDB | 30 | **3,365** | 0.0506 |
| Hard | Manhattan | 26 | 79 | 0.0008 |
| | Linear Conflict | 26 | 45 | 0.0032 |
| | Additive PDB | 26 | **26** | 0.0007 |

**PDB construction time:** 0.47 seconds.

### Key observations

- All three heuristics returned the same solution length for each test.
- Additive PDB expanded the fewest nodes in all three tests.
- Maximum reduction compared with Manhattan Distance: **79.7%**.
- Linear Conflict reduced node expansions but had higher execution time due to additional heuristic computation.
- PDB requires preprocessing, but its stored values can be reused during search.

## Correctness Evidence

- Initial states are generated through legal moves from the goal state, so they are solvable.
- Successor generation checks the valid movements of the blank.
- All three heuristics were evaluated on the same test instances.
- All three returned identical solution lengths for each instance.

**Limitations:** No independent exact solver or separate automated solution-path replay test was used to verify optimality.

## How to Run

**Requirements**
- Python 3
- No external Python packages required

**Run the program:**

```bash
python puzzle15.py
```

The program constructs the pattern databases and runs the experiments.

## Environment

| Component | Details |
|---|---|
| Operating System | Windows 11 |
| Python Version | 3.13.14 |
| Search Algorithm | IDA* |
| Puzzle | 15-Puzzle (4 × 4) |

## AI-Use Statement

AI tools were used for understanding heuristic search concepts, debugging assistance, explaining implementation details, and improving project documentation.

## References

1. EC3161 Artificial Intelligence Mini-Project Assignment, NIT Andhra Pradesh, 2026–27.
2. Stuart Russell and Peter Norvig, *Artificial Intelligence: A Modern Approach*, 4th Edition.
3. Richard E. Korf, “Depth-First Iterative-Deepening: An Optimal Admissible Tree Search,” 1985.
4. Richard E. Korf and Ariel Felner, “Disjoint Pattern Database Heuristics,” 2002.
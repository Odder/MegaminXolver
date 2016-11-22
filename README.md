# MegaminXolver
A python megaminx solver for solving the last 2 faces 2-gen \<L,U\>. It can find 20 move solutions on my Acer C720 Chromebook in less than 20 seconds using the pypy compiler :)

# Usage
Take a peak in the example.py file to see how I use it.
```python
from MegaminXolver import MegaminXolver
megaminx = MegaminXolver() # Create new MegaminXolver instance
megaminx.createMoveTable() # If this is not done... GG.

"""
Optimally you want to have your hashTable half the size of the solutions you want to find. 
You can run a search without, but I guarantee you it will run slow
"""
megaminx.createHashTable(9)

"""
You can create a state in 2 different ways, by describing it, and by applying a move string
"""
scramble = megaminx.applySequence("L' U' L U", mega.solvedState)
scramble = megaminx.getStateFromState({
  'edgePermutation': [2,0,1,3,4,5,6,7,8], # U-perm
  'cornerOrientation': [0,0,0,0,0,0,0,0],
  'cornerPermutation': [0,1,2,3,4,5,6,7]
})

"""
Solve it
"""
megaminx.solve(scramble, 5) # 5 = number of solutions
```

You can now run it with Python 3! (I use PyPy for a massive speed boost)

# What sort of magic is this?
Yeah well, people always says "Python is slow" so I thought it would be a great choice for something that needs to solve computationally "heavy" tasks. My first version that could solve something, spend almost 1 minute for finding a 6 move solution, so in order to reach 20 moves in under 20 seconds, I had to use quite a few neat tricks.

## Move table
We first create a table for all possible corner or edge permutation / orientation cases, (3 sets total) each state we just give a number for identification. We then iterate over all of these states and apply U and L and figure out what states you get from any given state. This allows us to efficiently answer this question "Corner Permutation looks like 21423, I want to do a U-turn, what will corners look like afterwards?"

## Hash table
In order to speed up things a lot we first make a search of depth n from the solved state, this allows us to check if any state we encounter in a solve search can be solved within n moves. It initially used a string concatenation of the state to easily look up states, but I have exchanged that with a simple binary representation for a 20-30% speed boost

## SOLVE!
Just a simple BFS using a queue. It checks current state up against the hash table to see if something is solved

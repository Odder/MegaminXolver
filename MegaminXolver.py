import time, itertools
from collections import deque

class MegaminXolver:
  
  def __init__(self):

    self.state = {
      'edgePermutation': 0,
      'cornerOrientation': 0,
      'cornerPermutation': 0
    }

    self.solvedState = {
      'edgePermutation': 0,
      'cornerOrientation': 0,
      'cornerPermutation': 0
    }

    self.hasHashTable = False
    self.hashTable = []
    self.hashDepth = 0
    self.revEPMoveTable = {}
    self.EPMoveTable = {}
    self.revCPMoveTable = {}
    self.CPMoveTable = {}
    self.revCOMoveTable = {}
    self.COMoveTable = {}

  def createMoveTable(self):
    
    edgePermutations = itertools.permutations( range(9) )
    cornerPermutations = itertools.permutations( range(8) )
    cornerOrientations = itertools.product( range(3), repeat=8 )
    self.revEPMoveTable = {}
    self.revCPMoveTable = {}
    self.revCOMoveTable = {}
    self.EPMoveTable = [x for x in range(362880)]
    self.CPMoveTable = [x for x in range(40320)]
    self.COMoveTable = [x for x in range(2187)]
    k = 0

    startTime = time.time()

    # EP
    for permutation in edgePermutations:

      self.revEPMoveTable[','.join([str(x) for x in permutation])] = k
      k += 1

    for permutation in self.revEPMoveTable.keys():

      case = [int(x) for x in permutation.split(',')]
      k = self.revEPMoveTable[permutation]
      caseU, caseL = case[:], case[:]
      
      caseU[0], caseU[1], caseU[2], caseU[3], caseU[4] = case[4], case[0], case[1], case[2], case[3]
      caseL[4], caseL[5], caseL[6], caseL[7], caseL[8] = case[8], case[4], case[5], case[6], case[7]

      strCaseU = ','.join([str(x) for x in caseU])
      strCaseL = ','.join([str(x) for x in caseL])

      self.EPMoveTable[k] = [self.revEPMoveTable[strCaseU], self.revEPMoveTable[strCaseL]]

    # CP
    k = 0
    for permutation in cornerPermutations:

      self.revCPMoveTable[','.join([str(x) for x in permutation])] = k
      k += 1

    for permutation in self.revCPMoveTable.keys():

      case = [int(x) for x in permutation.split(',')]
      k = self.revCPMoveTable[permutation]
      caseU, caseL = case[:], case[:]
      
      caseU[0], caseU[1], caseU[2], caseU[3], caseU[4] = case[4], case[0], case[1], case[2], case[3]
      caseL[0], caseL[4], caseL[5], caseL[6], caseL[7] = case[7], case[0], case[4], case[5], case[6]

      strCaseU = ','.join([str(x) for x in caseU])
      strCaseL = ','.join([str(x) for x in caseL])

      self.CPMoveTable[k] = [self.revCPMoveTable[strCaseU], self.revCPMoveTable[strCaseL]]

    # CO
    k = 0
    for permutation in cornerOrientations:

      if sum(permutation) % 3 != 0: 
        continue

      self.revCOMoveTable[','.join([str(x) for x in permutation])] = k
      k += 1

    for permutation in self.revCOMoveTable.keys():

      case = [int(x) for x in permutation.split(',')]
      k = self.revCOMoveTable[permutation]
      caseL = case[:]
      caseU = case[:]
      
      caseU[0], caseU[1], caseU[2], caseU[3], caseU[4] = case[4], case[0], case[1], case[2], case[3]
      caseL[0], caseL[4], caseL[5], caseL[6], caseL[7] = (case[7] + 2) % 3, (case[0] + 1) % 3, case[4], (case[5] + 2) % 3, (case[6] + 1) % 3

      strCaseL = ','.join([str(x) for x in caseL])
      strCaseU = ','.join([str(x) for x in caseU])

      self.COMoveTable[k] = [self.revCOMoveTable[strCaseU], self.revCOMoveTable[strCaseL]]


    print( 'Move tables done in %fs' % (time.time() - startTime,) )

  def createHashTable(self, depth):

    queue = deque()
    startTime = time.time()
    print( 'Creating hash table' )

    entries = 8 * pow(4, depth-2)
    k = 8
    self.hashTable = {}

    #Create Intial queue
    for i in range(2):
      for j in range(4):
        state = dict(self.solvedState)
        currentState = self.doFastTurn(state, (i<<3) + j)
        currentSolution = [(i<<3) + j]

        hash = self.getHashFromState(currentState)
        self.hashTable[hash] = currentSolution

        queue.append({
          'state': currentState,
          'axisApplied': i,
          'solution': currentSolution
        })

    for solution in range(entries):
      currentPosition = queue.popleft()
      oldState = dict(currentPosition['state'])

      for j in range(4):

        currentSolution = currentPosition['solution'][:]

        # If not solution, append to queue
        i = ( currentPosition['axisApplied'] + 1 ) & 1
        moveToApply = (i<<3) + j 

        currentState = self.doFastTurn(oldState, moveToApply)
        currentSolution.append(moveToApply)

        # Append to hashtable
        hash = self.getHashFromState(currentState)
        self.hashTable[hash] = currentSolution

        queue.append({
          'state': currentState,
          'axisApplied': i,
          'solution': currentSolution
        })

        k+=1

    self.hasHashTable = True
    self.hashDepth = depth
    print( 'Hash table (depth: %i; entries: %i) done in %fs' % (depth, k, time.time() - startTime) )

  def solve(self, state, maxSolutions = 0):

    queue = deque()
    k = 0
    solutions = 0
    startTime = time.time()

    # create initial queue
    for i in range(2):
      for j in range(4):
        currentState = dict(state)
        currentState = self.doFastTurn(state, (i<<3) + j)
        currentSolution = [(i<<3) + j]

        queue.append({
          'state': currentState,
          'axisApplied': i,
          'solution': currentSolution
        })

    while(True):

      k+=1

      currentPosition = queue.popleft()
      i = ( currentPosition['axisApplied'] + 1 ) & 1

      for j in range(4):

        currentState = dict(currentPosition['state'])
        currentSolution = list(currentPosition['solution'])

        # Apply move to current iteration
        move = (i << 3) + j

        currentState = self.doFastTurn(currentState, move)
        currentSolution.append(move)

        # Is solved?
        isSolved = self.isSolved(currentState)
        if not isSolved:
          queue.append({
            'state': currentState,
            'axisApplied': i,
            'solution': currentSolution
          })

        else:
          endTime = time.time() - startTime
          solution = self.getAlgorithm( currentSolution + isSolved )
          solutions += 1
          print('Found a solution in %f seconds\n%s (%i,%i moves)' % (endTime, solution['string'], solution['turns'], solution['fTurns'] ) )
          if solutions >= maxSolutions:
            return {
              'state': currentState,
              'solution': solution
            }

  def doFastTurn(self, state, move):

    surface = move >> 3
    length = move % 4

    newState = dict(state)

    for i in range(length + 1):
      newState['edgePermutation'] = self.EPMoveTable[newState['edgePermutation']][surface]
      newState['cornerPermutation'] = self.CPMoveTable[newState['cornerPermutation']][surface]
      newState['cornerOrientation'] = self.COMoveTable[newState['cornerOrientation']][surface]

    return newState

  def isSolved(self, state):

    if self.hasHashTable:
      hashedState = self.getHashFromState( state )
      if hashedState in self.hashTable:
        reverseSolution = self.hashTable[self.getHashFromState( state )]
        solution = self.getMoveStringFromHashSolution( reverseSolution )
        # print('Found solution in hashtable', solution)
        return solution

    if state == self.solvedState:
      return [16]

    return False

  def applyState(self, state):

    strEP = ','.join([str(x) for x in state['edgePermutation']])

    state['edgePermutation'] = self.revEPMoveTable[strEP]

    self.state = state

  def applySequence(self, moves, state):

    moves = moves.split(' ')

    for move in moves:
      state = self.doFastTurn(state, self.getTurnFromString(move))

    return state

  def getHashFromState(self, state):

    hash = (state['edgePermutation'] << 29) + (state['cornerPermutation'] << 13) + (state['cornerOrientation'])
    return hash

  def getAlgorithm(self, sequence):

    string = ''
    moves = 'UL*'
    postfix = ['','2','2\'', '\'']
    algorithm = {
      'string': '',
      'turns': 0,
      'fTurns': 0 # fifth turns
    }

    for move in sequence:
      i = move >> 3
      j = move & 3

      if i < 2:
        algorithm['string'] += moves[i] + postfix[j] + ' '
        algorithm['turns'] += 1
        algorithm['fTurns'] += int( ( ( j + 1 ) % 4 ) / 2 ) + 1

    return algorithm
    
  def getMoveStringFromHashSolution(self, hashSolution):

    solution = []

    for move in hashSolution[::-1]:
      i = move >> 3
      j = 3 - (move & 3)
      solution.append((i<<3) + j)

    return solution

  def getTurnFromString(self, string):

    moves = {
      'U': 0,
      'U2': 1,
      'U\'2': 2,
      'U\'': 3,
      'L': 8,
      'L2': 9,
      'L\'2': 10,
      'L\'': 11
    }

    move = moves[string]

    return move

  def getStateFromState(self, state):

    strEP = ','.join([str(x) for x in state['edgePermutation']])
    state['edgePermutation'] = self.revEPMoveTable[strEP]

    strCP = ','.join([str(x) for x in state['cornerPermutation']])
    state['cornerPermutation'] = self.revCPMoveTable[strCP]

    strCO = ','.join([str(x) for x in state['cornerOrientation']])
    state['cornerOrientation'] = self.revCOMoveTable[strCO]

    return state

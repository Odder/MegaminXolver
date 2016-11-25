from MegaminXolver import MegaminXolver

megaminx = MegaminXolver()
megaminx.createMoveTable()

hashTableDepth = int(raw_input('How deep do you want the hash table? '))
megaminx.createHashTable(hashTableDepth)

k = 0

while(True):

  fileName = str( raw_input('Scramble file: ') )
  f = file( fileName + '.mx' )
  scrambles = f.read()

  for state in scrambles.split('\n\n'):

    scramble = {}
    maxSolutions = 1
    k += 1

    for line in state.split('\n'):

      pair = line.split(':')

      if len(pair) == 2:

        setting = pair[0]
        value = pair[1]

        if setting == 'SOLUTIONS':
          maxSolutions = int(value)

        elif setting == 'EP':
          scramble['edgePermutation'] = [int(x) for x in value.split(',')]

        elif setting == 'CP':
          scramble['cornerPermutation'] = [int(x) for x in value.split(',')]

        elif setting == 'CO':
          scramble['cornerOrientation'] = [int(x) for x in value.split(',')]

    print( 'Solving case #' + str(k) )
    scramble = megaminx.getStateFromState(scramble)
    megaminx.solve(scramble, maxSolutions)

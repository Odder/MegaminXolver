from MegaminXolver import MegaminXolver

mega = MegaminXolver()
mega.createMoveTable()
mega.createHashTable(9)

scramble = mega.getStateFromState({
  'edgePermutation': [2,0,1,3,4,5,6,7,8],
  'cornerOrientation': [0,0,0,0,0,0,0,0],
  'cornerPermutation': [0,1,2,3,4,5,6,7]
})
solution = mega.solve(scramble, 5)
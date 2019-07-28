from MegaminXolver import MegaminXolver

mega = MegaminXolver()
mega.create_move_table()
mega.create_hash_table(9)

scramble = mega.get_state_from_state({
    'ep': (2, 0, 1, 3, 4, 5, 6, 7, 8),
    'co': (0, 0, 0, 0, 0, 0, 0, 0),
    'cp': (0, 1, 2, 3, 4, 5, 6, 7)
})

solution = mega.solve(scramble, 5)
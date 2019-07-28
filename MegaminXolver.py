import time
import itertools
from collections import deque


class MegaminXolver:
    def __init__(self):
        self.state = (0, 0, 0)
        self.solved_state = (0, 0, 0)
        self.has_hash_table = False
        self.hash_table = {}
        self.has_depth = 0
        self.rev_ep_move_table = {}
        self.ep_move_table = {}
        self.rev_cp_move_table = {}
        self.cp_move_table = {}
        self.rev_co_move_table = {}
        self.co_move_table = {}

    def create_move_table(self):
        eps = itertools.permutations(range(9))
        cps = itertools.permutations(range(8))
        cos = itertools.product(range(3), repeat=8)
        self.rev_ep_move_table = {}
        self.rev_cp_move_table = {}
        self.rev_co_move_table = {}
        self.ep_move_table = [x for x in range(362880)]
        self.cp_move_table = [x for x in range(40320)]
        self.co_move_table = [x for x in range(2187)]
        k = 0

        start_time = time.time()

        # EP
        for permutation in eps:
            self.rev_ep_move_table[permutation] = k
            k += 1
        for permutation in self.rev_ep_move_table.keys():
            case = list(permutation)
            k = self.rev_ep_move_table[permutation]
            case_u, case_l = case[:], case[:]

            case_u[0], case_u[1], case_u[2], case_u[3], case_u[4] = case[4], case[0], case[1], case[2], case[3]
            case_l[4], case_l[5], case_l[6], case_l[7], case_l[8] = case[8], case[4], case[5], case[6], case[7]

            self.ep_move_table[k] = [self.rev_ep_move_table[tuple(case_u)], self.rev_ep_move_table[tuple(case_l)]]

        # CP
        k = 0
        for permutation in cps:
            self.rev_cp_move_table[permutation] = k
            k += 1
        for permutation in self.rev_cp_move_table.keys():
            case = list(permutation)
            k = self.rev_cp_move_table[permutation]
            case_u, case_l = case[:], case[:]

            case_u[0], case_u[1], case_u[2], case_u[3], case_u[4] = case[4], case[0], case[1], case[2], case[3]
            case_l[0], case_l[4], case_l[5], case_l[6], case_l[7] = case[7], case[0], case[4], case[5], case[6]

            self.cp_move_table[k] = [self.rev_cp_move_table[tuple(case_u)], self.rev_cp_move_table[tuple(case_l)]]

        # CO
        k = 0
        for permutation in cos:
            if sum(permutation) % 3 != 0:
                continue
            self.rev_co_move_table[permutation] = k
            k += 1

        for permutation in self.rev_co_move_table.keys():
            case = list(permutation)
            k = self.rev_co_move_table[permutation]
            case_u, case_l = case[:], case[:]

            case_u[0], case_u[1], case_u[2], case_u[3], case_u[4] = case[4], case[0], case[1], case[2], case[3]
            case_l[0], case_l[4], case_l[5], case_l[6], case_l[7] = (case[7] + 2) % 3, (case[0] + 1) % 3, case[4], (
                        case[5] + 2) % 3, (case[6] + 1) % 3

            self.co_move_table[k] = [self.rev_co_move_table[tuple(case_u)], self.rev_co_move_table[tuple(case_l)]]

        print('Move tables done in %fs' % (time.time() - start_time,))

    def create_hash_table(self, depth):
        queue = deque()
        start_time = time.time()
        print('Creating hash table')

        entries = 8 * pow(4, depth - 2)
        k = 8
        self.hash_table = {}

        # Create intial queue
        for i in range(2):
            for j in range(4):
                state = self.solved_state
                current_state = self.fast_turn(state, (i << 3) + j)
                current_solution = [(i << 3) + j]

                hash = self.get_hash_from_state(current_state)
                self.hash_table[hash] = current_solution

                queue.append({
                    'state': current_state,
                    'axis_applied': i,
                    'solution': current_solution
                })

        for solution in range(entries):
            current_position = queue.popleft()
            old_state = current_position['state']

            for j in range(4):
                current_solution = current_position['solution'][:]

                # If not solution, append to queue
                i = (current_position['axis_applied'] + 1) & 1
                move_to_apply = (i << 3) + j

                current_state = self.fast_turn(old_state, move_to_apply)
                current_solution.append(move_to_apply)

                # Append to hashtable
                hash = self.get_hash_from_state(current_state)
                self.hash_table[hash] = current_solution

                queue.append({
                    'state': current_state,
                    'axis_applied': i,
                    'solution': current_solution
                })

                k += 1

        self.has_hash_table = True
        self.has_depth = depth
        print('Hash table (depth: %i; entries: %i) done in %fs' % (depth, k, time.time() - start_time))

    def solve(self, state, max_solutions=1):
        queue = deque()
        k = 0
        solutions = 0
        start_time = time.time()

        # create initial queue
        for i in range(2):
            for j in range(4):
                current_state = self.fast_turn(state, (i << 3) + j)
                current_solution = [(i << 3) + j]
                node = (current_state, i, current_solution)
                queue.append(node)

        while True:
            k += 1
            state, axis, prev_solution = queue.popleft()
            i = (axis + 1) & 1

            for j in range(4):
                current_state = state
                current_solution = list(prev_solution)

                # Apply move to current iteration
                move = (i << 3) + j

                current_state = self.fast_turn(current_state, move)
                current_solution.append(move)

                # Is solved?
                is_solved = self.is_solved(current_state)

                if not is_solved:
                    node = (current_state, i, current_solution)
                    queue.append(node)
                else:
                    end_time = time.time() - start_time
                    solution = self.get_algorithm(current_solution + is_solved)
                    solutions += 1
                    print('Found a solution #%i/%i in %f seconds\n%s (%i,%i moves)' %
                          (solutions,
                           max_solutions,
                           end_time,
                           solution['string'],
                           solution['turns'],
                           solution['fTurns']
                           )
                          )
                    if solutions >= max_solutions:
                        return {
                            'state': current_state,
                            'solution': solution
                        }

    def fast_turn(self, state, move):
        ep, cp, co = state
        surface = move >> 3
        length = (move % 4) + 1

        return (
                   self.ep_turn(ep, surface, length),
                   self.cp_turn(cp, surface, length),
                   self.co_turn(co, surface, length)
        )

    def ep_turn(self, state, surface, length):
        for i in range(length):
            state = self.ep_move_table[state][surface]
        return state

    def cp_turn(self, state, surface, length):
        for i in range(length):
            state = self.cp_move_table[state][surface]
        return state

    def co_turn(self, state, surface, length):
        for i in range(length):
            state = self.co_move_table[state][surface]
        return state

    def is_solved(self, state):
        if self.has_hash_table:
            hashed_state = self.get_hash_from_state(state)
            if hashed_state in self.hash_table:
                reverse_solution = self.hash_table[self.get_hash_from_state(state)]
                solution = self.get_move_string_from_solution(reverse_solution)
                # print('Found solution in hashtable', solution)
                return solution

        if state == self.solved_state:
            return [16]

        return False

    def apply_state(self, state):
        str_ep = ','.join([str(x) for x in state['ep']])
        state['ep'] = self.rev_ep_move_table[str_ep]
        self.state = state

    def apply_sequence(self, moves, state):
        moves = moves.split(' ')

        for move in moves:
            state = self.fast_turn(state, self.get_turn_from_string(move))

        return state

    def get_hash_from_state(self, state):
        ep, cp, co = state
        return (ep << 29) + (cp << 13) + co

    def get_algorithm(self, sequence):
        moves = 'UL*'
        postfix = ['', '2', '2\'', '\'']
        algorithm = {
            'string': '',
            'turns': 0,
            'fTurns': 0  # fifth turns
        }

        for move in sequence:
            if type(move) is not int:
                print(sequence, move, type(move))

            move = move
            i = move >> 3
            j = move & 3

            if i < 2:
                algorithm['string'] += moves[i] + postfix[j] + ' '
                algorithm['turns'] += 1
                algorithm['fTurns'] += int(((j + 1) % 4) / 2) + 1

        return algorithm

    def get_move_string_from_solution(self, hash_solution):
        solution = []

        for move in hash_solution[::-1]:
            i = move >> 3
            j = 3 - (move & 3)
            solution.append((i << 3) + j)

        return solution

    def get_turn_from_string(self, string):
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

    def get_state_from_state(self, state):
        state = (
            self.rev_ep_move_table[state['ep']],
            self.rev_cp_move_table[state['cp']],
            self.rev_co_move_table[state['co']]
        )
        return state

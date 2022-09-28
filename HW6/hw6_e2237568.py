# Arda Karaman 2237568

class StateProbablity:
    def __init__(self, name, start_probability, trans_prob, obs_prob, result_prob):
        self.name = name
        self.start_probability = start_probability
        self.trans_prob = trans_prob
        self.obs_prob = obs_prob
        self.result_prob = result_prob


class State:
    def __init__(self, name, prob):
        self.name = name
        self.prob = prob


class Transition:
    def __init__(self, start, goal, prob):
        self.start = start
        self.goal = goal
        self.prob = prob


class Observation:
    def __init__(self, start, goal, prob):
        self.start = start
        self.goal = goal
        self.prob = prob


def find_in_states_list(state_name, lis):
    for i in lis:
        if state_name == i.name:
            return i
    return None


def find_obs_in_states_list(obs_name, state: StateProbablity):
    for i in state.obs_prob:
        if obs_name == i[0]:
            return i[1]
    return 0


def find_stateprob_in_states_list(state_name, state: StateProbablity):
    for i in state.obs_prob:
        if state_name == i[0]:
            return i[1]
    return 0


def viterbi(problem_file_name):
    with open(problem_file_name, mode='r') as f:
        stateProbabilities = []
        states, start_probabilities, transition_probabilities, observation_probabilities, observations = False, False, False, False, False
        statesV, start_probabilitiesV, transition_probabilitiesV, observation_probabilitiesV, observationsV = [], [], [], [], []
        for line in f:
            line = line.removesuffix('\n')
            if line == '[states]':
                states = True
                continue
            if line == '[start probabilities]':
                start_probabilities = True
                continue
            if line == '[transition probabilities]':
                transition_probabilities = True
                continue
            if line == '[observation probabilities]':
                observation_probabilities = True
                continue
            if line == '[observations]':
                observations = True
                continue
            if states:
                statesV = line.split('|')
                stateProbabilities = [StateProbablity(x, 0, [], [], []) for x in statesV]
                states = False
                continue
            if start_probabilities:
                line = line.split('|')
                line = [x.split(":") for x in line]
                for sp in line:
                    find_in_states_list(sp[0], stateProbabilities).start_probability = float(sp[1])
                start_probabilities = False
                continue
            if transition_probabilities:
                line = line.split('|')
                line = [x.split(":") for x in line]
                for t in line:
                    names = t[0].split("-")
                    find_in_states_list(names[0], stateProbabilities).trans_prob.append((find_in_states_list(names[1], stateProbabilities), float(t[1])))
                transition_probabilities = False
                continue
            if observation_probabilities:
                line = line.split('|')
                line = [x.split(":") for x in line]
                for t in line:
                    names = t[0].split("-")
                    find_in_states_list(names[0], stateProbabilities).obs_prob.append((names[1], float(t[1])))
                observation_probabilities = False
                continue
            if observations:
                observationsV = line.split('|')
                observations = False
                continue

        firsts = []
        _state_probbs = []
        for state in stateProbabilities:
            state.result_prob.append(state.start_probability * find_obs_in_states_list(observationsV[0], state))
            argmax = state.result_prob[-1]
            highest = state
            firsts.append(([highest], argmax))

        i = 0
        _argmax = []
        _res_states = []
        _res_states_before_states = []
        for res_states, argmax in firsts:
            temp_dict = {}
            temp_dict_before_states = {}
            for obs in observationsV[1:]:
                temp_argmax = 0
                for state in res_states[-1].trans_prob:
                    temp = argmax * state[1] * find_obs_in_states_list(obs, state[0])
                    if state[0].name in temp_dict:
                        temp_dict.get(state[0].name).append(temp)
                        temp_dict_before_states.get(state[0].name).append(state[0].name)
                    else:
                        temp_dict.update({state[0].name: [temp]})
                        temp_dict_before_states.update({state[0].name: [state[0].name]})

                    state[0].result_prob.append(temp)
                    if temp_dict[state[0].name][-1] > temp_argmax:
                        temp_argmax = temp_dict.get(state[0].name)[-1]
                        highest = state[0]
                res_states.append(highest)
                argmax = temp_argmax
            _state_probbs.append(temp_dict)
            _res_states.append(res_states)
            _res_states_before_states.append(temp_dict_before_states)
            _argmax.append(argmax)
            i += 1

    state_probabilities = {}
    state_sequence = []
    for s in stateProbabilities:
        i = 0
        for i in range(len(observationsV)):
            if i == 0:
                state_probabilities.update({s.name: [s.result_prob[i]]})
            else:
                h = 0
                a = 0
                for j in range(len(_state_probbs)):
                    if _state_probbs[j][s.name][i-1] > h:
                        h = _state_probbs[j][s.name][i-1]
                        a = j
                state_probabilities[s.name].append(h)

    sequence_probability = 0
    last_state = ""
    for tm in state_probabilities.keys():
        if state_probabilities[tm][-1] > sequence_probability:
            sequence_probability = state_probabilities[tm][-1]
            last_state = tm

    for j in range(len(observationsV)):
        # j += 1
        h = 0
        seq = ""
        for i in state_probabilities.keys():
            if state_probabilities[i][j] > h:
                h = state_probabilities[i][j]
                seq = i
        state_sequence.append(seq)

    return state_sequence, sequence_probability, state_probabilities


# print(viterbi("inputOutput/process1.txt"))

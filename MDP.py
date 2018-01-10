import numpy as np
import pandas as pd

class MDP(object):
    def __init__(self, actions, learning_rate=0.9, reward_decay=0.9, greedy=0.9):
        self.actions = actions
        self.learning_rate = learning_rate
        self.gamma = reward_decay
        self.greedy = greedy
        self.q_table = pd.DataFrame(columns = self.actions, dtype=np.float64)

    def choose_action(self, state):
        self.check_state_exist(state)
        if np.random.uniform() < self.greedy:
            state_action = self.q_table.ix[state, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
            action = state_action.idxmax()
        else:
              # choose random action
            action = np.random.choice(self.actions)
        return action
 
    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def learn(self, *args):
        pass


class QLearning(MDP):

    def __init__(self, actions, learning_rate=0.9, reward_decay=0.9, greedy=0.9):
        super(QLearning, self).__init__(actions, learning_rate, reward_decay, greedy)

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_old = self.q_table.ix[s, a]
        if s_ != 'terminal':
            q_new = - r - self.gamma * self.q_table.ix[s_, :].max()
        else:
            q_new = r
        self.q_table.ix[s, a] += self.learning_rate * (q_new - q_old)


class Sarsa(MDP):

    def __init__(self, actions, learning_rate=0.9, reward_decay=0.9, greedy=0.9):
        super(Sarsa, self).__init__(actions, learning_rate, reward_decay, greedy)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_old = self.q_table.ix[s, a]
        if s_ != 'terminal':
            q_new = -(r + self.gamma * self.q_table.ix[s_, :].max())
        else:
            q_new = r
        self.q_table.ix[s, a] += self.learning_rate * (q_new - q_old)


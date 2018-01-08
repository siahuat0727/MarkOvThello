import numpy as np
import pandas as pd

class MDPTable:
    def __init__(self, actions, learning_rate=0.9, greedy=0.9):
        self.actions = actions
        self.learning_rate = learning_rate
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
 
    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_old = self.q_table.ix[s, a]
        if s_ != 'terminal':
            q_new = r + self.q_table.ix[s_, :].max()  # next state is not terminal
        else:
            q_new = r
        self.q_table.ix[s, a] += self.learning_rate * (q_new - q_old)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

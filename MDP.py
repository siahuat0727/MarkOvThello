import numpy as np
import pandas as pd
import random

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
 
    def choose_possible_action(self, state, pos_can_go_s):
        self.check_state_exist(state)
        if not pos_can_go_s:
            return (-1, -1), [0]
        pos_can_go_value_s = self.q_table.ix[state, pos_can_go_s]
        before_reindex = pos_can_go_value_s
        for i, j in zip(before_reindex, pos_can_go_value_s):
            if i != j:
                print("sth wrong after reindex before if!!!!!!!!!!!!!!")
                return
        if np.random.uniform() < self.greedy:
            # print(pos_can_go_s)
            # print('\n'.join("%s: %s" % item for item in attrs.items()))
    
            state_action = pos_can_go_value_s.reindex(np.random.permutation(pos_can_go_value_s.index))     # some actions have same value
            action = state_action.idxmax()
            for i, j in zip(before_reindex, pos_can_go_value_s):
                if i != j:
                    print("sth wrong after reindex!!!!!!!!!!!!!!")
                    return
        else:
            # choose random action
            action = random.choice(pos_can_go_s)
        return action, pos_can_go_value_s
 
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
            q_new = - (r + self.gamma * self.q_table.ix[s_, :].max())
        else:
            q_new = r
        self.q_table.ix[s, a] += self.learning_rate * (q_new - q_old)

    def othello_learn(self, s, a, r, s_, pos_can_go_s):
        self.check_state_exist(s_)
        if a == (-1, -1):
            return
        q_old = self.q_table.ix[s, a]
        if s_ != 'terminal':
            if not pos_can_go_s:
                s__ = s_[:-1] + str(int(s_[-1]) ^ 1)
                self.check_state_exist(s__)
                q_new = - r + self.gamma * self.q_table.ix[s__, :].max()
            else:
                q_new = - (r + self.gamma * self.q_table.ix[s_, pos_can_go_s].max())
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


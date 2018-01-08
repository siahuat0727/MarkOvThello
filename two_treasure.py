from qlearning import MDPTable
import numpy as np
import pandas as pd
import time

np.random.seed(3)  # reproducible


N_STATES = 7   # the length of the 1 dimensional world
INIT_STATE = N_STATES // 2
ACTIONS = ['left', 'right', 'stay']     # available actions
EPSILON = 0.9   # greedy police
ALPHA = 0.1     # learning rate
GAMMA = 0.9    # discount factor
MAX_EPISODES = 13   # maximum episodes
FRESH_TIME = 0.1    # fresh time for one move
A_TREASURE = 0
B_TREASURE = N_STATES - 1


def get_env_feedback(S, A, player):
    # This is how agent will interact with the environment
    if A == 'left' and int(S[0]) > A_TREASURE:  
        S_ = str(int(S[0])-1) + player
    elif A == 'right' and int(S[0]) < B_TREASURE:
        S_ = str(int(S[0])+1) + player
    else:
        S_ = S[0] + player

    if int(S_[0]) == A_TREASURE or int(S_[0]) == B_TREASURE:
        if player == 'A' and int(S_[0]) == A_TREASURE:
            R = 1
        else:
            R = -1
        S_ = 'terminal'
    else:
        R = 0

    return S_, R

def update_env(S, episode, step_counter, player, win_lose=''):
    # This is how environment be updated
    env_list = ['A'] + ['-']*(N_STATES-2) + ['B']   # '---------T' our environment
    if S == 'terminal':
        interaction = 'Episode %s: total_steps = %s ' % (episode+1, step_counter) + win_lose
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                                  ', end='')
    else:
        env_list[int(S[0])] = 'a' if player == 'A' else 'b'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)

def rl(start_player='A', change_player=False):
    # main part of RL loop
    table = MDPTable(ACTIONS)
    for episode in range(MAX_EPISODES):
        player = start_player 
        step_counter = 0
        S = str(INIT_STATE) + player
        is_terminated = False
        update_env(S, episode, step_counter, player)
        while not is_terminated:
            S = ''.join(S[0] + player)
            A = table.choose_action(S)
            S_, R = get_env_feedback(S, A, player)  # take action & get next state and reward
            table.learn(S, A, R, S_)
            S = S_  # move to next state
            win_lose = player + ' '
            win_lose += 'win' if R == 1 else 'lose'
            update_env(S, episode, step_counter+1, player, win_lose)
            if S_ == 'terminal':
                is_terminated = True
            step_counter += 1
            player = 'A' if player == 'B' else 'B'

        print('\n', table.q_table.sort_index(axis=0), end='\n\n')
    return table

if __name__ == "__main__":
    q_table = rl()
    print('\r\nQ-table:\n')
    print(q_table)

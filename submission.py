import numpy as np
import time
import random
def t_items(l):
    
    max_touch = 0
    touch = 0
    
    for i in range(len(l)-1):
        
        if (l[i+1]-1) == l[i]:
            touch += 1
            
        else:
            max_touch = max(touch,max_touch)
            touch = 0
    
    max_touch = max(touch,max_touch)
            
    return max_touch
def eval_move(obs, conf, player):
    
    opposite_player = {1:2,
                       2:1}
    
    otherplayer = opposite_player[player]
    
    arr = np.reshape(obs["board"], (conf["rows"], conf["columns"]))
    
    diags = [arr [::-1,:].diagonal(i) for i in range(-3,4)]
    diags.extend(arr.diagonal(i) for i in range(3,-4,-1))
    
    boardscore = 0
    score_lines = [arr, arr.T, diags]
    
    for direction in score_lines:
        for line in direction:

            t_p = t_items(np.where(line == player)[0])
            t_e = t_items(np.where(line == otherplayer)[0]) 
            o_items = set(range(len(line))).difference(set(np.where(line == otherplayer)[0]))


            if len(o_items) > 1 and 0 in o_items:
                o_items.remove(0)

            if len(o_items) > 1 and len(line)-1 in o_items:
                o_items.remove(len(line)-1)

            for o_item in o_items:
                if o_item in np.where(line == player)[0]:
                    boardscore += 25
            
            if len(o_items)>= 3:
             
                
                if list(o_items)[0]-1 in np.where(line == player)[0]:
                    boardscore+=95
                    
                if list(o_items)[-1]+1 in np.where(line == player)[0]:
                    boardscore+=95
                    
                
                
            

            if t_p >= 3:
                boardscore += 750
            
            if t_p >= 1:
                boardscore += 5

            if t_e >= 1:
                boardscore -= 5

            if t_e >= 3:
                boardscore -= 1000
   
    return boardscore
def get_moves(obs, conf):
    arr = np.reshape(obs["board"], (conf["rows"], conf["columns"]))
    open_moves = np.where(arr == 0)
    
    possible_moves = {}
    
    for move in list(zip(list(open_moves[0]), list(open_moves[1]))):
        
        if move[1] in possible_moves:
            if move[0] > possible_moves[move[1]][0]:
                possible_moves[move[1]] = move
                
        else:
            possible_moves[move[1]] = move
        
    return list(possible_moves.values())
def simulate_move(obs, conf, player, move):
    
    nboard = obs.copy()
    
    arr = np.reshape(nboard["board"], (conf["rows"], conf["columns"]))
    arr[move[0]][move[1]] = player
    nboard["board"] = arr.flatten()
    
    return nboard
def score_moves(obs, conf, depth, my_turn, alpha, beta):

    depth = depth - 1
    
    opposite_player = {1:2,
                       2:1}
    
    my_player = obs["mark"]
    
    if my_turn == True:
        moving_player = my_player
       
        pmoves = get_moves(obs, conf)
        scores = []

        for pmv in pmoves:
            new_obs = simulate_move(obs, conf, moving_player, pmv)
            

            score = (pmv, eval_move(new_obs, conf, my_player))
            if depth > 0:
                score = (pmv, score_moves(new_obs, conf, depth, (not my_turn), alpha, beta)[1])

            scores.append(score)
            if score[1] >= beta:
                break;
            alpha = max(score[1], alpha)

        if len(scores) > 0:
            movescore = max(scores, key=lambda m:m[1])

        else:
            movescore = (None, float("-inf"))

    if my_turn == False:
        moving_player = opposite_player[obs["mark"]]
       
        omoves = get_moves(obs, conf)
        scores = []

        for omv in omoves:
            new_obs = simulate_move(obs, conf, moving_player, omv)

            score = (omv, eval_move(new_obs, conf, my_player))
            if depth > 0:
                score = (omv, score_moves(new_obs, conf, depth, (not my_turn), alpha, beta)[1])

            scores.append(score)
            if score[1] <= alpha:
                break;

            beta = min(score[1], beta)

        if len(scores) > 0:
            movescore = min(scores, key=lambda m:m[1])

        else:
            movescore = (None, float("inf"))
    return movescore
def mm_ab(obs, conf, depth, my_turn):

    alpha = float("-inf")
    beta = float("inf")

    best = score_moves(obs, conf, depth, my_turn, alpha, beta)

    return best
def minimax_alpha_beta(obs, conf, depth):

    best_val = 0
    level = 1
    best_move = random.choice(get_moves(obs, conf))
    start = time.time()
    
    while (time.time() - start ) < conf["timeout"]/50:
        
        result = mm_ab(obs, conf, level, True)
        best_move, best_val = result

        level = level + 1
        if level > depth:
            break;

    return best_move, best_val, level
def my_agent(observation, configuration):
  
    best_move = minimax_alpha_beta(observation, configuration, depth = 10)
    converted_move = int(best_move[0][1])
    #print(best_move)
    #k == 1
  
    
    
    return converted_move

"""Student agent: edit ONLY this file."""
from agents.agent import Agent
from store import register_agent
from constants import *
import numpy as np
import time
from helpers import (Move, get_valid_moves, execute_move, check_winner,
                     check_endgame, random_move, copy_state, top_view, LINES)


class StopSearch(Exception):    
    pass

@register_agent("student_agent")          # do not change this string
class StudentAgent(Agent):

    def __init__(self):
        """Set up your agent. This runs once per game, before the first move, and must finish
        within INIT_TIME_LIMIT seconds."""
        super().__init__()
        self.name = "StudentAgent"
        self.DEPTHLIMIT = 3
        self.WINVALUE = 1000000
        self.startTime = 0


    def checkSearch(self): 
        if time.perf_counter() > 1.6 + self.startTime: 
            raise StopSearch()

    def evaluate(self,board, player, opponent):
        owners, size = top_view(board)
        total = 0 
        for win in LINES[WIN_LENGTH]: 
            p = 0 
            o = 0
            playermult = 1 
            opponentmult = 1
            add = 0 
            sub = 0 
            if any(owners[r][c] == OBSTACLE for (r, c) in win):
                continue
            for (r,c) in win: 
                if owners[r][c] == player: 
                    #int8 array to small causing overflow
                    playermult += int(size[r][c])
                    p += 1 
                if owners[r][c] == opponent: 
                    o += 1 
                    opponentmult += int(size[r][c])


            if p==2: 
                add +=1 
            elif p==3: 
                add += 10 
            add*=playermult
            if o == 2: 
                sub -= 1
            elif o == 3: 
                sub -= 10
            sub*=opponentmult
            total += add + sub
                
        return total




    def maxValue(self, board,a,b, depth, reserves, player,opponent):
        self.checkSearch() 
        if  depth == self.DEPTHLIMIT: 
            return self.evaluate(board, player, opponent)
        for move in get_valid_moves(board,reserves,player):
            nboard, nreserves = copy_state(board, reserves)
            execute_move(nboard, nreserves, player, move)
            winner = check_winner(nboard, player)
            if winner == player: 
                return self.WINVALUE - depth
            elif winner == opponent: 
                val =  -1 * (self.WINVALUE - depth)
                a = max(a,val)
            else:  
                a = max(a, self.minValue(nboard, a,b,depth+1, nreserves, player,opponent))
            if a>=b: 
                return b
            
        return a; 

    def minValue(self, board, a,b, depth, reserves, player, opponent):
        self.checkSearch() 
        if depth == self.DEPTHLIMIT: 
            return self.evaluate(board, player, opponent)
        for move in get_valid_moves(board,reserves,opponent):
            nboard, nreserves = copy_state(board, reserves)
            execute_move(nboard, nreserves, opponent, move)
            winner = check_winner(nboard, opponent)
            if winner == player: 
                val =  self.WINVALUE - depth
                b = min(b, val)
            elif winner == opponent: 
                return  -1 * (self.WINVALUE - depth)

            else:  
        
                b = min(b, self.maxValue(nboard, a,b,depth + 1, nreserves, player, opponent))
         
            if a>=b: 
                return a
            
        return b; 



        
                
    def startSearch(self, board, reserves, player, opponent): 
            self.checkSearch()
            bestMove = None 
            bestval = float('-inf')
            for move in get_valid_moves(board,reserves,player):
                nboard, nreserves = copy_state(board, reserves)
                execute_move(nboard, nreserves, player, move)
                winner = check_winner(nboard, player)
                if winner == player: 
                    return move
                elif winner == opponent: 
                    val = -self.WINVALUE
                else:  
                    val =  self.minValue(nboard,float('-inf'), float('inf'), 1, nreserves, player,opponent) 
                    if val> bestval: 
                        bestMove = move 
                        bestval = val
    
            if bestMove == None: 
                return random_move(board,reserves,player)

            return bestMove

        



    def step(self, board, reserves, player, opponent):
        """Return the Move you want to play.

        Takes: board, reserves - your own copies of the current position.
               player, opponent - your player number (1 or 2) and the other one.
        Agent.step in agents/agent.py explains each argument and the time limit.
        """
        self.startTime = time.perf_counter()
        # ALLOW_MOVES and WIN_LENGTH (from constants) are the rule flags of this game.
        # helpers.get_valid_moves / check_winner already respect them; your own
        # move generator and evaluation function must too.
        # TODO: replace with your search. Keep (time.perf_counter() - start) < STEP_TIME_LIMIT - margin.
        bestMove = None 
        for d in range(2,10): 
            self.DEPTHLIMIT = d
            try:
                bestMove = self.startSearch( board, reserves, player, opponent)
            except StopSearch: 
                break
  
    
        return bestMove

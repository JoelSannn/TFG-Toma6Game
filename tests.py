# Author: Joel Sánchez de Murga Pacheco
# TFG: Desenvolupament d’una aplicació del joc de cartes ¡Toma 6! incloent agents intel·ligents com a jugadors
# Year: 2023-24

from controller.controller import *
from PyGame.PyGame import *
import tensorflow as tf
import os
import logging

# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging (must be set before importing TensorFlow)
tf.get_logger().setLevel(logging.ERROR)
logging.getLogger('tensorflow').setLevel(logging.ERROR)

if __name__ == "__main__":    
    while True:
        try:
            numPlayers = int(View.inputMsg('How many players do you want to face? (1-9) '))
            if numPlayers in range(1, 10):
                break
            else:
                View.printMsg('Error: Number of players out of range.')
        except ValueError:
            View.printMsg('Error: Please enter a valid number.')
    iterations = int(input("How many iterations?  "))

    wins = 0
    p0 = []
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    
    for _ in range(iterations):
        # 1 - Easy
        # 2 - Medium
        # 3 - Hard
        # 4 - Expert
        players = [Player('Player0', True, 4)]
        for i in range(numPlayers):
            #players.append(Player('Player' + str(i+1), True, 2, typeBot=2))
            players.append(Player('Player' + str(i+1), True, 1))
            game = Game(players)
        game.game()
                
        if game.winner=='Player0':
                wins += 1
                
        p0.append(players[0].points)
        p1.append(players[1].points)
        p2.append(players[2].points)
        p3.append(players[3].points)
        p4.append(players[4].points)
        
                    
    print("###################### RESULTS ########################")
    print("If each player has the same probability to win, Player0 will get ", iterations//(numPlayers+1), " wins")
    print("Player0 has win ", wins, " games")
    print("It gives a ratio of ", wins/(iterations/(numPlayers+1)))
    
    print()
    print(f'wins: {wins}\np0: {sum(p0)/iterations}\np1: {sum(p1)/iterations}\np2: {sum(p2)/iterations}\np3: {sum(p3)/iterations}\np4: {sum(p4)/iterations}')
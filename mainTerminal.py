# Author: Joel Sánchez de Murga Pacheco
# TFG: Desenvolupament d’una aplicació del joc de cartes ¡Toma 6! incloent agents intel·ligents com a jugadors
# Year: 2023-24

from controller.controller import *
from PyGame.PyGame import *

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
    
    player1 = View.inputMsg('What\'s your name? ')
    players = [Player(player1, False, 0)]
    #players = [Player(player1, True, 2)]
    for i in range(numPlayers):
        if i == 0:
            players.append(Player('Bot' + str(i), True, 3))
        else:
            players.append(Player('Bot' + str(i), True, 1))

    game = Game(players)
    game.game()
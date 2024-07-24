# Author: Joel Sánchez de Murga Pacheco
# TFG: Desenvolupament d’una aplicació del joc de cartes ¡Toma 6! incloent agents intel·ligents com a jugadors
# Year: 2023-24

import numpy as np
from model.model import *
from neural_network.data_processing import preprocess_state
from view.view import *
from os import system
import sys

# Directory for log files
log_dir = 'logs'

# Create the directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Create log files
stdout_log = os.path.join(log_dir, 'stdout.log')
stderr_log = os.path.join(log_dir, 'stderr.log')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging

sys.stdout = open(stdout_log, 'w')
sys.stderr = open(stderr_log, 'w')

class Game():
    # Initialize all the variables
    def __init__(self, players) -> None:
        # Number of players
        self.players = players
        
        # Deck
        self.deck = Deck()
        self.deck.shuffleDeck()
        
        # Table
        self.table = self.setTable()
                
    def setTable(self) -> Table:
        """Set the first four cards of the table

        Returns:
            Table: The table with the four cards
        """
        # Get the 4 cards
        tableCards = []
        for _ in range(4):
            tableCards.append(self.deck.dealCard())
        
        # Sort them from lower to bigger and save them in arrays
        tableCards = sorted(tableCards, key=lambda Card: Card.value) 
        tableGame = [[tableCards[0]], [tableCards[1]], [tableCards[2]], [tableCards[3]]]
        
        return Table(tableGame)
    
    def chooseCard(self, player) -> list:
        """Choose a card to play in each turn

        Args:
            player (Player): The player

        Returns:
            list (Card, Player): The card played and the player
        """
        chosen_card = 0
        # Turn of the real player
        if not player.bot:
            View.printMsg(f"##################  {player.name}'s turn ({player.points} points)    ##################")
            # Show the table status
            View.showTable(self.table)
                        
            # Choose a card
            View.showHand(player.cards)
            while True:
                try:   
                    i = int(View.inputMsg('Choose a card to play:   '))
                    if i in range(len(player.cards)):
                        break
                    else:
                        View.printMsg('Error: Index out of range.')
                except ValueError:
                    View.printMsg('Error: Please enter a valid number.')

            chosen_card = i
        else:
            # Turn of the bots
            if player.difficulty == 2: # Medium
                card = player.tree_decision(self.table, self.deck, self.players, 3)
                i = 0
                chosen_card = 0
                for c in player.cards:
                    if c.value == card.value:
                        chosen_card = i
                    i+=1                
            
            elif player.difficulty == 1: # Easy
                if player.typeBot == 0: # Less to Biggest card
                    chosen_card = 0
                
                elif player.typeBot == 1: # Random
                    i = random.randint(0, len(player.cards) - 1)
                    chosen_card = i
                
                elif player.typeBot == 2: # Biggest to less card
                    chosen_card = len(player.cards) - 1
            elif player.difficulty == 3: # Hard
                i = player.mcts_decision(self.table, self.deck, self.players, 200)
                chosen_card = i
            elif player.difficulty == 4:  # New Difficulty using the model
                game_state = self.getGameState()
                preprocessed_state, player_card_indices = preprocess_state(game_state)
                preprocessed_state = np.expand_dims(preprocessed_state, axis=0)  # Add batch dimension
                predictions = player.model.predict(preprocessed_state)[0]  # Get the predictions for the batch

                player_card_indices = [c.value for c in player.cards]
                # Filter the predictions to only consider the player's cards
                player_card_predictions = predictions[player_card_indices]
                chosen_card = np.argmax(player_card_predictions)
                #chosen_card = player_card_indices[chosen_card_index]
                '''print(predictions)
                print(player_card_indices)
                print(player_card_predictions)
                print(chosen_card)'''
                
        # Save the state and action to the dataset
        game_state = self.getGameState()
        #self.saveStateAction(game_state, player.cards[chosen_card])

        return [player.playCard(chosen_card), player]
        
    def checkWinner(self) -> tuple[bool, str, int]:
        """Check if some player has alredy reach 66 points or more

        Returns:
            tuple[bool, str, int]: If the game ends or not, the winner and his points
        """
        end = False
        winner = None
        points = 999999
        for p in self.players:
            # If someone has 66 or more points, the game ends
            if p.points >= 66:
                end = True
            # In case the game ends here we can get the winner
            if p.points < points:
                winner = p.name
                points = p.points
                self.winner = winner
        return end, winner, points
    
    def resetRound(self) -> None:
        """Reset the round, we get a new deck and new table
        """
        # Get a new deck and a new table
        self.deck = Deck()
        self.deck.shuffleDeck()
        self.table = self.setTable()
    
    # Neural Network
    def getGameState(self):
        """Get the current state of the game."""
        # Create a representation of the game state
        state = {
            'table': [[card.value for card in row] for row in self.table.cards],  # Flatten the table cards into a 2D list of card values
            'players': [
                {
                    'name': p.name,  # Player's name
                    'cards': [card.value for card in p.cards],  # List of card values the player holds
                    'points': p.points,  # Player's current points
                    'bot': p.bot  # Boolean indicating if the player is a bot
                } for p in self.players  # Iterate over each player and collect their information
            ]
        }
        return state  # Return the created state representation

    def saveStateAction(self, state, action):
        """Save the game state and action to a file or database."""
        # Implement your preferred method of saving data, e.g., append to a CSV file
        with open('neural_network/data/game_data.csv', 'a') as f:
            # Write the state and action to the CSV file in the format: state;action
            f.write(f"{state};{action.value}\n")
            
    # The game loop
    def game(self):
        """The game loop
        """
        end = False
        while not end:            
            # Give 10 cards to each player
            for p in self.players:
                p.cards = []
                for _ in range(10):
                    p.getCard(self.deck.dealCard())
                    
            # First we play 10 turns
            for turn in range(10):
                # Each player choose a card
                cardsPlayed = []
                for p in self.players:
                    # Clean the terminal
                    #system("cls")
                    # Save the played card in an array
                    cardsPlayed.append(self.chooseCard(p))
                    
                # Once all players had played a card, we put them in the table in order from lower to bigger
                cardsPlayed = sorted(cardsPlayed, key=lambda x: x[0].value)
                for c in cardsPlayed:
                    bulls = self.table.playCard(c[0], c[1], self.table)
                    c[1].points += bulls
            # Once the 10 rounds are played we check if someone has lost already
            end, winner, points = self.checkWinner()
            
            # We reset the deck and table for a new round
            self.resetRound()
                    
        # Show the results
        #View.showWinner(self.players, winner, points)
        os.remove(stdout_log)
        os.remove(stderr_log)
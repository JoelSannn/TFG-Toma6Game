# Author: Joel Sánchez de Murga Pacheco
# TFG: Desenvolupament d’una aplicació del joc de cartes ¡Toma 6! incloent agents intel·ligents com a jugadors
# Year: 2023-24

import math
import random
import copy
from typing import Union
from view.view import *
from tensorflow.keras.models import load_model
import os
import sys


# The value of each card with the number of bulls
VALUE_BULL = [(1, 1), (2,1), (3,1), (4,1),(5,2),(6,1),(7,1),(8,1),(9,1),(10,3),
              (11, 5), (12,1), (13,1), (14,1),(15,2),(16,1),(17,1),(18,1),(19,1),(20,3),
              (21, 1), (22,5), (23,1), (24,1),(25,2),(26,1),(27,1),(28,1),(29,1),(30,3),
              (31, 1), (32,1), (33,5), (34,1),(35,2),(36,1),(37,1),(38,1),(39,1),(40,3),
              (41, 1), (42,1), (43,1), (44,5),(45,2),(46,1),(47,1),(48,1),(49,1),(50,3),
              (51, 1), (52,1), (53,1), (54,1),(55,7),(56,1),(57,1),(58,1),(59,1),(60,3),
              (61, 1), (62,1), (63,1), (64,1),(65,2),(66,5),(67,1),(68,1),(69,1),(70,3),
              (71, 1), (72,1), (73,1), (74,1),(75,2),(76,1),(77,5),(78,1),(79,1),(80,3),
              (81, 1), (82,1), (83,1), (84,1),(85,2),(86,1),(87,1),(88,5),(89,1),(90,3),
              (91, 1), (92,1), (93,1), (94,1),(95,2),(96,1),(97,1),(98,1),(99,5),(100,3),
              (101, 1), (102,1), (103,1), (104,1)
              ]

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Table class
class Table():
    def __init__(self, cards) -> None:
        # All the cards that are in the table
        self.cards = cards
    
    # Play a card to the table        
    def playCard(self, card, player, table) -> int: # 0 - ok, another number - number of bulls
        """Play a card to the table

        Args:
            card (Card): The card to be played
            player (Player): The player that plays the card
            table (Table): The table

        Returns:
            int: Number of bulls the player will get
        """
        # We get the row with the least difference between the last card and the played card
        index = 0
        diff = 105
        i = 0
        for row in table.cards:
            lastCard = row[-1]
            difference = card.value - lastCard.value
            if (difference > 0):
                if diff > difference:
                    diff = difference
                    index = i
            
            i += 1
        # If we cannot put the card we choose a row or we get the row with leasts bulls
        if diff == 105:
            # Turn of the real player
            if not player.bot:
                View.showTable(table)
                while True:
                    try:
                        index = int(View.inputMsg(f"{player.name} choose a row:    "))
                        if index in range(len(table.cards)):
                            break
                        else:
                            View.printMsg('Error: Index out of range.')
                    except ValueError:
                        View.printMsg('Error: Please enter a valid number.')
            else:
                # Turn of the bots                
                # Check which row has more and less bulls
                biggest = 0
                biggestBull = 0
                leasts = 0
                leastsBull = 99
                index = 0
                for row in table.cards:
                    bull = 0
                    for i in row:
                        bull += i.bull
                    
                    if biggestBull < bull:
                        biggestBull = bull
                        biggest = index
                    if leastsBull > bull:
                        leastsBull = bull
                        leasts = index
                    index += 1
                            
                if player.difficulty == 1: # Easy, get the biggest amount of bulls
                    index = biggest
                elif player.difficulty == 2: # Medium, get random index
                    index = random.randint(0, len(table.cards) - 1)
                elif player.difficulty == 3 or player.difficulty == 4: # Hard, get the leats amount of bulls
                    index = leasts
            
            bulls = 0
            for c in table.cards[index]:
                bulls += c.bull
            table.cards[index] = [card]
            return bulls
            
        # We check if the row is full
        if len(table.cards[index]) == 5:
            # if it's full we sum all the bulls and give to the player
            bulls = 0
            for c in table.cards[index]:
                bulls += c.bull
            table.cards[index] = [card]
            return bulls
        # If not we play the card
        table.cards[index].append(card)
        return 0
        
    def copy(self):
        return Table(copy.deepcopy(self.cards))
            
            
# Card class
class Card():
    def __init__(self, value, bull, brightness = 0) -> None:
        # Value of the card
        self.value = value
        # Number of bulls of the card
        self.bull = bull
        self.brightness = brightness
        
    def __eq__(self, other):
        return self.value == other.value and self.bull == other.bull
    
    def __hash__(self):
        return hash((self.value, self.bull))
    
# Deck class
class Deck():
    def __init__(self) -> None:
        # All the cards
        self.numCards = [Card(i[0], i[1]) for i in VALUE_BULL]
        
    # Sort randomly
    def shuffleDeck(self) -> None:
        """Sort randomly
        """
        random.shuffle(self.numCards)
        
    # Play the first card of the deck
    def dealCard(self) -> Union[None, Card]:
        """Play the first card of the deck

        Returns:
            Union[None, Card]: Returns the first card of the deck or None if it's empty
        """
        if len(self.numCards) > 0:
            return self.numCards.pop(0)
        else:
            return None
    
    def removeCards(self, cards):
        for card in cards:
            for c in self.numCards:
                if card.value == c.value:
                    self.numCards.remove(c)
        
    def copy(self):
        return Deck(list(self.numCards))
        
# Player class
class Player():
    def __init__(self, name, bot, diff, cards = [], points = 0, typeBot = 0, winRound=None, pointsRound=None) -> None:
        # Player name
        self.name = name
        # The cards that the player has
        self.cards = cards
        # The points that the player has
        self.points = points
        # If it's a bot or not
        self.bot = bot
        # The difficulty of the bot (0 - human / 1 - easy / 2 - medium / 3 - hard)
        self.difficulty = diff
        # The type of difficulty of the bot
        if self.difficulty == 1:
            self.typeBot = random.randint(0, 2)
        else:
            self.typeBot = typeBot
        # Number of rounds wins
        self.winRound = winRound if winRound is not None else []
        # Points by round
        self.pointsRound = pointsRound if pointsRound is not None else []
        # Model
        if self.difficulty == 4:
            self.load_model()
        
    def copy(self):
        return Player(self.name, self.bot, self.difficulty, list(self.cards), points=self.points)
        
    # Get a card from the deck
    def getCard(self, card) -> None:
        """Get a card from the deck

        Args:
            card (Card): The card the player will get
        """
        self.cards.append(card)
        self.cards = sorted(self.cards, key=lambda Card: Card.value) 
      
    # Play a card to the table
    def playCard(self, i) -> Card:
        """Play a card to the table

        Args:
            i (int): The index of the card

        Returns:
            Card: The card that the player will play
        """
        if i < len(self.cards):
            return self.cards.pop(i)
        else:
            View.printMsg("Index out of range")
            return None
    
    # Tree Decision    
    class Node:
        """A node from the tree
        """
        def __init__(self, card=None, cards=None, row=None, points=0, table=None, deck=None, parent=None, visits=None) -> None:
            self.card = card
            self.cards = cards
            self.row = row
            self.points = points
            self.nodes = []
            self.table = table
            self.deck = deck
            self.parent = parent
            self.visits = visits

    def tree_decision(self, table, deck, players, count) -> Card:
        """The first step of creating the decision tree.
        
        This method initiates the decision tree search.
        
        Args:
            table (Table): The current state of the game table.
            deck (Deck): The deck of cards.
            players (list): The list of players in the game.
            count (int): The number of iterations to perform.

        Returns:
            Card: The card that the AI decides to play.
        """
        # Initialize the root node
        root = self.Node()
        root.cards = list(self.cards)
        root.table = copy.deepcopy(table)
        deck = Deck()

        # Remove the player's cards from the deck
        deck.removeCards(root.cards)

        # Remove the table's cards from the deck
        for row in root.table.cards:
            deck.removeCards(row)

        root.deck = deck

        # Seek for each card which is the best position
        for card in root.cards:
            # Find the best position for each card
            best_card_played, best_row = self.find_best_position(root.table, card)

            if best_card_played:
                # Calculate points for the chosen card and row
                points = self.calculate_points(best_card_played, best_row)
                # Create a node for the decision tree
                node = self.Node(card=best_card_played, cards=best_row, points=points)
                # Generate the subtree for the current node
                self.generate_subtree(node, root.cards, deck, root.table, players, count)
                root.nodes.append(node)

        # Choose the best path in the decision tree
        path = self.choose_best_path(root)
        return path[1].card if len(path) > 1 else self.cards[0]

    def find_best_position(self, table, card):
        """Find the best position to play a card on the table.

        Args:
            table (Table): The current state of the game table.
            card (Card): The card to be played.

        Returns:
            tuple: The best card to play and the corresponding row.
        """
        best_card_played = None
        best_row = None
        min_difference = float('inf')

        for row in table.cards:
            # Check if the card can be played in this row
            if card.value > row[-1].value:
                difference = card.value - row[-1].value
                if difference < min_difference:
                    min_difference = difference
                    best_card_played = card
                    best_row = row

        return best_card_played, best_row
    
    def calculate_points(self, card, row) -> int:
        """Calculate the points that the node has.

        Args:
            card (Card): The card being played.
            row (list): The row where the card will be played.

        Returns:
            int: The points of the node.
        """
        points = 0
        if len(row) == 5:
            # If the row is full, sum up the bull points of each card
            for card in row:
                points += card.bull
        return points

    def generate_subtree(self, node, cards, deck, table, players, count) -> None:
        """Generate a new node on the decision tree.

        Args:
            node (Node): The current node.
            cards (list): The cards of the player.
            deck (Deck): The deck.
            table (Table): The table.
            players (list): List of players.
            count (int): Number of iterations to perform.
        """
        table = copy.deepcopy(table)

        cards.remove(node.card)
        for r in table.cards:
            if r == node.row:
                r.append(node.card)

        deck_players = Deck()
        deck_players.numCards = [card for player in players for card in player.cards]

        for card in cards:
            if card in deck_players.numCards:
                deck_players.numCards.remove(card)

        for _ in range(len(players) - 1):
            card = random.choice(deck_players.numCards)
            row_index = self.find_best_position(table, card)
            for r in table.cards:
                if r == row_index:
                    r.append(card)

        for card in cards:
            best_card_played, best_row = self.find_best_position(table, card)

            if best_card_played:
                points = self.calculate_points(best_card_played, best_row)
                node_sec = self.Node(card=best_card_played, cards=best_row, points=points)
                if count != 0:
                    self.generate_subtree(node_sec, cards, deck, table, players, count - 1)
                node.nodes.append(node_sec)

    def choose_best_path(self, node, actual_path=[], best_paths=[[], [], [], []], best_points=[float('inf')]*4) -> list:
        """Seeks the decision tree and gets the best path.

        Args:
            node (Node): The current node.
            actual_path (list, optional): The current path. Defaults to [].
            best_paths (list, optional): The list of best paths. Defaults to [[]]*4.
            best_points (list, optional): The list of points for the best paths. Defaults to [float('inf')]*4.

        Returns:
            list: The best path.
        """
        actual_path.append(node)

        if not node.nodes:
            # If it's a leaf node, update best paths if necessary
            actual_points = sum(n.points for n in actual_path)
            for i, points in enumerate(best_points):
                if actual_points < points:
                    best_points.insert(i, actual_points)
                    best_paths.insert(i, actual_path[:])
                    best_points.pop()
                    best_paths.pop()
                    break

        for sub_node in node.nodes:
            self.choose_best_path(sub_node, actual_path, best_paths, best_points)

        actual_path.pop()

        return best_paths[self.typeBot]
            
    # MCTS (MonteCarlo)
    def simulation(self, node, table, deck, players):
        """
        Perform a single simulation in the Monte Carlo Tree Search.

        Args:
            node (Node): The current node in the MCTS tree.
            table (Table): The current table state.
            deck (Deck): The current deck state.
            players (list): The list of all players in the game.
        """
        # Find the index of the current player
        current_player_index = next((i for i, p in enumerate(players) if p.name == self.name), None)
        if current_player_index is None:
            return  # Player not found, exit simulation

        current_player = players[current_player_index]
        current_table = copy.deepcopy(table)
        current_players = [player.copy() for player in players]

        # Iterate until we have done 5 rounds or the player empties their deck
        node_parent = node
        for _ in range(3):
            # Randomize the order of players' turns
            random.shuffle(current_players)

            # Iterate over each player and choose a random card from their hand to play
            for player in current_players:
                if not player.cards:
                    continue  # Player's deck is empty, move to the next player
                player.difficulty = 2
                player.bot = True
                # Choose a random card from the player's hand and play it
                card = random.choice(player.cards)
                player.cards.remove(card)
                bulls = current_table.playCard(card, player, current_table)
                player.points += bulls

            # Create a child node and add it to the current node's children
            child_node = self.Node(card=card, parent=node_parent, visits=1)
            child_node.points = current_player.points
            node_parent.nodes.append(child_node)
            node_parent = child_node

        # Backpropagate the reward to update the values of nodes in the MCTS tree
        self.backpropagation(child_node, current_player.points)

    def mcts_decision(self, table, deck, players, simulations):
        """
        Use Monte Carlo Tree Search to make a decision on the best move.

        Args:
            table (Table): The current table state.
            deck (Deck): The current deck state.
            players (list): The list of all players in the game.
            simulations (int): The number of simulations to run.

        Returns:
            Card: The card that the player decides to play.
        """
        # Create the root node for the MCTS tree
        root = self.Node(visits=0)

        # Run simulations to build the tree and choose the best move
        for _ in range(simulations):
            # Create a copy of the current game state for each simulation
            sim_table = copy.deepcopy(table)
            sim_deck = copy.deepcopy(deck)
            sim_players = [player.copy() for player in players]

            # Perform a simulation starting from the root node
            self.simulation(root, sim_table, sim_deck, sim_players)

        # Choose the best move based on the MCTS tree
        best_child = self.select_best_child(root)
        return next((i for i, c in enumerate(self.cards) if c.value == best_child.card.value), 0)

    def backpropagation(self, node, reward):
        """
        Backpropagate the reward from a simulated game to update node values in the MCTS tree.

        Args:
            node (Node): The current node in the MCTS tree.
            reward (int): The reward obtained from the simulated game.
        """
        # Update the value of the current node based on the reward
        node.points += reward
        node.visits += 1  # Increment visits for the node

        # Recursively backpropagate the reward to parent nodes
        if node.parent is not None:
            self.backpropagation(node.parent, reward)
            
    def ucb1(self, node):
        """
        Calculate the Upper Confidence Bound (UCB1) for a given node.

        Args:
            node (Node): The node for which to calculate UCB1.

        Returns:
            float: The UCB1 value for the node.
        """
        if node.visits == 0:
            return float('inf')
        exploitation = node.points / node.visits
        exploration = math.sqrt(2 * math.log(node.parent.visits) / node.visits)
        
        # Increase the weight of the exploration term
        return exploitation + 2.0 * exploration  # Adjust the coefficient as needed

    def select_best_child(self, node):
        """
        Select the best child node based on UCB1 value.

        Args:
            node (Node): The parent node whose children to evaluate.

        Returns:
            Node: The best child node according to UCB1.
        """
        # Shuffle the list of nodes to introduce randomness
        random.shuffle(node.nodes)
        return max(node.nodes, key=self.ucb1)
   
   # Neural Network
    def load_model(self):
        self.model = load_model(resource_path('neural_network/game_model.h5'))

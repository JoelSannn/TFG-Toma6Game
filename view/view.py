# Author: Joel Sánchez de Murga Pacheco
# TFG: Desenvolupament d’una aplicació del joc de cartes ¡Toma 6! incloent agents intel·ligents com a jugadors
# Year: 2023-24

class View():    
    
    # Print a message
    def printMsg(msg) -> None:
        """Print a message

        Args:
            msg (str): The message to be printed
        """
        print(msg)
      
    # Input a message  
    def inputMsg(msg) -> str:
        """Inputs a message

        Args:
            msg (str): The message to be printed

        Returns:
            str: The input result
        """
        return input(msg)
    
    # Show the table status
    def showTable(table) -> None:
        """Show the table status

        Args:
            table (Table): The Table variable
        """
        print('##################   Table Status    ##################')
        index = 0
        for row in table.cards:
            print(f"({index})", end=' | ')
            bull = 0
            for i in row:
                print(f"{i.value}", end= ' | ')
                bull += i.bull
                    
            print(f"({bull} bulls)")
            index += 1
    
    # Show the hand of the player
    def showHand(cards) -> None:
        """Show the hand of the player

        Args:
            cards (list): The cards that the player has
        """
        print('##################   Your Deck   ##################')
        i = 0
        for c in cards:
            print(f"({i}) Card value: {c.value}, Number of bulls: {c.bull}")
            i += 1

    # Show the results of the game
    def showWinner(players, winner, points) -> None:
        """Show the results of the game

        Args:
            players (list): All the players
            winner (str): The name of the winner
            points (int): The points of the winner
        """
        for p in players:
            print(f"{p.name} has {p.points} points.")
        print('##############################################')
        print(f"The winner is {winner} with {points} points.")
# Author: Joel Sánchez de Murga Pacheco
# TFG: Desenvolupament d’una aplicació del joc de cartes ¡Toma 6! incloent agents intel·ligents com a jugadors
# Year: 2023-24

from PIL import Image, ImageDraw, ImageFont
import numpy as np
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
    iterations = int(input("How many iterations?  "))

    a = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
    b = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
    
    # Initialize nested dictionary to store win counts
    win_counts = {}
    for difficulty1 in [1, 2, 3, 4]:
        for difficulty2 in [1, 2, 3, 4]:
            win_counts[(difficulty1, difficulty2)] = {'wins': 0, 'total': 0}
                
    for diff in range(16):
        wins = 0
        gameNumber = 0
        for _ in range(iterations):
            print(f"Game number {gameNumber}/{iterations} - Turn of player {a[diff]} - Turn of enemy {b[diff]}")
            players = [Player('Player0', True, a[diff])]
            for i in range(numPlayers):
                players.append(Player('Player' + str(i+1), True, b[diff], typeBot=2))
            game = Game(players)
            game.game()
            
            # Update win counts
            if game.winner == 'Player0':
                win_counts[(players[0].difficulty, players[1].difficulty)]['wins'] += 1
            win_counts[(players[0].difficulty, players[1].difficulty)]['total'] += 1


            if game.winner == 'Player0':
                wins += 1
            gameNumber += 1

    # Create confusion matrix
    print("Confusion Matrix:")
    print("{:<10} {:<10} {:<10} {:<10} {:<10}".format('Difficulty', 'Easy', 'Medium', 'Hard', 'Expert'))  # Adjusted print statement
    for difficulty1 in [1, 2, 3, 4]:
        row = []
        for difficulty2 in [1, 2, 3, 4]:
            win_count = win_counts[(difficulty1, difficulty2)]
            row.append(f"{win_count['wins']}/{win_count['total']}")
        print("{:<10} {:<10} {:<10} {:<10} {:<10}".format(difficulty1, *row))

    # Create confusion matrix data
    conf_matrix_data = np.zeros((4, 4))  # Initialize the matrix with zeros
    for i, difficulty1 in enumerate([1, 2, 3, 4]):
        for j, difficulty2 in enumerate([1, 2, 3, 4]):
            win_count = win_counts[(difficulty1, difficulty2)]
            conf_matrix_data[i, j] = win_count['wins'] / win_count['total']

    # Create image
    image_size = (600, 600)
    image = Image.new('RGB', image_size, color='white')
    draw = ImageDraw.Draw(image)

    # Define cell size and padding
    cell_width = image_size[0] // 6
    cell_height = image_size[1] // 6
    padding = 5

    # Define font
    font = ImageFont.load_default()

    # Draw confusion matrix
    for i, label in enumerate(['Easy', 'Medium', 'Hard', 'Expert']):
        draw.text((cell_width * (i + 1.5), cell_height), label, fill='black', font=font)
        draw.text((cell_width, cell_height * (i + 1.5)), label, fill='black', font=font)

    for i in range(4):
        for j in range(4):
            x0 = (j + 1) * cell_width
            y0 = (i + 1) * cell_height
            x1 = (j + 2) * cell_width - padding
            y1 = (i + 2) * cell_height - padding
            draw.rectangle([x0, y0, x1, y1], outline='black')
            text = f"{conf_matrix_data[i, j]:.2f}"
            text_width, text_height = draw.textsize(text, font=font)
            draw.text(((x0 + x1 - text_width) / 2, (y0 + y1 - text_height) / 2), text, fill='black', font=font)

    # Save image
    image.save('img/confusion_matrix.png')

    # Display the image
    #image.show()
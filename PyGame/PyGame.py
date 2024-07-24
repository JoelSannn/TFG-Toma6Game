# Author: Joel Sánchez de Murga Pacheco
# TFG: Desenvolupament d’una aplicació del joc de cartes ¡Toma 6! incloent agents intel·ligents com a jugadors
# Year: 2023-24

import pygame
from pygame.locals import *
from controller.controller import *
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font, text_color, border_radius=20):
        # Initialize the button with the given parameters
        self.text = text  # The text displayed on the button
        self.rect = pygame.Rect(x, y, width, height)  # The rectangular area representing the button's position and size
        self.color = color  # The default color of the button
        self.hover_color = hover_color  # The color of the button when hovered over
        self.font = font  # The font used to render the button's text
        self.text_color = text_color  # The color of the button's text
        self.border_radius = border_radius  # The radius of the button's border corners

    def draw(self, screen, mouse_pos):
        # Draw the button on the screen
        if self.rect.collidepoint(mouse_pos):  # Check if the mouse is hovering over the button
            color = self.hover_color  # Use the hover color
        else:
            color = self.color  # Use the default color
        
        # Draw the button rectangle
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        
        # Render the text and center it on the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen

class PlayerButton:
    def __init__(self, player, x, y, width, height, font, text_color, bg_color, hover_color, border_radius=20):
        # Initialize the player button with the given parameters
        self.player = player  # The player associated with the button
        self.rect = pygame.Rect(x, y, width, height)  # The rectangular area representing the button's position and size
        self.font = font  # The font used to render the button's text
        self.text_color = text_color  # The color of the button's text
        self.hover_color = hover_color  # The color of the button when hovered over
        self.bg_color = bg_color  # The default background color of the button
        self.text = f"{player.name} - {player.points} points"  # The text displayed on the button
        self.border_radius = border_radius  # The radius of the button's border corners

    def draw(self, screen, mouse_pos):
        # Draw the player button on the screen
        if self.rect.collidepoint(mouse_pos):  # Check if the mouse is hovering over the button
            color = self.hover_color  # Use the hover color
        else:
            color = self.bg_color  # Use the default background color
        
        # Draw the button rectangle
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        
        # Render the text and position it slightly inset from the top-left corner of the button
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))  # Blit the text surface onto the screen

    def is_clicked(self, mouse_pos):
        # Check if the button is clicked (mouse position within button bounds)
        return self.rect.collidepoint(mouse_pos)

class PygameGame():
    def __init__(self) -> None:
        """Initialize global variables"""
        # Initialize PyGame
        pygame.init()
        
        # Initialize screen attributes
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # Create the game window
        pygame.display.set_caption('¡Toma 6! Game')  # Set the window title
        
        # Initialize clock, running variable, and fonts
        self.clock = pygame.time.Clock()  # Create a clock object to manage the frame rate
        self.running = True  # Boolean to control the game loop
        self.font = pygame.font.Font(resource_path('font/Aceh-Light.ttf'), 48)  # Main font for buttons
        self.small_font = pygame.font.Font(resource_path('font/Aceh-Light.ttf'), 32)  # Smaller font for additional text
        self.letters_font = pygame.font.Font(resource_path('font/Aceh-Light.ttf'), 20)  # Font for smaller text elements
        
        # Initialize some variables for the configuration
        self.hint = False  # Toggle for hint display
        self.showRow = False  # Toggle for row display
        
        # Initialize background images
        self.bg_menu_image = pygame.image.load(resource_path('img/bg_menu2.jpg'))  # Load the menu background image
        self.bg_menu_image = pygame.transform.scale(self.bg_menu_image, (self.screen_width, self.screen_height))  # Scale to fit screen
        self.bg_game_image = pygame.image.load(resource_path('img/bg_game1.jpg'))  # Load the game background image
        self.bg_game_image = pygame.transform.scale(self.bg_game_image, (self.screen_width, self.screen_height))  # Scale to fit screen
        
        # Initialize images
        self.punctuation_image = pygame.image.load(resource_path('img/punctuation.png'))  # Load an image for punctuation display
        self.punctuation_image = pygame.transform.scale(self.punctuation_image, (300, 300))  # Scale image to desired size
        
        # Create a mask for the punctuation image
        mask = pygame.Surface((300, 300), pygame.SRCALPHA)  # Create a new surface with alpha transparency
        pygame.draw.circle(mask, (255, 255, 255, 255), (150, 150), 200)  # Draw a filled circle on the mask
        self.punctuation_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Apply the mask to the image
        
        # Save the cards images
        self.cardImages = []
        for i in range(104):
            temp = pygame.image.load(resource_path(f'img/card/{i+1}.png'))
            temp =  pygame.transform.scale(temp, (75, 100))
            self.cardImages.append(temp)

    def user(self):
        # Set input box properties
        input_box_width = 300
        input_box_height = 40
        input_box_color_inactive = pygame.Color('lightskyblue3')  # Color when inactive
        input_box_color_active = (212, 152, 74)  # Color when active
        input_box_font = pygame.font.Font(None, 32)  # Font for input box text
        
        # Initialize input box states
        name_input_active = True  # Name input is active by default
        players_input_active = False  # Players input is inactive by default
        name_input_text = ''  # Initial text for name input
        players_input_text = ''  # Initial text for players input
        
        # Initialize buttons
        continue_button = Button("Continue", self.screen_width // 8 * 5.5, self.screen_height - 60, 200, 50,
                                (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))  # Continue button
        continue_button_active = False  # Continue button is inactive by default
        return_menu_button = Button("Return back", self.screen_width // 8 * 0.5, self.screen_height - 60, 300, 50,  # Enlarge button
                                    (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))  # Return back button
        
        while True:
            self.screen.blit(self.bg_menu_image, (0, 0))  # Draw the background image
            mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position

            for event in pygame.event.get():  # Event handling loop
                if event.type == pygame.QUIT:  # If the window is closed
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # If a mouse button is pressed
                    if continue_button_active and continue_button.rect.collidepoint(mouse_pos):  # If continue button is clicked
                        self.players(name_input_text, players_input_text)
                    elif return_menu_button.rect.collidepoint(mouse_pos):  # If return menu button is clicked
                        return
                    elif pygame.Rect(200, 200, input_box_width, input_box_height).collidepoint(event.pos):  # Name input box clicked
                        name_input_active = True
                        players_input_active = False
                    elif pygame.Rect(200, 300, input_box_width, input_box_height).collidepoint(event.pos):  # Players input box clicked
                        name_input_active = False
                        players_input_active = True
                elif event.type == pygame.KEYDOWN:  # If a key is pressed
                    if event.key == pygame.K_RETURN:  # If Enter key is pressed
                        name_input_active = not name_input_active
                        players_input_active = not players_input_active
                    elif name_input_active:  # Handle name input
                        if event.key == pygame.K_BACKSPACE:
                            name_input_text = name_input_text[:-1]
                        elif len(name_input_text) < 15:
                            name_input_text += event.unicode
                    elif players_input_active:  # Handle players input
                        if event.key == pygame.K_BACKSPACE:
                            players_input_text = players_input_text[:-1]
                        elif event.unicode.isdigit() and len(players_input_text) < 1 and event.unicode != '0':
                            players_input_text += event.unicode

            # Draw background boxes for text labels
            self.draw_text_box('Intro: Change the text box', self.screen_width // 8 * 0.5 + 10, self.screen_height - 90, input_box_font)

            # Draw input boxes with combined prompt and input text
            self.render_input_box(200, 200, 'Enter your name (max 15 characters):', name_input_text, name_input_active, input_box_width, input_box_height, input_box_color_active, input_box_color_inactive, input_box_font)
            self.render_input_box(200, 300, 'Enter number of players (1-9):', players_input_text, players_input_active, input_box_width, input_box_height, input_box_color_active, input_box_color_inactive, input_box_font)

            continue_button_active = name_input_text.strip() != '' and players_input_text.strip() != ''  # Activate continue button if inputs are valid
                    
            if continue_button_active:
                continue_button.draw(self.screen, mouse_pos)  # Draw the continue button
                    
            return_menu_button.draw(self.screen, mouse_pos)  # Draw the return menu button
            
            pygame.display.flip()  # Update the display

    def players(self, name_input_text, players_input_text):
        initPlayers = True  # Flag to initialize players
        difficulty_buttons = []  # List to store difficulty buttons
        button_width = 130
        button_height = 30
        gap = 20  # Gap between buttons
        box_padding = 5  # Padding for the background box
        total_width = button_width * 4 + gap * 3  # Total width for arranging buttons
        continue_button_players = Button("Continue", self.screen_width // 8 * 5.5, self.screen_height - 60, 200, 50,
                                        (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))  # Continue button
        active_button = False  # Flag to check if any button is active
        return_back_button = Button("Return back", self.screen_width // 8 * 0.5, self.screen_height - 60, 300, 50,  # Enlarge button
                                    (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))  # Return back button
        
        while True:
            self.screen.blit(self.bg_menu_image, (0, 0))  # Draw the background image
            mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position

            for event in pygame.event.get():  # Event handling loop
                if event.type == pygame.QUIT:  # If the window is closed
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # If a mouse button is pressed
                    if return_back_button.rect.collidepoint(mouse_pos):  # If return back button is clicked
                        return
                    elif active_button and continue_button_players.rect.collidepoint(mouse_pos):  # If continue button is clicked
                        self.runGame(name_input_text, players_difficulty)
                    for button in difficulty_buttons:  # Handle difficulty button clicks
                        if button.rect.collidepoint(mouse_pos):
                            player_index = difficulty_buttons.index(button) // 4  # Determine the player index (4 buttons per player now)
                            players_difficulty[player_index] = button.text  # Set the difficulty for the player
                            for btn in difficulty_buttons:
                                if player_index == difficulty_buttons.index(btn) // 4:
                                    if btn.text == button.text:
                                        btn.color = pygame.Color('tan4')  # Highlight the selected button
                                    else:
                                        btn.color = pygame.Color(212, 152, 74)  # Reset color for non-selected buttons
                            break
                            
            if initPlayers:
                initPlayers = False
                active_button = True
                players_difficulty = ['Easy' for _ in range(int(players_input_text))]  # Initialize difficulties
                start_x = (self.screen_width - total_width) // 2  # Calculate start position for buttons
                start_y = (self.screen_height - (button_height + gap) * int(players_input_text)) // 2  # Calculate start position for buttons
                for i in range(int(players_input_text)):
                    for j, difficulty in enumerate(['Easy', 'Medium', 'Hard', 'Expert']):  # Create difficulty buttons for each player
                        x = start_x + j * (button_width + gap) + 10
                        y = start_y + i * (button_height + gap)
                        color = pygame.Color('tan4') if difficulty == 'Easy' else pygame.Color(212, 152, 74)  # Set initial button color
                        button = Button(difficulty, x, y, button_width, button_height, color, (70, 130, 180), self.small_font, pygame.Color('white'))
                        difficulty_buttons.append(button)
                            
            for button in difficulty_buttons:
                button.is_hovered = button.rect.collidepoint(mouse_pos)  # Check if button is hovered
                button.draw(self.screen, mouse_pos)  # Draw the button
                    
            for i in range(int(players_input_text)):
                # Render the player name text to get its size
                name_text = self.small_font.render(f"Bot {i+1}", True, pygame.Color('white'))
                name_rect = name_text.get_rect(topleft=(start_x - 70, start_y + i * (button_height + gap)))
                
                # Calculate the background box size and position
                box_rect = pygame.Rect(
                    name_rect.left - box_padding,
                    name_rect.top - box_padding,
                    name_rect.width + box_padding * 2,
                    name_rect.height + box_padding * 2
                )
                
                # Draw the background box
                pygame.draw.rect(self.screen, pygame.Color(212, 152, 74), box_rect, border_radius=20)
                
                # Draw the player name text on top of the box
                self.screen.blit(name_text, name_rect)
                
            continue_button_players.draw(self.screen, mouse_pos)  # Draw the continue button
            return_back_button.draw(self.screen, mouse_pos)  # Draw the return back button
                
            pygame.display.flip()  # Update the display

    def tutorial0(self):
        text = (
            "This is the design of the cards, the black number is the value of the card and the red number on the bottom is the points that the card will give you.\n"
            "In each game, you will have 10 cards in your hand at the start of the round and 4 cards on the table, one for each row. You will play one card in each turn after you will play all the cards.\n"
            "Once the round is finished, it will review if someone has 66 points or more to finish the game. If not, it will play another round."
        )
        
        # Initialize 1st tutorial
        continue_button = Button("Continue", self.screen_width // 8 * 5, self.screen_height // 8 * 5, 200, 50,
                                (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))
        explanation_button = Button("Explanation", self.screen_width // 8 * 5, self.screen_height // 8 * 4, 250, 50,
                                    (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))
        self.show_explanation = False  # Use self.show_explanation as a class attribute
        
        players = [Player('User', False, 0), Player('Tutorial Bot', True, 1)]
        self.game = Game(players)
        self.game.table.cards = [[Card(20, 3)], [Card(40, 3)], [Card(70, 3)], [Card(90, 3)]]
        self.game.players[0].cards = [Card(22, 5), Card(37, 1), Card(52, 1), Card(55, 7), Card(57, 1), Card(74, 1), Card(87, 1), Card(98, 1), Card(100, 3), Card(104, 1)]
        self.game.players[1].cards = [Card(101, 1)]
        self.rowPlayer = False

        
        while True:
            self.screen.blit(self.bg_game_image, (0, 0))  # Draw the background image
            mouse_pos = pygame.mouse.get_pos()
            
            # Iterate over all pygame events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if explanation_button.rect.collidepoint(mouse_pos):
                            self.show_explanation = True
                        elif continue_button.rect.collidepoint(mouse_pos):
                            self.tutorial1()

            # Display the cards
            self.drawDeckPlayer()
            self.drawTable()
            
            # Draw the explanation button
            explanation_button.draw(self.screen, mouse_pos)
            continue_button.draw(self.screen, mouse_pos)
            
            # Show the explanation pop-up
            if self.show_explanation:
                self.show_explanation_popup(text)
            
            pygame.display.flip()
        
    def tutorial1(self):
        # Initialize the explanation
        # Define the text
        text = (
            "In this 1st tutorial we will explain to you how to play a card to the table.\n"
            "If your card value is greater than any last card of any row in the table, you can play the card.\n"
            "But you can only play it on the row with the least difference between the points of your card and the card of the table."
        )
                
        # Initialize 1st tutorial
        continue_button = Button("Continue", self.screen_width // 8 * 5, self.screen_height - 60, 200, 50,
                                (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))
        explanation_button = Button("Explanation", self.screen_width // 8 * 5, self.screen_height // 8 * 5, 250, 50,
                                    (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))
        active_button = False
        self.show_explanation = False  # Use self.show_explanation as a class attribute

        players = [Player('User', False, 0), Player('Tutorial Bot', True, 1)]
        self.game = Game(players)
        
        self.game.table.cards = [[Card(20, 1)], [Card(40, 1)], [Card(70, 1)], [Card(90, 1)]]
        self.game.players[0].cards = [Card(57, 1)]
        self.game.players[1].cards = [Card(101, 1)]
        
        phase = 'Choose'
        self.choosePlayer = True
        self.rowPlayer = False
        self.cardIndex = None
        self.row = None
        self.rowAssigned = False
        nextStep = False
        
        while True:
            self.screen.blit(self.bg_game_image, (0, 0))  # Draw the background image
            mouse_pos = pygame.mouse.get_pos()
            
            # Iterate over all pygame events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if explanation_button.rect.collidepoint(mouse_pos):
                            self.show_explanation = True
                        elif active_button and continue_button.rect.collidepoint(mouse_pos):
                            self.tutorial2()
                        if self.choosePlayer:
                            for i, card in enumerate(self.game.players[0].cards):
                                cardRect = pygame.Rect(30 + 76 * i, 460, 75, 100)
                                if cardRect.collidepoint(mouse_pos):
                                    self.cardIndex = i
                                    break
                        elif self.rowPlayer:
                            for i, row in enumerate(self.game.table.cards):
                                for j, card in enumerate(row):
                                    cardRect = pygame.Rect(60 + 76 * j, 25 + 101 * i, 75, 100)
                                    if cardRect.collidepoint(mouse_pos):
                                        self.row = i
                                        self.rowAssigned = True
                                        break
                                else:
                                    continue
                                break
                            
            if phase == 'Choose':
                if self.choosePlayer:
                    if self.cardIndex is not None:
                        cardsPlayed = [[self.game.players[0].playCard(self.cardIndex), self.game.players[0]]]
                        nextStep = True
                        self.choosePlayer = False
                if nextStep:
                    for i in range(1, len(self.game.players)):
                        cardsPlayed.append(self.game.chooseCard(self.game.players[i]))
                    cardsPlayed = sorted(cardsPlayed, key=lambda x: x[0].value)
                    phase = 'Play'
                    nextStep = False
            
            if phase == 'Play':
                if not self.rowPlayer:
                    cardsBefore = []
                    i = 0
                    for card in cardsPlayed:
                        if card[1] != self.game.players[0]:
                            cardsBefore.append(card)
                        else:
                            cardPlayer = card
                            break
                        i += 1
                    cardsPlayed = cardsPlayed[i + 1:]
                
                if not self.rowPlayer:
                    for c in cardsBefore:
                        bulls = self.playCard(c[0], c[1], self.game.table)
                        c[1].points += bulls
                    cardsBefore = []
                
                if not self.rowPlayer:
                    bulls = self.playCard(cardPlayer[0], cardPlayer[1], self.game.table)
                    if bulls == -1:
                        self.rowPlayer = True
                    else:
                        cardPlayer[1].points += bulls
                else:
                    if self.rowAssigned:
                        bulls = sum(c.bull for c in self.game.table.cards[self.row])
                        self.game.table.cards[self.row] = [cardPlayer[0]]
                        self.game.players[0].points += bulls
                        self.rowAssigned = False
                        self.rowPlayer = False
                
                if not self.rowPlayer:
                    for c in cardsPlayed:
                        bulls = self.playCard(c[0], c[1], self.game.table)
                        c[1].points += bulls
                    cardsPlayed = []
                    
                if len(cardsPlayed) == 0:
                    phase = 'Choose'
                    self.choosePlayer = True
                    self.cardIndex = None
                    active_button = True
            
            if len(self.game.players[0].cards) == 0:
                active_button = True
                continue_button.draw(self.screen, mouse_pos)
            
            # Display the cards
            self.drawDeckPlayer()
            self.drawTable()
            
            # Draw the explanation button
            explanation_button.draw(self.screen, mouse_pos)
            
            # Show the explanation pop-up
            if self.show_explanation:
                self.show_explanation_popup(text)
            
            pygame.display.flip()
    
    def tutorial2(self):
        # Initialize the explication
        # Define the text
        text = (
            "In this 2nd tutorial we will show you how works the action to play a card.\n "
            "If your card value is greater to any last card of any row in the table you can play the card.\n "
            "But you can only play it on the row with the least difference between the points of your card and the card of the table.\n"
            "A row is full when it has 5 cards, if the row you will play your card is full, you will get the points (bulls) of this row.\n"
            "Once you get all the cards of the row, the amount of points will be added to your punctuation, as you can see in the leaderboard.\n"
            "Hint: the idea os the game is to get the leasts points to win!"
        )
                
        # Initialize 1st tutorial
        continue_button = Button("Continue", self.screen_width // 8 * 5, self.screen_height - 60, 200, 50,
                                (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))
        explanation_button = Button("Explanation", self.screen_width // 8 * 5, self.screen_height // 8 * 5, 250, 50,
                                    (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))
        active_button = False
        self.show_explanation = False  # Use self.show_explanation as a class attribute
        
        players = [Player('User', False, 0), Player('Tutorial Bot', True, 1)]
        self.game = Game(players)
        
        self.game.table.cards = [[Card(20, 1), Card(24, 1), Card(27, 1), Card(30, 1)], 
                                 [Card(40,1), Card(50, 1), Card(51, 1), Card(53, 1), Card(54, 1)],
                                 [Card(70, 1), Card(75, 1), Card(78, 1), Card(84, 1), Card(85, 1)], 
                                 [Card(90,1), Card(97, 1), Card(98, 1), Card(100, 1)]]
        self.game.players[0].cards = [Card(57, 1)]
        self.game.players[1].cards = [Card(101, 1)]
        
        phase = 'Choose'
        self.choosePlayer = True
        self.rowPlayer = False
        self.cardIndex = None
        self.row = None
        self.rowAssigned = False
        nextStep = False
        
        while True:
            #self.screen.fill((30, 30, 30))  # Black color for background
            self.screen.blit(self.bg_game_image, (0, 0))  # Draw the background image
            mouse_pos = pygame.mouse.get_pos()

            # Iterate over all pygame events
            for event in pygame.event.get():
                # Check for quit event
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # Check for mouse button click event
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the left mouse button is clicked
                    if event.button == 1:
                        # Get the current mouse position
                        mouse_pos = pygame.mouse.get_pos()
                        if explanation_button.rect.collidepoint(mouse_pos):
                            self.show_explanation = True
                        # If it's time to choose a player
                        if self.choosePlayer:
                            # Iterate over each card in the player's hand
                            for i, card in enumerate(self.game.players[0].cards):
                                # Create a rectangle representing the card's area on the screen
                                cardRect = pygame.Rect(30 + 76 * i, 460, 75, 100)
                                # Check if the mouse click occurred within the card's rectangle
                                if cardRect.collidepoint(mouse_pos):
                                    # Store the index of the selected card
                                    self.cardIndex = i
                                    # Exit the loop since the card is selected
                                    break
                        # If it's time to choose a row
                        elif self.rowPlayer:
                            # Iterate over each row on the table
                            for i, row in enumerate(self.game.table.cards):
                                for j, card in enumerate(row):
                                    # Create a rectangle representing the card's area on the screen
                                    cardRect = pygame.Rect(60 + 76 * j, 25 + 101 * i, 75, 100)
                                    # Check if the mouse click occurred within the card's rectangle
                                    if cardRect.collidepoint(mouse_pos):
                                        # Store the index of the selected row
                                        self.row = i
                                        # Set a flag indicating that a row has been selected
                                        self.rowAssigned = True
                                        # Exit the loop since the row is selected
                                        break
                                else:
                                    # Continue to the next row if no card is selected in the current row
                                    continue
                                # Break the outer loop since a row is selected
                                break
                    if active_button and continue_button.rect.collidepoint(event.pos):
                        self.tutorial3()
            
            if phase == 'Choose':
                if self.choosePlayer:
                    if (self.cardIndex != None):
                        cardsPlayed = [[self.game.players[0].playCard(self.cardIndex), self.game.players[0]]]
                        nextStep = True
                        self.choosePlayer = False
                if nextStep:
                    for i in range(1, len(self.game.players)):
                        # Save the played card in an array
                        cardsPlayed.append(self.game.chooseCard(self.game.players[i]))
                    # Once all players had played a card, we put them in the table in order from lower to bigger
                    cardsPlayed = sorted(cardsPlayed, key=lambda x: x[0].value)
                    phase = 'Play'
                    nextStep = False
            
            if phase == 'Play':
                if not self.rowPlayer:
                    cardsBefore = []
                    i = 0
                    for card in cardsPlayed:
                        if card[1] != self.game.players[0]:
                            cardsBefore.append(card) # Save the cards that will be played before the player
                        else:
                            cardPlayer = card # The player card
                            break
                        i += 1
                    cardsPlayed = cardsPlayed[i + 1:] # Save the other cards
                
                if not self.rowPlayer:
                    for c in cardsBefore:
                        bulls = self.playCard(c[0], c[1], self.game.table)
                        c[1].points += bulls
                    cardsBefore = []
                
                # Hacer la parte del usuario
                if not self.rowPlayer:
                    bulls = self.playCard(cardPlayer[0], cardPlayer[1], self.game.table)
                    if bulls == -1:
                        self.rowPlayer = True
                    else:
                        cardPlayer[1].points += bulls
                else:
                    if self.rowAssigned:
                        bulls = 0
                        for c in self.game.table.cards[self.row]:
                            bulls += c.bull
                            
                        self.game.table.cards[self.row] = [cardPlayer[0]]
                        self.game.players[0].points += bulls
                        self.rowAssigned = False
                        self.rowPlayer = False
                
                if not self.rowPlayer: 
                    for c in cardsPlayed:
                        bulls = self.playCard(c[0], c[1], self.game.table)
                        c[1].points += bulls
                    cardsPlayed = []
                        
                if len(cardsPlayed) == 0:
                    phase = 'Choose'
                    self.choosePlayer = True
                    self.cardIndex = None
                    active_button = True
                
            if (len(self.game.players[0].cards) == 0):
                active_button = True
                continue_button.draw(self.screen, mouse_pos)
            
            # Display the cards
            self.drawDeckPlayer()
            self.drawTable()
            self.drawPoints()
            
            # Draw the explanation button
            explanation_button.draw(self.screen, mouse_pos)
            
            # Show the explanation pop-up
            if self.show_explanation:
                self.show_explanation_popup(text)
            
            pygame.display.flip()
         
    def tutorial3(self):
        # Initialize the explication
        # Define the text
        text = (
            "In this 3rd tutorial we will show you what happens if your card cannot fit in any row.\n "
            "If your card is lower than the last card of any row, you will have to choose any row to get their points.\n"
            "Hint: the idea os the game is to get the leasts points to win, in this case you can choose the row with leasts points!"
        )
        
        # Initialize 1st tutorial
        continue_button = Button("Continue", self.screen_width // 8 * 5, self.screen_height - 60, 200, 50,
                                (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))
        explanation_button = Button("Explanation", self.screen_width // 8 * 5, self.screen_height // 8 * 5, 250, 50,
                                    (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))
        active_button = False
        self.show_explanation = False  # Use self.show_explanation as a class attribute
        
        players = [Player('User', False, 0), Player('Tutorial Bot', True, 1)]
        self.game = Game(players)
        
        self.game.table.cards = [[Card(20, 1), Card(24, 1), Card(27, 1), Card(30, 1)], 
                                 [Card(40,1), Card(50, 1), Card(51, 1), Card(53, 1), Card(54, 1)],
                                 [Card(70, 1), Card(75, 1), Card(78, 1), Card(84, 1), Card(85, 1)], 
                                 [Card(90,1), Card(97, 1), Card(98, 1), Card(100, 1)]]
        self.game.players[0].cards = [Card(28, 1)]
        self.game.players[1].cards = [Card(101, 1)]
        
        phase = 'Choose'
        self.choosePlayer = True
        self.rowPlayer = False
        self.cardIndex = None
        self.row = None
        self.rowAssigned = False
        nextStep = False
        
        while True:
            #self.screen.fill((30, 30, 30))  # Black color for background
            self.screen.blit(self.bg_game_image, (0, 0))  # Draw the background image
            mouse_pos = pygame.mouse.get_pos()
            # Iterate over all pygame events
            for event in pygame.event.get():
                # Check for quit event
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # Check for mouse button click event
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the left mouse button is clicked
                    if event.button == 1:
                        # Get the current mouse position
                        mouse_pos = pygame.mouse.get_pos()
                        if explanation_button.rect.collidepoint(mouse_pos):
                            self.show_explanation = True
                        # If it's time to choose a player
                        if self.choosePlayer:
                            # Iterate over each card in the player's hand
                            for i, card in enumerate(self.game.players[0].cards):
                                # Create a rectangle representing the card's area on the screen
                                cardRect = pygame.Rect(30 + 76 * i, 460, 75, 100)
                                # Check if the mouse click occurred within the card's rectangle
                                if cardRect.collidepoint(mouse_pos):
                                    # Store the index of the selected card
                                    self.cardIndex = i
                                    # Exit the loop since the card is selected
                                    break
                        # If it's time to choose a row
                        elif self.rowPlayer:
                            # Iterate over each row on the table
                            for i, row in enumerate(self.game.table.cards):
                                for j, card in enumerate(row):
                                    # Create a rectangle representing the card's area on the screen
                                    cardRect = pygame.Rect(60 + 76 * j, 25 + 101 * i, 75, 100)
                                    # Check if the mouse click occurred within the card's rectangle
                                    if cardRect.collidepoint(mouse_pos):
                                        # Store the index of the selected row
                                        self.row = i
                                        # Set a flag indicating that a row has been selected
                                        self.rowAssigned = True
                                        # Exit the loop since the row is selected
                                        break
                                else:
                                    # Continue to the next row if no card is selected in the current row
                                    continue
                                # Break the outer loop since a row is selected
                                break
                    if active_button and continue_button.rect.collidepoint(event.pos):
                        self.menu()
            
            if phase == 'Choose':
                if self.choosePlayer:
                    if (self.cardIndex != None):
                        cardsPlayed = [[self.game.players[0].playCard(self.cardIndex), self.game.players[0]]]
                        nextStep = True
                        self.choosePlayer = False
                if nextStep:
                    for i in range(1, len(self.game.players)):
                        # Save the played card in an array
                        cardsPlayed.append(self.game.chooseCard(self.game.players[i]))
                    # Once all players had played a card, we put them in the table in order from lower to bigger
                    cardsPlayed = sorted(cardsPlayed, key=lambda x: x[0].value)
                    phase = 'Play'
                    nextStep = False
            
            if phase == 'Play':
                if not self.rowPlayer:
                    cardsBefore = []
                    i = 0
                    for card in cardsPlayed:
                        if card[1] != self.game.players[0]:
                            cardsBefore.append(card) # Save the cards that will be played before the player
                        else:
                            cardPlayer = card # The player card
                            break
                        i += 1
                    cardsPlayed = cardsPlayed[i + 1:] # Save the other cards
                
                if not self.rowPlayer:
                    for c in cardsBefore:
                        bulls = self.playCard(c[0], c[1], self.game.table)
                        c[1].points += bulls
                    cardsBefore = []
                
                # Hacer la parte del usuario
                if not self.rowPlayer:
                    bulls = self.playCard(cardPlayer[0], cardPlayer[1], self.game.table)
                    if bulls == -1:
                        self.rowPlayer = True
                    else:
                        cardPlayer[1].points += bulls
                else:
                    if self.rowAssigned:
                        bulls = 0
                        for c in self.game.table.cards[self.row]:
                            bulls += c.bull
                            
                        self.game.table.cards[self.row] = [cardPlayer[0]]
                        self.game.players[0].points += bulls
                        self.rowAssigned = False
                        self.rowPlayer = False
                
                if not self.rowPlayer: 
                    for c in cardsPlayed:
                        bulls = self.playCard(c[0], c[1], self.game.table)
                        c[1].points += bulls
                    cardsPlayed = []
                        
                if len(cardsPlayed) == 0:
                    phase = 'Choose'
                    self.choosePlayer = True
                    self.cardIndex = None
                    active_button = True
                
            if (len(self.game.players[0].cards) == 0):
                active_button = True
                continue_button.draw(self.screen, mouse_pos)
            
            # Display the cards
            self.drawDeckPlayer()
            self.drawTable()
            self.drawPoints()
            
            # Draw the explanation button
            explanation_button.draw(self.screen, mouse_pos)
            
            # Show the explanation pop-up
            if self.show_explanation:
                self.show_explanation_popup(text)
            
            pygame.display.flip()
         
    def config_menu(self):
        hint_rect = pygame.Rect(500, 150, 30, 30)
        table_hint_rect = pygame.Rect(500, 250, 30, 30)
        return_menu_button = Button("Return back", self.screen_width // 8 * 0.5, self.screen_height - 60, 300, 50,  # Enlarge button
                                    (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))
        
        while True:
            self.screen.blit(self.bg_menu_image, (0, 0))  # Draw the background image
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if hint_rect.collidepoint(event.pos):
                        self.hint = not self.hint
                    elif table_hint_rect.collidepoint(event.pos):
                        self.showRow = not self.showRow
                    elif return_menu_button.rect.collidepoint(event.pos):
                        return

            # Draw the options with background boxes
            self.draw_option_with_background(
                "Give hints", "Click 'H' to give a hint to what card is better to play, click 'K' to reset.", (100, 150), hint_rect, self.hint
            )
            
            self.draw_option_with_background(
                "Show table hints", "Hover a card in your hand and it will show where it will be placed on the table.", (100, 250), table_hint_rect, self.showRow
            )

            return_menu_button.is_hovered = return_menu_button.rect.collidepoint(mouse_pos)
            return_menu_button.draw(self.screen, mouse_pos)
            
            pygame.display.flip()
        
    def menu(self):
        ##################################   MENU    ##################################
        # Display the game title
        title_text = self.font.render("¡Toma 6! Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))

        # Create a background box for the title
        title_bg_rect = pygame.Rect(
            title_rect.left - 20, title_rect.top - 10,
            title_rect.width + 40, title_rect.height + 20
        )

        # Calculate button positions for better centering and spacing
        button_width, button_height = 200, 50
        button_spacing = 20  # Space between buttons
        total_height = button_height * 3 + button_spacing * 2  # Total height of all buttons plus spaces
        start_y = self.screen_height // 2 - total_height // 2  # Start position for the first button
        
        # Display buttons for starting the game and accessing configurations
        button_color = (212, 152, 74)  
        hover_color = (70, 130, 180)   # Steel Blue
        start_button = Button("Start", self.screen_width // 2 - button_width // 2, start_y, button_width, button_height,
                            button_color, hover_color, self.font, (255, 255, 255))
        config_button = Button("Options", self.screen_width // 2 - button_width // 2, start_y + button_height + button_spacing, button_width, button_height,
                            button_color, hover_color, self.font, (255, 255, 255))
        tutorial_button = Button("Tutorial", self.screen_width // 2 - button_width // 2, start_y + (button_height + button_spacing) * 2, button_width, button_height,
                                button_color, hover_color, self.font, (255, 255, 255))
        exit_button = Button("Exit", self.screen_width // 2 - button_width // 2, start_y + (button_height + button_spacing) * 3, button_width, button_height,
                                button_color, hover_color, self.font, (255, 255, 255))
        
        # Main menu loop
        while True:
            self.screen.blit(self.bg_menu_image, (0, 0))  # Draw the background image
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.rect.collidepoint(mouse_pos):
                        self.user()
                    elif config_button.rect.collidepoint(mouse_pos):
                        self.config_menu()
                    elif tutorial_button.rect.collidepoint(mouse_pos):
                        self.tutorial0()
                    elif exit_button.rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            # Draw everything
            pygame.draw.rect(self.screen, ('tan4'), title_bg_rect, border_radius=20)  # Draw the title background box
            self.screen.blit(title_text, title_rect)
            start_button.draw(self.screen, mouse_pos)
            config_button.draw(self.screen, mouse_pos)
            tutorial_button.draw(self.screen, mouse_pos)
            exit_button.draw(self.screen, mouse_pos)
            
            pygame.display.flip()
    
    def results(self):
        # Sort players by points to determine the winner
        winner = min(self.game.players, key=lambda p: p.points)

        player_buttons = []
        for i, p in enumerate(self.game.players):
            player_button = PlayerButton(p, 50, 100 + i * 50, 375, 40, self.small_font, (255, 255, 255), (212, 152, 74), (70, 130, 180))
            player_buttons.append(player_button)

        continue_button = Button("Continue", self.screen_width - 250, self.screen_height - 60, 200, 50,
                                (212, 152, 74), (70, 130, 180), self.font, (255, 255, 255))

        winner_text = f"Winner: {winner.name} - {winner.points} points"
        winner_surface = self.font.render(winner_text, True, (255, 255, 255))
        
        box_padding = 10  # Padding for the background box

        while True:
            #self.screen.fill((30, 30, 30))  # Black color for background
            self.screen.blit(self.bg_menu_image, (0, 0))  # Draw the background image
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.rect.collidepoint(event.pos):
                        self.menu()
                    for player_button in player_buttons:
                        if player_button.is_clicked(event.pos):
                            self.show_player_popup(player_button.player)

            # Calculate the position and size of the winner box
            winner_rect = winner_surface.get_rect(center=(self.screen_width // 2, 50))
            box_rect = pygame.Rect(
                winner_rect.left - box_padding,
                winner_rect.top - box_padding,
                winner_rect.width + box_padding * 2,
                winner_rect.height + box_padding * 2
            )

            # Draw the background box for the winner
            pygame.draw.rect(self.screen, pygame.Color('tan4'), box_rect, border_radius=20)

            # Draw the winner text at the top
            self.screen.blit(winner_surface, winner_rect.topleft)

            for player_button in player_buttons:
                player_button.draw(self.screen, mouse_pos)
            continue_button.draw(self.screen, mouse_pos)

            pygame.display.flip()
            
    def render_input_box(self, x, y, prompt, text, active, width, height, color_active, color_inactive, font):
        box_color = color_active if active else color_inactive
        prompt_surface = font.render(prompt, True, (255, 255, 255))
        text_surface = font.render(text, True, (0, 0, 0))

        # Calculate the total width and height for the combined prompt and input box
        combined_height = height + prompt_surface.get_height() + 10
        combined_width = max(width, prompt_surface.get_width() + 10)

        # Draw the background box for both prompt and input text
        combined_rect = pygame.Rect(x, y, combined_width + 10, combined_height + 10)
        pygame.draw.rect(self.screen, box_color, combined_rect, border_radius=15)

        # Draw the prompt text inside the combined box
        self.screen.blit(prompt_surface, (x + 5, y + 5))

        # Draw the input text box inside the combined box
        input_box = pygame.Rect(x + 5, y + 5 + prompt_surface.get_height() + 5, combined_width, height)
        pygame.draw.rect(self.screen, (255, 255, 255), input_box, border_radius=15)
        self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        
    def show_player_popup(self, player):
        popup_width, popup_height = 600, 200
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

        # Draw popup background
        pygame.draw.rect(self.screen, (30, 30, 30), popup_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, 2)  # White border

        # Titles and positions
        titles = [player.name] + [f"Round {i+1}" for i in range(len(player.winRound))]
        title_x_positions = [popup_x + 10 + i * 80 for i in range(len(titles))]

        # Render and draw titles
        self.render_and_draw_text(titles[0], title_x_positions[0], popup_y + 20, (255, 255, 255))
        for i, title in enumerate(titles[1:], 1):
            self.render_and_draw_text(title, title_x_positions[i], popup_y + 40, (255, 255, 255))

        # Render and draw points per round
        self.render_and_draw_text("Points", title_x_positions[0], popup_y + 80, (255, 255, 255))
        for i, points in enumerate(player.pointsRound):
            self.render_and_draw_text(str(points), title_x_positions[i + 1], popup_y + 80, (255, 255, 255))

        # Render and draw win/lose status per round
        self.render_and_draw_text("Status", title_x_positions[0], popup_y + 120, (255, 255, 255))
        for i, win in enumerate(player.winRound):
            status = "Win" if win else "Lose"
            self.render_and_draw_text(status, title_x_positions[i + 1], popup_y + 120, (255, 255, 255))

        pygame.display.flip()
        pygame.time.delay(3000)  # Display for 3 seconds

    def render_and_draw_text(self, text, x, y, color):
        text_surface = self.letters_font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def show_explanation_popup(self, text):
        """Display the explanation pop-up."""
        margin = 10  # Margin around the text inside the pop-up
        text_margin = 10  # Margin between the text and the edges of the pop-up
        line_spacing = 5  # Spacing between lines of text
        max_line_width = 500  # Maximum width of a single line of text
        button_height = 50  # Height of the button
        button_margin = 20  # Margin between the button and the text

        # Split the text into lines
        lines = text.split('\n')
        wrapped_lines = []

        # Split lines that are too long
        for line in lines:
            words = line.split(' ')
            current_line = ''
            for word in words:
                test_line = current_line + (word + ' ')
                if self.letters_font.size(test_line)[0] <= max_line_width:
                    current_line = test_line
                else:
                    wrapped_lines.append(current_line.strip())
                    current_line = word + ' '
            wrapped_lines.append(current_line.strip())

        # Render each line of text and determine the required dimensions of the pop-up
        text_surfaces = []
        total_height = 0
        max_width = 0
        for line in wrapped_lines:
            rendered_text = self.letters_font.render(line, True, (255, 255, 255))
            text_surfaces.append(rendered_text)
            line_width = rendered_text.get_width()
            line_height = rendered_text.get_height()
            max_width = max(max_width, line_width)
            total_height += line_height + line_spacing

        total_height -= line_spacing  # Remove the last line spacing

        # Calculate the size and position of the pop-up
        pop_up_width = max_width + 2 * text_margin + 2 * margin
        pop_up_height = total_height + 2 * text_margin + 2 * margin + button_height + button_margin
        pop_up_rect = pygame.Rect(
            self.screen_width // 2 - pop_up_width // 2,  # Centered horizontally
            self.screen_height // 2 - pop_up_height // 2,  # Centered vertically
            pop_up_width,
            pop_up_height
        )

        # Inner rectangle for the pop-up (inside margins)
        inner_rect = pygame.Rect(
            pop_up_rect.left + margin,
            pop_up_rect.top + margin,
            pop_up_rect.width - 2 * margin,
            pop_up_rect.height - 2 * margin - button_height - button_margin
        )

        # Draw the pop-up background with outer and inner rectangle
        pygame.draw.rect(self.screen, (30, 30, 30), pop_up_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), inner_rect, 2)  # White border

        # Calculate the starting Y position for rendering the text
        current_y = inner_rect.top + text_margin

        # Render and blit each line of text inside the inner pop-up area
        for surface in text_surfaces:
            text_rect = surface.get_rect(left=inner_rect.left + text_margin, top=current_y)
            self.screen.blit(surface, text_rect)
            current_y += surface.get_height() + line_spacing

        # Draw the close button at the bottom center within the pop-up area
        close_button = Button(
            "Close",
            pop_up_rect.centerx - 50,
            pop_up_rect.bottom - button_height - margin,
            120,
            40,
            (212, 152, 74),
            (70, 130, 180),
            self.font,
            (255, 255, 255)
        )
        close_button.draw(self.screen, pygame.mouse.get_pos())

        # Handle events to close the pop-up when the close button is clicked
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.rect.collidepoint(event.pos):
                    self.show_explanation = False  # Close the pop-up

    def runGame(self, namePlayer, playersDifficulty) -> None:
        """Start the game loop

        Args:
            players (list): list with all the players
        """
        players = [Player(namePlayer, False, 0)]
        i = 0
        for diff in playersDifficulty:
            if diff == 'Easy':
                players.append(Player('Bot' + str(i) + ' (Easy)', True, 1))
            elif diff == 'Medium':
                players.append(Player('Bot' + str(i) + ' (Medium)', True, 2, typeBot=2))
            elif diff == 'Hard':
                players.append(Player('Bot' + str(i) + ' (Hard)', True, 3))
            else:
                players.append(Player('Bot' + str(i) + ' (Expert)', True, 4))
            i += 1
        
        self.setupGame(players)
        
        turn = 0
        end = False
        
        phase = 'Choose'
        self.choosePlayer = True
        self.rowPlayer = False
        self.cardIndex = None
        self.row = None
        self.rowAssigned = False
        nextStep = False
        setup = True
        
        round = 1
        while True:
            if (end):
                # Show the results
                self.results()   
            
            if setup:
                # Give 10 cards to each player
                for p in self.game.players:
                    p.cards = []
                    for _ in range(10):
                        #card = self.game.deck.dealCard()
                        p.getCard(self.game.deck.dealCard())
                setup = False
            
            # First we play 10 turns
            # Each player choose a card
            if phase == 'Choose':
                if self.choosePlayer:
                    if (self.cardIndex != None):
                        cardsPlayed = [[self.game.players[0].playCard(self.cardIndex), self.game.players[0]]]
                        nextStep = True
                        self.choosePlayer = False
                        #time.sleep(1)
                if nextStep:
                    for i in range(1, len(self.game.players)):
                        # Save the played card in an array
                        cardsPlayed.append(self.game.chooseCard(self.game.players[i]))
                    # Once all players had played a card, we put them in the table in order from lower to bigger
                    cardsPlayed = sorted(cardsPlayed, key=lambda x: x[0].value)
                    phase = 'Play'
                    nextStep = False
            
            if phase == 'Play':
                #time.sleep(3)
                if not self.rowPlayer:
                    cardsBefore = []
                    i = 0
                    for card in cardsPlayed:
                        if card[1] != self.game.players[0]:
                            cardsBefore.append(card) # Save the cards that will be played before the player
                        else:
                            cardPlayer = card # The player card
                            break
                        i += 1
                    cardsPlayed = cardsPlayed[i + 1:] # Save the other cards
                
                if not self.rowPlayer:
                    for c in cardsBefore:
                        bulls = self.playCard(c[0], c[1], self.game.table)
                        c[1].points += bulls
                        if (len(c[1].pointsRound) < round):
                            c[1].pointsRound.append(bulls)
                        else:
                            c[1].pointsRound[round-1] += bulls
                    cardsBefore = []
                
                # Hacer la parte del usuario
                if not self.rowPlayer:
                    bulls = self.playCard(cardPlayer[0], cardPlayer[1], self.game.table)
                    self.resetColors(self.game.players[0])
                    if bulls == -1:
                        self.rowPlayer = True
                    else:
                        cardPlayer[1].points += bulls

                        if (len(cardPlayer[1].pointsRound) < round):
                            cardPlayer[1].pointsRound.append(bulls)
                        else:
                            cardPlayer[1].pointsRound[round-1] += bulls
                else:
                    if self.rowAssigned:
                        bulls = 0
                        for c in self.game.table.cards[self.row]:
                            bulls += c.bull
                        self.game.table.cards[self.row] = [cardPlayer[0]]
                        self.game.players[0].points += bulls
                        if (len(self.game.players[0].pointsRound) < round):
                            self.game.players[0].pointsRound.append(bulls)
                        else:
                            self.game.players[0].pointsRound[round-1] += bulls
                        self.rowAssigned = False
                        self.rowPlayer = False
                        #time.sleep(1)
                
                if not self.rowPlayer: 
                    for c in cardsPlayed:
                        bulls = self.playCard(c[0], c[1], self.game.table)
                        c[1].points += bulls
                        if (len(c[1].pointsRound) < round):
                            c[1].pointsRound.append(bulls)
                        else:
                            c[1].pointsRound[round-1] += bulls
                    cardsPlayed = []
                        
                if len(cardsPlayed) == 0:
                    turn += 1
                    phase = 'Choose'
                    self.choosePlayer = True
                    self.cardIndex = None
            
            if turn == 10:
                # Next round
                pointsRound = 9999
                for p in self.game.players:
                    if p.pointsRound[round-1] < pointsRound:
                        pointsRound = p.pointsRound[round-1]
                
                for p in self.game.players:
                    if p.pointsRound[round-1] == pointsRound:
                        p.winRound.append(True)
                    else:
                        p.winRound.append(False)
                
                round += 1

                # Once the 10 rounds are played we check if someone has lost already
                end, winner, points = self.game.checkWinner()
                turn = 0
                setup = True
                # We reset the deck and table for a new round
                self.game.resetRound()

                
            self.handle_events()
            self.update()
            self.render()
                    
    def handle_events(self) -> None:
        """Handle events of PyGame
        """
        # Iterate over all pygame events
        for event in pygame.event.get():                    
            # Get the current mouse position
            mouse_pos = pygame.mouse.get_pos()

            if self.showRow:
                # Iterate over each card in the player's hand
                for i, card in enumerate(self.game.players[0].cards):
                    # Create a rectangle representing the card's area on the screen
                    cardRect = pygame.Rect(30 + 76 * i, 460, 75, 100)
                    
                    # Check if the mouse position is within the card's rectangle
                    if cardRect.collidepoint(mouse_pos):
                        # Determine which rows can be played based on the hovered card
                        playable_row = self.get_playable_row(card)  # Implement this function
                        
                        # Adjust the brightness of the rows accordingly
                        for j, row in enumerate(self.game.table.cards):
                            if j == playable_row:
                                # Brighten the row
                                for table_card in row:
                                    table_card.brightness = 200
                            else:
                                # Darken the row
                                for table_card in row:
                                    table_card.brightness = -200
                        break
                else:
                    # If the mouse is not hovering over any card, reset the brightness of all table cards
                    for j, row in enumerate(self.game.table.cards):
                        for table_card in row:
                            table_card.brightness = 0
            
            # Check for quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Check for mouse button click event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the left mouse button is clicked
                if event.button == 1:
                    # Get the current mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    # If it's time to choose a player
                    if self.choosePlayer:
                        # Iterate over each card in the player's hand
                        for i, card in enumerate(self.game.players[0].cards):
                            # Create a rectangle representing the card's area on the screen
                            cardRect = pygame.Rect(30 + 76 * i, 460, 75, 100)
                            # Check if the mouse click occurred within the card's rectangle
                            if cardRect.collidepoint(mouse_pos):
                                # Store the index of the selected card
                                self.cardIndex = i
                                # Exit the loop since the card is selected
                                break
                    # If it's time to choose a row
                    elif self.rowPlayer:
                        # Iterate over each row on the table
                        for i, row in enumerate(self.game.table.cards):
                            for j, card in enumerate(row):
                                # Create a rectangle representing the card's area on the screen
                                cardRect = pygame.Rect(60 + 76 * j, 25 + 101 * i, 75, 100)
                                # Check if the mouse click occurred within the card's rectangle
                                if cardRect.collidepoint(mouse_pos):
                                    # Store the index of the selected row
                                    self.row = i
                                    # Set a flag indicating that a row has been selected
                                    self.rowAssigned = True
                                    # Exit the loop since the row is selected
                                    break
                            else:
                                # Continue to the next row if no card is selected in the current row
                                continue
                            # Break the outer loop since a row is selected
                            break
            elif event.type == pygame.KEYDOWN:
                if self.hint:
                    # If 'h' key is pressed, give a hint to the player
                    if event.key == pygame.K_h:
                        # Set the player to be controlled by a bot temporarily
                        player = self.game.players[0]
                        player.bot = True
                        player.difficulty = 4
                        player.load_model()
                        game_state = self.game.getGameState()
                        preprocessed_state, player_card_indices = preprocess_state(game_state)
                        preprocessed_state = np.expand_dims(preprocessed_state, axis=0)  # Add batch dimension
                        predictions = player.model.predict(preprocessed_state)[0]  # Get the predictions for the batch

                        player_card_indices = [c.value for c in player.cards]
                        # Filter the predictions to only consider the player's cards
                        player_card_predictions = predictions[player_card_indices]
                        index = np.argmax(player_card_predictions)
                        
                        # Reset player control to human after making the decision
                        player.bot = False
                        player.difficulty = 0
                        
                        # Get the current mouse position
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Determine which cards can be played
                        for j, card in enumerate(self.game.players[0].cards):
                            if j == index:
                                # Brighten the card
                                card.brightness = 200
                            else:
                                # Darken the card
                                card.brightness = -200
                    # If 'k' key is pressed, reset brightness of all cards
                    elif event.key == pygame.K_k:
                        for j, card in enumerate(self.game.players[0].cards):
                            card.brightness = 0              

    def get_playable_row(self, card):
        index = 99
        diff = 105
        i = 0
        for row in self.game.table.cards:
            lastCard = row[-1]
            difference = card.value - lastCard.value
            if (difference > 0):
                if diff > difference:
                    diff = difference
                    index = i
            
            i += 1
        return index
    
    def display_text(self, text_surfaces, line_spacing):
        y_offset = 0
        for surface in text_surfaces:
            self.screen.blit(surface, (450, 150 + y_offset))
            y_offset += surface.get_height() + line_spacing
        
    def wrap_text(self, text):
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_surface = self.font.render(word, True, (255, 255, 255))
            word_width, word_height = word_surface.get_size()
            
            # Check if adding the word exceeds the maximum width
            if current_width + word_width > 800 and current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width + self.font.size(' ')[0]  # reset width with the new word's width plus a space
            else:
                current_line.append(word)
                current_width += word_width + self.font.size(' ')[0]  # add word width plus a space

        if current_line:
            lines.append(' '.join(current_line))

        return lines
    
    def update(self) -> None:
        """Update the frames
        """
        self.clock.tick(60)

    def drawDeckPlayer(self) -> None:
        """Draw the deck that the player has
        """
        if not self.rowPlayer:
            for index, card in enumerate(self.game.players[0].cards):
                # Calculate the position of the card
                card_position = (30 + 76 * index, 460)
                
                # Get the card image from the preloaded images
                card_image = self.cardImages[card.value - 1]  # Assuming card.value is 1-based index
                
                # Adjust the brightness
                card_image_with_brightness = self.adjust_brightness(card_image, card.brightness)

                # Blit the card image
                self.screen.blit(card_image_with_brightness, card_position)
        else:
            playerRect = pygame.Rect(190, 485, 410, 35) 
            pygame.draw.rect(self.screen, ('tan2'), playerRect, border_radius=20) # White color
            
            # The text with the points
            text_surface = self.small_font.render('Choose a row to play the card', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=playerRect.center)
            self.screen.blit(text_surface, text_rect)
    
    def drawTable(self) -> None:
        """Draw the cards on the table."""
        for i, row in enumerate(self.game.table.cards):
            for j, card in enumerate(row):
                # Calculate the position of the card
                card_position = (60 + 76 * j, 25 + 101 * i)
                
                # Get the card image from the preloaded images
                card_image = self.cardImages[card.value - 1]  # Assuming card.value is 1-based index
                
                # Adjust the brightness
                card_image_with_brightness = self.adjust_brightness(card_image, card.brightness)

                # Blit the card image
                self.screen.blit(card_image_with_brightness, card_position)

    def drawPoints(self) -> None:
        """Draw the points that all the players has
        """
        i = 0
        self.screen.blit(self.punctuation_image, (450, 25))
        for p in self.game.players:
            # Draw the rectangle
            playerRect = pygame.Rect(450, 100 + i * 20, 300, 20) 
            #pygame.draw.rect(self.screen, (255, 255, 255), playerRect) # White color
            
            # The text with the points
            if p.points == 1:
                text_surface = self.letters_font.render(p.name + ' - ' + str(p.points) + ' point', True, (0, 0, 0))
            else:
                text_surface = self.letters_font.render(p.name + ' - ' + str(p.points) + ' points', True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=playerRect.center)
            self.screen.blit(text_surface, text_rect)
            i += 1
    
    def draw_text(self, text, position, font, color=(255, 255, 255)):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_checkbox(self, rect, is_checked):
        pygame.draw.rect(self.screen, pygame.Color('white'), rect, border_radius=5)
        if is_checked:
            pygame.draw.rect(self.screen, pygame.Color(212, 152, 74), rect.inflate(-4, -4), border_radius=5)

    def draw_text_box(self, text, x, y, font):
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(x, y))
        bg_rect = pygame.Rect(
            text_rect.left - 10, text_rect.top - 5,
            text_rect.width + 20, text_rect.height + 10
        )
        pygame.draw.rect(self.screen, ('tan4'), bg_rect, border_radius=20)
        self.screen.blit(text_surface, text_rect)
    
    def draw_option_with_background(self, title, description, position, checkbox_rect, is_checked):
        box_padding = 10
        title_surface = self.font.render(title, True, (255, 255, 255))
        description_surface = self.letters_font.render(description, True, (255, 255, 255))
        
        # Calculate the background box size and position
        title_rect = title_surface.get_rect(topleft=position)
        description_rect = description_surface.get_rect(topleft=(position[0], position[1] + 50))
        
        box_width = max(title_rect.width, description_rect.width) + box_padding * 2
        box_height = title_rect.height + description_rect.height + box_padding * 3
        box_rect = pygame.Rect(
            position[0] - box_padding,
            position[1] - box_padding,
            box_width,
            box_height
        )
        
        # Draw the background box
        pygame.draw.rect(self.screen, pygame.Color('tan4'), box_rect, border_radius=20)
        
        # Draw the title, description, and checkbox on top of the box
        self.screen.blit(title_surface, title_rect.topleft)
        self.screen.blit(description_surface, description_rect.topleft)
        self.draw_checkbox(checkbox_rect, is_checked)
    
    def render(self) -> None:
        """Render the screen
        """
        
        #self.screen.fill((0, 0, 0))  # Black color for background
        self.screen.blit(self.bg_game_image, (0, 0))  # Draw the background image
        self.drawDeckPlayer()
        self.drawTable()
        self.drawPoints()
        
        pygame.display.flip()  # Update screen
        
    def setupGame(self, players) -> None:
        """Setup the game loop

        Args:
            players (list): List with all the players
        """
        self.game = Game(players)
        
    def playCard(self, card, players, table):
        card.brightness = 0
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
            if not players.bot:
                return -1
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
                            
                if players.difficulty == 1: # Easy, get the biggest amount of bulls
                    index = biggest
                elif players.difficulty == 2: # Medium, get random index
                    index = random.randint(0, len(table.cards) - 1)
                elif players.difficulty == 3: # Hard, get the leats amount of bulls
                    index = leasts
                elif players.difficulty == 4: # Expert, get the leats amount of bulls
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

    def resetColors(self, player):
        for c in player.cards:
            c.brightness = 0
           
    def adjust_brightness(self, image, brightness):
        """Adjust the brightness of an image."""
        # Create a copy of the image to modify
        brightness_image = image.copy()
        # Create a brightness filter surface
        brightness_filter = pygame.Surface(image.get_size()).convert_alpha()
        # Set the brightness filter color based on the brightness value
        brightness_color = (brightness, brightness, brightness, 0) if brightness >= 0 else (-brightness, -brightness, -brightness, 0)
        brightness_filter.fill(brightness_color)
        # Blend the brightness filter with the image
        brightness_image.blit(brightness_filter, (0, 0), special_flags=pygame.BLEND_RGBA_ADD if brightness >= 0 else pygame.BLEND_RGBA_SUB)
        return brightness_image
 
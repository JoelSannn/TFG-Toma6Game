import csv
import numpy as np

def preprocess_state(state, max_table_rows=4, max_table_cols=4, max_players=10, max_player_cards=10):
        """Preprocess a single state to a fixed-size feature vector and return the indices of the player's cards."""
        # Flatten the table cards and pad or truncate to fixed size
        table_flat = [card for row in state['table'] for card in row]
        table_size = max_table_rows * max_table_cols
        table_flat = table_flat[:table_size] + [0] * (table_size - len(table_flat))

        # Flatten the player cards and other features
        player_features = []
        player_card_indices = []

        # Add dummy players if there are fewer than max_players
        num_players = len(state['players'])
        for i in range(max_players):
            if i < num_players:
                # Process actual player
                player = state['players'][i]
                player_cards = player['cards']
                # Pad or truncate player cards to a fixed length
                player_cards_padded = player_cards[:max_player_cards] + [0] * (max_player_cards - len(player_cards))
                player_points = player['points']
                player_is_bot = 1 if player['bot'] else 0
                start_idx = len(table_flat) + len(player_features)
                player_card_indices.extend(range(start_idx, start_idx + len(player_cards)))
                player_features.extend(player_cards_padded)
                player_features.append(player_points)
                player_features.append(player_is_bot)
            else:
                # Add dummy player with all zeros
                player_cards_padded = [0] * max_player_cards
                player_features.extend(player_cards_padded)
                player_features.append(0)  # Dummy player points
                player_features.append(0)  # Dummy player is_bot

        # Combine table features with player features
        features = table_flat + player_features

        return np.array(features), player_card_indices  # Ensure the result is a 1D array

def preprocess_data(file_path):
    """Load and preprocess data from a CSV file."""
    X = []
    y = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            state = eval(row[0])  # Evaluate the string representation of the dictionary
            action = row[1]
            X.append(preprocess_state(state))
            y.append(int(action))  # Convert action to an integer

    # Ensure all states have the same number of features by padding/truncating
    max_features = max(len(x) for x in X)
    X = np.array([np.pad(x, (0, max_features - len(x))) for x in X])

    y = np.array(y)

    return X, y

import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.metrics import accuracy_score
from data_processing import preprocess_data, preprocess_state
from model import build_model

# Load and preprocess the data
print("Loading and preprocessing data...")
file_path = 'neural_network/data/game_data.csv'
X, y = preprocess_data(file_path)
print(f"Data loaded and preprocessed successfully! Shape of X: {X.shape}, Shape of y: {y.shape}")

# Split the data into training and testing sets
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Data split completed: {len(X_train)} training samples and {len(X_test)} testing samples.")

# Print the shape of X_train and X_test for debugging
print(f"Shape of X_train: {X_train.shape}, Shape of X_test: {X_test.shape}")

# Load the trained model
print("Loading the trained model...")
model = tf.keras.models.load_model('neural_network/game_model.h5')
print("Model loaded successfully!")

# Evaluate the model on the test data
print("Evaluating the model...")
y_pred = np.argmax(model.predict(X_test), axis=1)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy on test data: {accuracy:.4f}")

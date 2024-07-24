import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
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

# Build the model
print("Building the model...")
input_shape = (X_train.shape[1],)  # Use the shape of the input data (number of features)
output_shape = len(np.unique(y)) + 1  # Number of unique actions
model = build_model(input_shape, output_shape)
print("Model built successfully!")

# Define a custom callback to print progress at each epoch
class EpochProgressCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"Epoch {epoch + 1}/{self.params['epochs']} - loss: {logs['loss']:.4f} - accuracy: {logs.get('accuracy', 0):.4f} - val_loss: {logs['val_loss']:.4f} - val_accuracy: {logs.get('val_accuracy', 0):.4f}")

# Train the model with progress prints at each epoch
print("Training the model...")
model.fit(
    X_train, 
    y_train, 
    epochs=10, 
    batch_size=32, 
    validation_data=(X_test, y_test),
    callbacks=[EpochProgressCallback()]
)
print("Model training completed!")

# Save the trained model
print("Saving the model...")
model.save('neural_network/game_model.h5')
print("Model saved successfully!")

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def build_model(input_shape, output_shape):
    """Builds and compiles the neural network model."""
    model = Sequential()
    # First dense layer with 128 units and ReLU activation
    model.add(Dense(128, input_shape=input_shape, activation='relu'))
    # Second dense layer with 64 units and ReLU activation
    model.add(Dense(64, activation='relu'))
    # Output layer with softmax activation for categorical output
    model.add(Dense(output_shape, activation='softmax'))
    
    # Compile the model with Adam optimizer and sparse categorical crossentropy loss
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    return model

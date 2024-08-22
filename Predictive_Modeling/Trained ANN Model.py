print(df.columns)

# List all column names
print(df.columns)

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

# Step 1: Load the dataset
from google.colab import files
uploaded = files.upload()

# Replace 'Dataset (ATS)-1.csv' with your actual file name
df = pd.read_csv('Dataset (ATS)-1.csv')

# Step 2: Explore the dataset
df.head()  # View the first few rows of the dataset
df.info()  # Check for data types and missing values
df.describe()  # Get summary statistics

# Step 3: Preprocess the data
# Encode the 'Churn' column (target) as binary: 1 for 'Yes', 0 for 'No'
df['Churn'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

# Set X and y
X = df.drop('Churn', axis=1)  # Features (independent variables)
y = df['Churn']  # Target (dependent variable)

# Handle categorical variables (convert them to numerical)
# Identify categorical columns
categorical_columns = X.select_dtypes(include=['object']).columns
print(categorical_columns)  # Prints columns like ['gender', 'Dependents', etc.]

# Encoding categorical columns
X = pd.get_dummies(X, columns=categorical_columns, drop_first=True)

# Normalize (scale) the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 5: Define the model
model = Sequential()

# Input layer (with input shape equal to number of features)
model.add(Dense(units=64, activation='relu', input_shape=(X_train.shape[1],)))

# Hidden layers
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=16, activation='relu'))

# Output layer (with a single neuron for binary classification)
model.add(Dense(units=1, activation='sigmoid'))

# Step 6: Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Step 7: Train the model
history = model.fit(X_train, y_train, validation_split=0.2, epochs=50, batch_size=32)

# Step 8: Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {test_accuracy}')

# Step 9: Plot the training history
# Plot training & validation accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Plot training & validation loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Step 10: Generate Predictions and Evaluate
predictions = model.predict(X_test)
predictions = (predictions > 0.5).astype(int)  # Convert probabilities to binary output

from sklearn.metrics import confusion_matrix, classification_report
cm = confusion_matrix(y_test, predictions)
print('Confusion Matrix:')
print(cm)

print('Classification Report:')
print(classification_report(y_test, predictions))

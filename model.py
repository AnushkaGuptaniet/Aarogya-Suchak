import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# LOAD DATASET
df = pd.read_csv("diabetes.csv")

# FEATURES + TARGET
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# TRAIN MODEL
model = RandomForestClassifier()
model.fit(X_train, y_train)

# SAVE MODEL
pickle.dump(model, open("models/diabetes.pkl", "wb"))

print("Diabetes model saved ")
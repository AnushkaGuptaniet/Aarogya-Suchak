import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# load dataset
df = pd.read_csv("liver.csv")

# 🔥 convert Gender to numeric
df["Gender"] = df["Gender"].map({"Male": 1, "Female": 0})

# drop missing values (important)
df = df.dropna()

# features & target
X = df.drop("Dataset", axis=1)
y = df["Dataset"]

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# save model
pickle.dump(model, open("models/liver.pkl", "wb"))

print("Liver model saved ")
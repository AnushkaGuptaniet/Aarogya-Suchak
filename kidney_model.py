import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# load dataset
df = pd.read_csv("kidney.csv")

# drop id column if exists
if "id" in df.columns:
    df = df.drop("id", axis=1)

# 🔥 CLEAN TEXT (IMPORTANT)
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].str.strip().str.lower()

# 🔥 REPLACE ALL TEXT VALUES
df.replace({
    "normal": 0,
    "abnormal": 1,
    "present": 1,
    "notpresent": 0,
    "yes": 1,
    "no": 0,
    "good": 0,
    "poor": 1,
    "ckd": 1,
    "notckd": 0
}, inplace=True)

# convert everything to numeric
df = df.apply(pd.to_numeric, errors='coerce')

# drop missing
df = df.dropna()

# features & target
X = df.drop("classification", axis=1)
y = df["classification"]

# train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# save model
pickle.dump(model, open("models/kidney.pkl", "wb"))

print("Kidney model saved ")
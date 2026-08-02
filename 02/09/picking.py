import pickle

data = {
    "name": "Kim",
    "age": 25,
    "scores": [80, 90, 85] 
}

with open("data.pkl", "wb") as f:
    pickle.dump(data, f)
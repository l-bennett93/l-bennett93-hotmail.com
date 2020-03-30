from joblib import load
from pathlib import Path
import sklearn
import numpy as np

print(sklearn.__version__)

file = Path("C:/Users/lubennett/Desktop/Workspaces/red-wine-dataset (complete)/app/wine_analyser/networks/random_forest.pkl")

model = load(file)

prediction = model.predict([list(np.arange(11))])
print(prediction[0])

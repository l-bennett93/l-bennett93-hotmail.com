import shap
from joblib import load
import sklearn
from pathlib import Path

class Interpretive_ML():
    def __init__(self):

        #Instantiate the model
        file = Path("wine_analyser/networks/random_forest.pkl")
        self.model = load(file)
        self.explainer = shap.TreeExplainer(self.model)

    def prediction(self, sample):
        return self.model.predict(x)

    def tree(self,sample):
        pass
        # shap_values = explainer.shap_values(sample)

    def shapley_feature_absolute(self, sample):
        return self.explainer.shap_values(sample)

    def shapley_feature_directional(self, sample):
        shap_values = self.explainer.shap_values(sample)
        return np.abs(np.array(shap_values))

class Predictor:
    def __init__(self, class_probs, probabilities):
        self.class_probs = class_probs
        self.probabilities = probabilities

    def predict(self,sample):
        if not self.class_probs or not self.probabilities:
            raise ValueError("Model is not trained yet")

        scores = {}
        for cls in self.class_probs:
            prob = self.class_probs[cls]
            for feature, value in sample.items():
                if feature in self.probabilities and value in self.probabilities[feature]:
                    prob *= self.probabilities[feature][value].get(cls, 1e-6)
                else:
                    prob *= 1e-6
            scores[cls] = prob
        return max(scores, key=scores.get)
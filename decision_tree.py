import numpy as np
from collections import Counter

class DecisionTree:
    def __init__(self):
        self.tree = None

    def entropy(self, y):
        counts = np.bincount(y)
        probabilities = counts / len(y)
        return -np.sum([p * np.log2(p) for p in probabilities if p > 0])

    def information_gain(self, X, y, feature):
        original_entropy = self.entropy(y)
        values, counts = np.unique(X[:, feature], return_counts=True)
        weighted_entropy = np.sum([(counts[i] / np.sum(counts)) * self.entropy(y[X[:, feature] == values[i]]) for i in range(len(values))])
        return original_entropy - weighted_entropy

    def best_feature(self, X, y):
        information_gains = [self.information_gain(X, y, feature) for feature in range(X.shape[1])]
        return np.argmax(information_gains)

    def build_tree(self, X, y, features):
        if len(np.unique(y)) == 1:
            return y[0]
        if len(features) == 0:
            return Counter(y).most_common(1)[0][0]
        best_feature = self.best_feature(X, y)
        tree = {best_feature: {}}
        features = [f for f in features if f != best_feature]
        for value in np.unique(X[:, best_feature]):
            subtree = self.build_tree(X[X[:, best_feature] == value], y[X[:, best_feature] == value], features)
            tree[best_feature][value] = subtree
        return tree

    def fit(self, X, y):
        features = list(range(X.shape[1]))
        self.tree = self.build_tree(X, y, features)

    def predict_one(self, x, tree):
        if not isinstance(tree, dict):
            return tree
        feature = list(tree.keys())[0]
        if x[feature] in tree[feature]:
            return self.predict_one(x, tree[feature][x[feature]])
        else:
            return Counter([self.predict_one(x, subtree) for subtree in tree[feature].values()]).most_common(1)[0][0]

    def predict(self, X):
        return np.array([self.predict_one(x, self.tree) for x in X])
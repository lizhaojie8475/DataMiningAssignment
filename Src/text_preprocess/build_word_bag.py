from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2, SelectKBest
import numpy as np

class wordBag:
    def __init__(self, k=10000):
        """
        :param k: 表示词袋的维度大小
        """
        self.k = k
        self.words = []

    def fit(self, X, y):
        """
        使用卡方检验进行特征选择
        :param X: 训练集的文本内容
        :param y: 每个文本的类别标签
        :return:
        """
        self.X = X
        tf_vec = TfidfVectorizer(token_pattern='(?u)\\b\\w+\\b')
        X_tf = tf_vec.fit_transform(X)
        chi2_model = SelectKBest(chi2, k=self.k)
        chi2_model.fit(X_tf, y)

        indexes = np.argmax(chi2_model.scores_)
        self.words = tf_vec.get_feature_names()[indexes]

    def transform(self, X):
        """
        对输入的向量X，映射为词袋特征向量
        :param X: 输入向量
        :return: tf-idf的特征向量
        """
        tf_vec = TfidfVectorizer(vocabulary=self.words, token_pattern='(?u)\\b\\w+\\b')
        tf_vec.fit(self.X)
        X_tf = tf_vec.transform(X)
        return X_tf

    def fit_transform(self, X, y):
        """
        同时进行特征选择和特征映射
        :param X: 输入向量
        :param y: 文本的类别标签
        :return: tf-idf的特征向量
        """
        self.X = X
        tf_vec = TfidfVectorizer(token_pattern='(?u)\\b\\w+\\b')
        X_tf = tf_vec.fit_transform(X)
        chi2_model = SelectKBest(chi2, k=self.k)
        chi2_model.fit(X_tf, y)

        indexes = np.argmax(chi2_model.scores_)
        self.words = tf_vec.get_feature_names()[indexes[:self.k]]

        return chi2_model.transform(X_tf)

if __name__ == "__main__":
    pass
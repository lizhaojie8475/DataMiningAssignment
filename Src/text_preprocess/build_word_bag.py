from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_selection import chi2, SelectKBest
from sklearn.utils import as_float_array
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
import numpy as np
from MySQLHelper.MySqlHelper import MySqlHelper

SEGMENT_TABLE_NAME = "segment_data"

class wordBag:
    def __init__(self, k=0):
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
        scores, p_val = chi2(X_tf, y)
        scores = as_float_array(scores, copy=True)
        scores[np.isnan(scores)] = np.finfo(scores.dtype).min

        if self.k == 0:
            k = np.sum(scores >= np.mean(scores))
        else:
            k = self.k

        indexes = np.argsort(scores)
        feature_names = tf_vec.get_feature_names()
        feature_names = np.array(feature_names)
        self.words = feature_names[indexes[k]]

    def transform(self, X):
        """
        对输入的向量X，映射为词袋特征向量
        :param X: 输入向量
        :return: tf-idf的特征向量
        """
        tf_vec = TfidfVectorizer(vocabulary=self.words, token_pattern='(?u)\\b\\w+\\b')
        tf_vec.fit(self.X)
        return tf_vec.transform(X)

    def fit_transform(self, X, y):
        """
        同时进行特征选择和特征映射
        :param X: 输入向量
        :param y: 文本的类别标签
        :return: tf-idf的特征向量
        """
        self.fit(X, y)

        return self.transform(X)

def insertWordBag(words):
    helper = MySqlHelper()
    helper.connect()
    sql = "INSERT INTO word_bag(word) VALUES(%s)"
    for word in words:
        helper.insert(sql, word)

def insertWordVect(id, vectList, role):
    helper = MySqlHelper()
    helper.connect()
    sql = "INSERT INTO word_vec(id, vector, role) VALUES(%d, %s, %s)"
    for i, vec in zip(id, vectList):
        helper.insert(sql, i, vec, role)

if __name__ == "__main__":
    helper = MySqlHelper()
    helper.connect()

    idSql = 'SELECT id FROM %s where role = "%s" ' % (SEGMENT_TABLE_NAME, "train")
    contentSql = 'SELECT content FROM %s where role = "%s" ' % (SEGMENT_TABLE_NAME, "train")
    typeSql = 'SELECT type FROM %s where role = "%s" ' % (SEGMENT_TABLE_NAME, "train")

    contentText = helper.search(contentSql)
    contentText = np.array(contentText)
    X_raw = contentText[:, 0]

    typeText = helper.search(typeSql)
    typeText = np.array(typeText)
    y_raw = typeText[:, 0]
    y_raw = LabelEncoder().fit_transform(y_raw)

    idText = helper.search(idSql)
    idText = np.array(idText)
    id = idText[:, 0]

    bag = wordBag()
    wordVects = bag.fit_transform(X_raw, y_raw)

    insertWordBag(bag.words)
    insertWordVect(id, wordVects)

import pynlpir
from MySQLHelper.MySqlHelper import MySqlHelper
import re
import math


def wordSegmenter(sentence='',pathOfStopWords=''):
    """
    将传入的句子分词并去除停用词
    :param sentence:         传入的句子
    :param pathOfStopWords:  停用词的路径
    :return:                 分词并去除停用词后由空格分隔的字符串
    """
    pynlpir.open()

    seg_list = []
    for seg in pynlpir.segment(sentence):
        seg_list.append(seg[0])
    #去除停用词
    resultWords = []

    f_stop = open(pathOfStopWords, 'rt', encoding='utf-8')
    try:
        f_stop_text = f_stop.read()
    finally:
        f_stop.close()
    f_stop_words = f_stop_text.split("\n")
    for seg in seg_list:
        seg = seg.strip()
        if re.match(r'[a-zA-Z0-9]+',seg): #去掉英文以及数字
            continue
        if len(seg) > 0 and (seg not in f_stop_words):
            resultWords.append(seg)
    return " ".join(resultWords)


if __name__ == '__main__':

    STOP_WORDS = "stopWords.txt"

    allData = 1081273  # 1081273                          # 总共多少数据
    dataOfEach = 5000                                    # 每个批次多少条数据
    batch = math.ceil(allData / dataOfEach)             # 批次
    IDctrl = 1

    MySql = MySqlHelper()
    MySql.connect()

    while IDctrl < allData:
        data_list = []

        sql = 'SELECT id,content,type,role FROM rawdata where ID>=' + str(IDctrl) + ' and ID <' + str(IDctrl + dataOfEach)
        text = MySql.search(sql)
        content_list = []

        for item in text:
            print(item[0])
            res = wordSegmenter(item[1], STOP_WORDS)
            content_list=[item[0], res, item[2], item[3]]
            data_list.append(content_list)
        try:
            MySql.insertMany(data_list)
        except:
            print('something error')
        IDctrl += dataOfEach
    MySql.close()
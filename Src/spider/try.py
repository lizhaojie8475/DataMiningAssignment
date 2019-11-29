import os
import sys

pwd = os.path.dirname(__file__)
fileList = pwd.split('/')
print(fileList[:-4])
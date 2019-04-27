# coding=utf-8

import os
import sys

from epayapp import my_epay

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
sys.path.append('C:\\DevTools\\my_blockchain')

my_epay.loop_epay("my_epay_data.json")

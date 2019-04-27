# coding=utf-8

import os
import sys

from epayapp import my_epay

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

my_epay.loop_epay("my_epay_data.json")

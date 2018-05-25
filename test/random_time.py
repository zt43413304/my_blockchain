import random
import time

MIN_SEC = 3
MAX_SEC = 8
for i in range(3):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("before time.sleep() " + str(datetime))
    time.sleep(random.randint(MIN_SEC, MAX_SEC))
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("after time.sleep() " + str(datetime))
    print("\r\n")

import time
def traversal_list(alist, i):
    while True:
        length = len(alist)
        i = i%(length)
        yield alist[i]
        i += 1

def traversal_list2(alist):
    i = 0
    f = traversal_list(alist, i)
    while True:
        a = next(f)
        time.sleep(1)
        i += 1
        print(a)
        # return a

def unlimiated():
    alist = ["__all__", "news_hot", "news_entertainment", "news_tech", "news_travel", "news_sports"]
    for i in range(len(alist)):
        print(alist[i])
        time.sleep(1)
        if i == len(alist)-1:
            unlimiated()

if __name__ == '__main__':
    # alist = [1, 2, 3, 4, 5]
    # alist = ["__all__", "news_hot", "news_entertainment", "news_tech", "news_travel", "news_sports"]
    # traversal_list2(alist)

    unlimiated()
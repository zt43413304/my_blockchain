def test1():
    try:
        print("1")
        raise Exception("hehe")
        print("2")
        return "a"
    except Exception as e:
        print("3")
        print(e)
        return "b"


print(test1())

import random


def get_tracks2(distance):
    '''
    拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
    匀变速运动基本公式：
    ①v=v0+at
    ②s=v0t+½at²
    ③v²-v0²=2as
    :param distance: 需要移动的距离
    :return: 存放每0.3秒移动的距离
    '''
    v = 0
    t = 0.3
    tracks = []
    current = 0
    mid = distance * 4 / 5

    while current < distance:
        if current < mid:
            # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
            a = 2
        else:
            a = -3
        v0 = v
        s = v0 * t + 0.5 * a * (t ** 2)
        current += s
        tracks.append(round(s))
        v = v0 + a * t
    print("********** 40. 计算轨迹后，偏差值 = " + str(sum(tracks) - distance))
    return tracks


def slide_tracks(distance):
    # 移动距离的列表
    track = []
    # 当前距离
    current = 0
    # 改变加速度的时间点
    mid = distance * 4 / 5
    # 计算移动距离所需的时间间隔
    t = 0.3
    # 速度
    speed = 0

    while current < distance:
        if current < mid:
            a = 3
            # 距离的计算公式
            move_distance = speed * t + 0.5 * a * t * t
            # 将生成的移动距离添加到列表中
            track.append(round(move_distance))
            speed += (a * t)
            current += move_distance
        else:
            # 当距离大于五分之三的position时，添加减速轨迹，并跳出循环
            track.extend([3, 2, 1])
            break
    # 识别当前总共移动距离是大于还是小于position
    # 大于则补连续的-1，小于则补连续的1
    offset = int(sum(track) - distance)
    print(">>>offset=" + str(offset))
    if offset > 0:
        track.extend([-1 for i in range(offset)])
    elif offset < 0:
        track.extend([1 for i in range(abs(offset))])

    # 模拟终点附近的左右移动
    track.extend(
        [0, 0, 0, -1, 1, -1, 1, -1, 1, 0, 0, 0])
    print("********** 41. 计算轨迹后，偏差值 = " + str(sum(track) - distance))
    return track


# 根据缺口的位置模拟x轴移动的轨迹
def get_tracks3(distance):
    len_ori = distance
    # pass
    tracks = []
    # 间隔通过随机范围函数来获得,每次移动一步或者两步
    x = random.randint(1, 3)
    # 生成轨迹并保存到list内
    while distance - x >= 5:
        tracks.append(x)
        distance = distance - x
        x = random.randint(3, 6)
    # 最后五步都是一步步移动
    for i in range(distance):
        tracks.append(1)

    # 识别当前总共移动距离是大于还是小于position
    # 大于则补连续的-1，小于则补连续的1
    offset = int(sum(tracks) - len_ori)
    print(">>>>> offset=" + str(offset))
    if offset > 0:
        tracks.extend([-1 for i in range(offset)])
    elif offset < 0:
        tracks.extend([1 for i in range(abs(offset))])

    # 模拟终点附近的左右移动
    tracks.extend(
        [0, 1, -1, 0])
    # logger.warning("********** 4. 计算轨迹后，偏差值 = " + str(sum(tracks) - distance))
    print("********** 42. 计算轨迹后，偏差值 = " + str(sum(tracks) - len_ori))

    return tracks


def get_tracks(distance):
    """
    根据偏移量获取移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    """
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 3 / 5
    # 计算间隔
    t = 0.3
    # 初速度
    v = 0

    while current < distance:
        if current < mid:
            # 加速度为正2
            a = 2
        else:
            # 加速度为负3
            a = -3
        # 初速度v0
        v0 = v
        # 当前速度v = v0 + at
        v = v0 + a * t
        # 移动距离x = v0t + 1/2 * a * t^2
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))

    # 识别当前总共移动距离是大于还是小于position
    # 大于则补连续的-1，小于则补连续的1
    offset = int(sum(track) - distance)
    print(">>>>> offset=" + str(offset))
    if offset > 0:
        track.extend([-1 for i in range(offset)])
    elif offset < 0:
        track.extend([1 for i in range(abs(offset))])

    # 模拟终点附近的左右移动
    track.extend(
        [0, 1, -1, 0])
    print("********** 4. 计算轨迹后，偏差值 = " + str(sum(track) - distance))
    return track


# tracks = get_tracks(200)
# print(tracks)
#
# tracks = slide_tracks(200)
# print(tracks)

tracks = get_tracks3(200)
print(tracks)

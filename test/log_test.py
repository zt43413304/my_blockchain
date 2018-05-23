import logging  # 引入logging模块
import os.path
import time

import testing1
import testing2

# 默认生成的root logger的level是logging.WARNING,低于该级别的就不输出了
# 级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG

# 如果需要显示低于WARNING级别的内容，可以引入NOTSET级别来显示：
# logging.basicConfig(level=logging.NOTSET)  # 设置日志级别


# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做相关配置
# # 由于日志基本配置中级别设置为DEBUG，所以一下打印信息将会全部显示在控制台上
#
#
# # 将信息打印到控制台上
# logging.debug(u"苍井空")
# logging.info(u"麻生希")
# logging.warning(u"小泽玛利亚")
# logging.error(u"桃谷绘里香")
# logging.critical(u"泷泽萝拉")


# 第一步，创建一个logger
logger = logging.getLogger("log_test.py")
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/Logs/'
log_name = log_path + rq + '.log'
logfile = log_name

fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关

# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第四步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

# 日志
logger.debug(u"苍井空")
logger.info(u"麻生希")
logger.warning(u"小泽玛利亚")
logger.error(u"桃谷绘里香")
logger.critical(u"泷泽萝拉")

testing1.test136()
testing2.test138()

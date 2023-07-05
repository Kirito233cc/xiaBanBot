import time
from datetime import datetime

import requests


def xiaBanBot(content):
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'key': '81a799ef-6eaf-4c3b-91ca-6ac7a75741ee',
    }

    json_data = {
        'msgtype': 'text',
        'text': {
            'content': content,
        },
    }

    requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send', params=params, headers=headers, json=json_data)


# 将时间格式转换为中文
def timeFormat(original_time):
    # original_time = original_time.split(':')
    original_time = [int(i) for i in original_time]
    if original_time[0] == 0:
        new_time = f'{original_time[1]}分钟'
    elif original_time[0] > 0:
        new_time = f'{original_time[0]}小时{original_time[1]}分钟'
    else:
        return False
    return new_time


# 判断距离下班时间是否在一小时内
def timeLeftIn1H(xiaBan_time='18:30'):
    now = datetime.now().strftime('%H:%M')
    time = timeSubtraction(xiaBan_time, now)
    # time = time.split(':')
    if time:
        time = [int(i) for i in time]
        if time[0] == 1 and time[1] == 0:
            content = 'Hi, 我是机器人反卷先锋001\n温馨提示，距离下班仅剩1小时。'
            xiaBanBot(content)
            return True
        elif time[0] == 0 and time[1] < 60:
            return True
        else:
            return False
    else:
        return False


# 判断是否已经到下班时间
def timeIsUp(xiaBan_time='18:30'):
    now = datetime.now().strftime('%H:%M')
    time = timeSubtraction(xiaBan_time, now)
    if time:
        return False
    # print(time)
    else:
        content = 'Hi, 我是机器人反卷先锋001\n温馨提示，下班时间到了，请速速离开公司。'
        xiaBanBot(content)
        return True


# 时间相减,返回时间差
def timeSubtraction(time1, time2):
    time1 = time1.split(':')
    time2 = time2.split(':')
    time1 = [int(i) for i in time1]
    time2 = [int(i) for i in time2]
    if time1[0] < time2[0]:
        return False
    elif time1[0] == time2[0]:
        if time1[1] < time2[1]:
            return False
        elif time1[1] == time2[1]:
            return False
        else:
            time = [time1[i] - time2[i] for i in range(2)]
            return time
    # time2的分钟大于time1的分钟的情况
    else:
        if time1[1] < time2[1]:
            time1[0] -= 1
            time1[1] += 60
            time = [time1[i] - time2[i] for i in range(2)]
            return time
        elif time1[1] == time2[1]:
            time = [time1[i] - time2[i] for i in range(2)]
            return time
        else:
            time = [time1[i] - time2[i] for i in range(2)]
            return time


# 判断是否到了5的倍数的分钟
def timeIs5():
    now = datetime.now().strftime('%H:%M:%S')
    now = now.split(':')
    now = [int(i) for i in now]
    if now[1] % 5 == 0 and now[2] == 0:
        return True
    else:
        return False


# 判断是否到了11:50
def timeIs1150():
    now = datetime.now().strftime('%H:%M:%S')
    now = now.split(':')
    now = [int(i) for i in now]
    if now[0] == 11 and now[1] == 50 and now[2] == 0:
        return True
    else:
        return False


# 判断是否到了11:00
def timeIs1100():
    now = datetime.now().strftime('%H:%M:%S')
    now = now.split(':')
    now = [int(i) for i in now]
    if now[0] == 11 and now[1] == 00 and now[2] == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    now = datetime.now()
    print("当前时间为:", now.strftime('%H:%M:%S'))
    print("距离下班还剩:", timeFormat(timeSubtraction('18:30', now.strftime('%H:%M'))), '\n')
    content = '反卷先锋下班倒计时系统已启动\n当前时间为:' + now.strftime('%H:%M:%S') + '\n距离下班还剩:' + timeFormat(
        timeSubtraction('18:30', now.strftime('%H:%M')))
    xiaBanBot(content)
    while not timeIsUp():
        if timeIs5():
            now = datetime.now()
            # 距离下班时间不到一小时
            if timeLeftIn1H():
                time.sleep(1)
                time_left = timeSubtraction('18:30', now.strftime('%H:%M'))
                print(timeFormat(time_left))
                # 距离下班剩30分钟
                if time_left[1] == 30:
                    content = 'Hi, 我是机器人反卷先锋001\n温馨提示，距离下班仅剩30分钟，为今天的工作收个尾吧。'
                    xiaBanBot(content)
                # 距离下班剩15分钟
                elif time_left[1] == 15:
                    content = 'Hi, 我是机器人反卷先锋001\n温馨提示，距离下班仅剩15分钟，想想晚饭吃啥好。'
                    xiaBanBot(content)
                # 距离下班剩5分钟
                elif time_left[1] == 5:
                    content = 'Hi, 我是机器人反卷先锋001\n温馨提示，距离下班仅剩5分钟，去趟厕所吧，准备下班。'
                    xiaBanBot(content)
            # 距离下班时间超过一小时
            else:
                # 判断是否到外卖时间
                if timeIs1100():
                    content = 'Hi, 我是机器人反卷先锋001\n温馨提示，现在11点了，可以考虑点外卖了。'
                    xiaBanBot(content)
                    print("外卖时间到!")
                # 判断是否到午饭时间
                elif timeIs1150():
                    content = '干饭时间到！！！'
                    xiaBanBot(content)
                    print("吃饭时间到!")
                time.sleep(1)
                # print("当前时间为:", now.strftime('%H:%M:%S'))
                # print("距离下班还剩:", timeFormat(timeSubtraction('18:30', now.strftime('%H:%M'))), '\n')
        else:
            continue
    # content = 'Hi, 我是机器人反卷先锋001\n温馨提示，下班时间到了，请速速离开公司。'
    # xiaBanBot(content)

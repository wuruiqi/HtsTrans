# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 16:39:24 2017

@author: QQ
"""

import serial
import time
import array
t = serial.Serial('com3',9600)  # 配对码默认 1234
while True:
    count = t.inWaiting()
    if count !=0:
        recv = t.read(count)
        print recv
        t.flushInput()
        time.sleep(0.1)
    else:
        break
    
def executcmd(cmd_int):
    a= array.array('B',cmd_int)
    for x in a:
        t.write(a)
t.close


def getControl(cmd):
    angle = cmd['jointAngle'][0:16]
    runtime =  cmd['runTime']/20
    nextTime = cmd['totalTime']/20-2
    parameters_list = []
    for x in angle:   #  放入16个关节的角度值
        parameters_list.append(x)
    parameters_list.append(runtime % 256)     # 放入运行时间
    parameters_list.append(nextTime/256)      # 放入允许下帧允许的高位
    parameters_list.append(nextTime%256)      # 放入允许下帧允许的低位
    return parameters_list

def packageCommand(parameters,cmdType):
    type2Number={'handShake':1, 'multiControl':35}
    cmd_list = [251,191]      # 先放入命令头 FB=251  BF=191
    cmd_list.append(len(parameters)+5)  # 放入长度 1字节 ,等于参数长度 +5 ，5个字节分别是（FB BF 长度 命令 check）
    cmd_list.append(type2Number[cmdType])   #放入命令代码
    for x in parameters:       # 放入参数数据
        cmd_list.append(x)
    checkSum = 0    
    for x in cmd_list[2:]:
        checkSum += x
    cmd_list.append(checkSum%256)   # 放入check码
    cmd_list.append(237)       # 放入结束标志ED = 237
    return cmd_list

def TransCmd(cmd):
    parameters = getControl(cmd)
    parameters =[0];
    cmd_int = packageCommand(parameters,'multiControl')
    cmd_int = packageCommand(parameters,'handShake')
    return cmd_int

cmd ={'actionAmount': 188,
 'actionFlag': 1,
 'actionID': 1,
 'check': '14',
 'jointAngle': [87,
  26,
  49,
  92,
  155,
  126,
  90,
  60,
  76,
  110,
  89,
  90,
  120,
  104,
  70,
  90,
  90,
  90,
  90,
  90],
 'runTime': 1200,
 'totalTime': 5600}
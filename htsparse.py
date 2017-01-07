# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 11:39:31 2017

@author: QQ
"""

import binascii
import csv

filepath = "c:\\xiao.hts"
with open(filepath,"rb") as f:
    file_str = f.read()
poffset = 0 
csv_path = file('C:\\command.csv','wb')
writer = csv.writer(csv_path)
writer.writerow(['action_group','action_sum','action_id','joint_angle','runtime','next_time'])
while poffset < len(file_str):
    try:
        poffset= file_str.index('\xfb\xbf',poffset+1)
        command = map(binascii.b2a_hex,file_str[poffset:poffset+33])
        cmd= cmdparse(command)
        writercmd = (cmd['action_group'],cmd['action_sum'],cmd['action_id'],cmd['joint_angle'],cmd['runtime'],cmd['next_time'])
        writer.writerow(writercmd)
    except ValueError,e:
        print "最后一个命令抵制",poffset+33
        break
csv_path.close()

def cmdparse(str_file):     # hts文件命令解析
    cmd_dict = {'action_group':[],'action_sum':0,'action_id':0,'joint_angle':[],'runtime':0,'next_time':0,'check':'\x00'}
    cmd_dict['action_group'] = map(lambda a:int(a,16),str_file[2:4])
    cmd_dict['action_sum'] = twoByteTrans( map(lambda a:int(a,16),str_file[4:6]))
    cmd_dict['action_id'] = twoByteTrans( map(lambda a:int(a,16),str_file[6:8]))
    cmd_dict['joint_angle'] = map(lambda a:int(a,16),str_file[8:28])
    cmd_dict['runtime'] = twoByteTrans( map(lambda a:int(a,16),str_file[28:30]))
    cmd_dict['next_time'] = map(lambda a:int(a,16),str_file[30:31])
    cmd_dict['check'] = str_file[32]
    return cmd_dict

def twoByteTrans(x):
    if x[1]!=0:
        return x[0]+x[1]*255
    else :
        return x[0]
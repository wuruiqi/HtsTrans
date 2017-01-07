# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 11:39:31 2017

@author: QQ
"""

import binascii
import csv
import sys
import getopt
import os
def cmdparse(str_file,cmd_dict):     # hts文件命令解析    
    cmd_dict['actionFlag'] = int(str_file[3],16)
    cmd_dict['actionAmount'] = twoByteTrans( map(lambda a:int(a,16),str_file[4:6]))
    cmd_dict['actionID'] = twoByteTrans( map(lambda a:int(a,16),str_file[6:8]))
    cmd_dict['jointAngle'] = map(lambda a:int(a,16),str_file[8:28])
    cmd_dict['runTime'] = int(str_file[28],16)*20
    cmd_dict['totalTime'] = (int(str_file[29],16)*255+int(str_file[30],16)+2)*20
    cmd_dict['check'] = str_file[31]
    return cmd_dict

def twoByteTrans(x):        # 高位低存数据转换
    if x[1]!=0:
        return x[0]+x[1]*255
    else :
        return x[0]
   
def hts2csv(htsfile,csvfile) :
    #filepath = "c:\\xiao.hts"
    with open(htsfile,"rb") as f:
        file_str = f.read()
    poffset = 0 
    touch_csv = file(csvfile,'wb')
    writer = csv.writer(touch_csv)
    writer.writerow(['actionFlag','actionAmount','actionID','jointAngle','runTime','totalTime'])
    cmd_dict = {'actionFlag':0,'actionAmount':0,'actionID':1,'jointAngle':[],'runTime':0,'totalTime':0,'check':'\x00'}
    while cmd_dict['actionAmount'] != cmd_dict['actionID'] :      # 动作组标志为3时，说明读到最后一个动作了。
        try:
            poffset= file_str.index('\xfb\xbf',poffset+1)
            command = map(binascii.b2a_hex,file_str[poffset:poffset+33])
            cmd= cmdparse(command,cmd_dict)
            writercmd = (cmd['actionFlag'],cmd['actionAmount'],cmd['actionID'],cmd['jointAngle'],cmd['runTime'],cmd['totalTime'])
            writer.writerow(writercmd)
        except ValueError,e:
               print 'ValueError:' , e
               break
    touch_csv.close()
    print u"%s转换成功,共有动作%d，转换动作%d" %(htsfile,cmd_dict['actionAmount'],cmd_dict['actionID'])

def batchTans(input_dir,output_dir):
    pass
def usage():
    print '-h,--help: print help message.'
    print '-i, -i: input file path'
    print '-o, -o:output file path'

def main (argv=None):   
    if argv is None:
        argv = sys.argv
    opts, args = getopt.getopt(argv[1:],"hv:i:o:")  # opts为分析出的格式信息。args为不属于格式信息的剩余的命令行参数。opts是一个两元组的列表。每个元素为：(选项串,附加参数)。如果没有附加参数则为空串''。
    input_file= None
    output_file= None
    for op , value in opts:
        if not op:
            usage()
            sys.exit()
        if op == "-i":
            input_file = value
        elif op == "-o":
            output_file = value
        elif op == "-h":
            usage()
            sys.exit()
    if input_file is None or output_file is None :
        print u"无输入或输出参数"
        sys.exit()
    print u'\n输入文件为：%s\n输出文件为:%s' %(input_file, output_file)
    hts2csv(input_file,output_file)
    
if __name__ == '__main__' :
    sys.exit(main())

            
            
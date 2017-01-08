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
   
def hts2csv(htsfile,csvfile) :    # hts文件转换为csv文件
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
    print "%s translation success,Total %d actions" %(os.path.split(htsfile)[1],cmd_dict['actionAmount']) 

def batchTrans(input_dir,output_dir=None):  #批量转换hts文件为csv文件
    if os.path.isdir(input_dir) is False:
        print u"输入文件夹路径无效，请输入正确路径"
        sys.exit()
    if output_dir is None:     # 不指定目录的，则自动转换在hts文件下面。指定目录暂无法复制hts目录架构。
        output_dir = input_dir
    elif os.path.isdir(output_dir) is False:
        print u"输出文件夹路径无效，请输入正确路径"
        sys.exit()
    for parent,dirnames,filenames in os.walk(input_dir):
        for filename in filenames:
            basename,extname = os.path.splitext(filename)
            if extname == '.hts':
                output_file = os.path.join(output_dir , basename + '.csv')
                input_file = os.path.join(parent,filename)
                hts2csv(input_file,output_file)
                print "inpuuname is:" + input_file
                print "outputname is:" + output_file

def usage():   # 参数说明
    print '-h,--help: print help message.'
    print '-i, -input: input file path'
    print '-o, -output:output file path'
    print '--outputdir, outputdir:output dir path'
    print '--inputdir, -inputdir:input dir path'

def main (argv=None):    # 程序主入口
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:],"hv:i:o:",["help","input=","inputdir=","output=","outputdir="])  # opts为分析出的格式信息。args为不属于格式信息的剩余的命令行参数。opts是一个两元组的列表。每个元素为：(选项串,附加参数)。如果没有附加参数则为空串''。
    except getopt.GetoptError:
        print u"参数无效,可用参数如下："
        sys.exit(usage())
    input_file= None
    output_file= None
    input_dir = None
    output_dir = None
    for op , value in opts:
        if op in ("-i","--input"):
            input_file = value
        elif op in ("-o","--output"):
            output_file = value
        elif op in ("--inputdir"):
            input_dir = value
        elif op in ("--outputdir"):
            output_dir = value
        elif op in ("-h","--help"):
            sys.exit(usage())
        else:
            sys.exit(usage())
    if input_file is None or output_file is None:
        if os.path.isdir(input_dir) is True:  # 判断文件夹路径合法性
            batchTrans(input_dir,output_dir)
        else :
            print u"没有输入有效的文件\文件夹地址"
    elif os.path.splitext(input_file)[1] != '.hts' or os.path.splitext(output_file)[1] != '.csv':  # 判断输入输出文件是否为hts 和csv格式
        print u"输入的文件路径无效，请输入hts文件，输出csv文件"
    else :
        print '\n input file is : %s\n out put file is : %s' %(input_file, output_file)   # str 无法和print u''一块儿用，只能暂时用英文咯。
        hts2csv(input_file,output_file)
    
if __name__ == '__main__' :
    sys.exit(main())

            
            
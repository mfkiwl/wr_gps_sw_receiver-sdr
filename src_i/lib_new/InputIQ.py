#!/usr/bin/python3
# -*- coding: UTF-8 -*- 

import numpy
import matplotlib.pyplot as plt
import datetime

data_format={
    b'0':1,
    b'2':3,
    b'4':5,
    b'6':7,
    b'8':-1,
    b'a':-3,
    b'c':-5,
    b'e':-7
}

class InputIQ(object):
    """docstring for InputIQ"""
    def __init__(self, filename):
        super(InputIQ, self).__init__()
        self.file = open(filename,"rb")
        self.loc = 0
        self.time = 0

    def read(self,size):
        LIST=[]
        TIME_LIST=[]
        for i in range(size):
            if self.loc%1257 == 0:
                tai = self.file.read(8)
                cycles = self.file.read(7)
                I = self.file.read(1)
                self.loc += 8
                tmp_ns = int(cycles,16)*8
                tmp_s = int(tai,16)
                period = tmp_s*1e9 + tmp_ns - self.time
                if (self.time!=0) and (period!=64):
                    print("Data lose!")
                    break
                self.time = tmp_s*1e9 + tmp_ns
            else:
                self.loc += 1
                tmp = self.file.read(1)
                I = self.file.read(1)
                self.time += 64
            
            I_BIN= data_format[I]
            LIST.append(I_BIN)
            TIME_LIST.append(self.time)
        return LIST, TIME_LIST
    
    def reset(self,loc=0):
        self.file.seek(loc*2*1257)
        self.loc = loc*2*1257
        self.time = 0

    def __del__(self):
        self.file.close()

def main():
    IQ_input = InputIQ("../../../raw/gps_adc_192.168.0.2test0")
    IQ_input.reset(1257*15625)
    IQ_input.read(10)
    
if __name__ == '__main__':
    main()

from calendar import month
import datetime
import numpy as np
from sys import argv
import matplotlib.pyplot as plt

def size_type(b1,b2):
    a1=int.from_bytes(b1,"little")
    a2=int.from_bytes(b2,"little")
    if a2==4660:
        return a1,0
    elif a2==22136:
        return a1,1
    elif a2==43690:
        return a1,2
    else:
        return a1,3

def to_int(byte,signed=False):
    return int.from_bytes(byte,"little",signed=signed)

def to_string(byte):
    #assert(len(byte)%2==0)
    return str(byte,"iso8859_2")


class Record():

    def get_header(self,bytes):
        self.SamplingPeriod=to_int(bytes[0:2])
        year=to_int(bytes[64:66],True)
        month=to_int(bytes[66:68],True)
        day=to_int(bytes[68:70],True)
        hour=to_int(bytes[70:72],True)
        min=to_int(bytes[72:74],True)
        sec=to_int(bytes[74:76],True)
        microsec=to_int(bytes[76:80])
        self.time_start=datetime.datetime(year,month,day,hour,min,sec,microsec)

    def get_data(self,bytes):
        year=to_int(bytes[12:14],True)
        month=to_int(bytes[14:16],True)
        day=to_int(bytes[16:18],True)
        hour=to_int(bytes[18:20],True)
        min=to_int(bytes[20:22],True)
        sec=to_int(bytes[22:24],True)
        microsec=to_int(bytes[24:28])
        time_0=datetime.datetime(year,month,day,hour,min,sec,microsec)
        bytes=bytes[28:]
        for i in range(len(bytes)//4):
            c1=bytes[4*i:4*i+2]
            c2=bytes[4*i+2:4*i+4]
            #print(len(c1),len(c2))
            self.chanel1.append(to_int(c1,True))
            self.chanel2.append(to_int(c2,True))
            self.date.append(time_0+datetime.timedelta(microseconds=i*20))
    def __init__(self,name):
        f=open(name,"rb")
        self.strings=[]
        self.chanel1=[]
        self.chanel2=[]
        self.trigger=[]
        self.date=[]
        self.pps=[]
        while True:
            b1=f.read(2)
            if b1==b'':
                break
            b2=f.read(2)
            a1,a2=size_type(b1,b2)
            temp=f.read(a1-4)
            if a2==0:
                print("getting header")
                self.get_header(temp)
            elif a2==2:
                self.strings.append(to_string(temp))
            elif a2==1:
                self.get_data(temp)
        f.close()
        self.chanel1=np.array(self.chanel1)
        self.chanel2=np.array(self.chanel2)
        self.ellapsed=np.array(list(map(lambda x:(x-self.time_start).total_seconds(),self.date)))

if __name__ == "__main__":
    t=Record(argv[1])
    print(t.strings)
    print(t.time_start)
    plt.plot(t.ellapsed,t.chanel2)
    plt.savefig("test.jpg")

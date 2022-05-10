import csv
#import matplotlib
import subprocess
from tkinter import CENTER
import speedtest
import os

def speedTest():
   
    i=0
    st = speedtest.Speedtest()
    bruh=st.get_best_server()
    print("Server info: ")
    for b in bruh.items():
        a,c=b
        print(str(a) + "-" + str(c))
           
        
    print("\n\n")
    print(f"Your ping is: {st.results.ping} ms")
    print(f"Your download speed: {round(st.download() / 1000 / 1000, 1)} Mbit/s")
    print(f"Your upload speed: {round(st.upload() / 1000 / 1000, 1)} Mbit/s")

    

def dnsTest():
    #flush antes de mandat query
    pass

def ftpTest():
   
    pass
def wifiTest():
        process = subprocess.run(["airport", "en0", "--scan"],
                         check=True,
                         stdout=subprocess.PIPE,
                         universal_newlines=True)
        print(process)
 

def speedTestloop():
    pass

def dnsTestloop():
    pass

def ftpTestloop():
    pass

def showstats1():
    pass

def showstats2():
    pass

def showstats3():
    pass


if __name__ == "__main__":
   x=0
   op=1
   while(op):
        print("Selecione a opção desejada: ")
        print("1  SpeedTest")
        print("2  DnsTest")
        print("3  FtpTeste")
        print("0 para sair") 
        x=int(input())
        if(x==1):
           speedTest()
        elif(x==2):
            import testdns  
        elif(x==3):
            print(1)
        elif(x==0):
            op=x
        else:
            pass
        
        os.system('cls||clear')    
   



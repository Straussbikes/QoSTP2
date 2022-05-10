import csv
#import matplotlib
import subprocess
from tkinter import CENTER
import speedtest
import speedtest1 as sp
import os

def speedTest(flag):
    servers=[]
    i=0
    st = speedtest.Speedtest()   
    bruh=st.get_best_server()
    print("Server info: ")
    if(flag):
        for b in bruh.items():
            a,c=b
            print(str(a) + "-" + str(c))
            
            
        print("\n\n")
        print(f"Ping : {st.results.ping} ms")
        print(f"Download speed: {round(st.download() / 1000 / 1000, 1)} Mbit/s")
        print(f"Upload speed: {round(st.upload() / 1000 / 1000, 1)} Mbit/s")
    else:
        return (st.results.ping,{round(st.download() / 1000 / 1000, 1)},{round(st.upload() / 1000 / 1000, 1)})
    


def ftpTest():
   
    pass
def wifiTest():
        process = subprocess.run(["airport", "en0", "--scan"],
                         check=True,
                         stdout=subprocess.PIPE,
                         universal_newlines=True)
        print(process)
 
 
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
   op="1"
   while(op=="1"):
        print("Selecione a opção desejada: ")
        print("1  SpeedTest server otimo")
        print("2  DnsTest")
        print("3  FtpTeste")
        print("4  SpeedTest para CSV")
        print("0 para sair") 
        x=input()
        if(x=="1"):
            os.system('cls||clear')
            speedTest(1)
            bruh=1
            while(bruh):
                print("selecione 0 para voltar atras") 
                bruh=input() 
                os.system('cls||clear') 
                if(bruh=="0"):
                    break
                else: 
                    print("opcao nao reconhecida")
                     
        elif(x=="2"):
            os.system('cls||clear')
            import testdns  
        elif(x=="3"):
            os.system('cls||clear')
            pass
        elif(x=="4"):
             os.system('cls||clear')  
             sp.main()
             bruh=1
             while(bruh):
                print("selecione 0 para voltar atras") 
                bruh=input() 
                os.system('cls||clear') 
                if(bruh=="0"):
                    break
                else: 
                    print("opcao nao reconhecida")
                          
                    
                    
        elif(x=="0"):
            os.system('cls||clear')
            op=x
        else:
            os.system('cls||clear')
            print("Opção nao reconhecida")
            
        
           
   



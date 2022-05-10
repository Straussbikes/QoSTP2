import speedtest
from datetime import datetime

def test():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    return res["download"], res["upload"], res["ping"]


def main():
    # write to csv
   
            print("Especifique o numero de testes")
   
            bruh=int(input())
            # csv file
            with open('file.csv', 'a') as f:
                f.write('download,upload,ping\n')
                
                for i in range(bruh):
                    print('A fazer o teste #{}'.format(i+1))
                    d, u, p = test()
                  
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    f.write('{},{},{},{}\n'.format(d, u, p,current_time))
                        
            # txt file
            with open('file.txt', 'w') as f:
                for i in range(bruh):
                    print('A fazer o teste #{}'.format(i+1))
                    d, u, p = test()
                    f.write('Teste #{}\n'.format(i+1))
                    f.write('Download: {:.2f} Kb/s\n'.format(d / 1024))
                    f.write('Upload: {:.2f} Kb/s\n'.format(u / 1024))
                    f.write('Ping: {}\n'.format(p))
            # stdout
            for i in range(bruh):
                d, u, p = test()
                print('Teste #{}\n'.format(i+1))
                print('Download: {:.2f} Kb/s\n'.format(d / 1024))
                print('Upload: {:.2f} Kb/s\n'.format(u / 1024))
                print('Ping: {}\n'.format(p))
        



import dns.resolver
import socket
from datetime import datetime
import os
import csv
import glob
import matplotlib.pyplot as plt
import pandas as pd

# Guardar histórico de pesquisas para depois aproveitarmos estatísticas
nameservers_history = {}
path = "stat_files"
main_directoy = os.getcwd()

mainMenu_options = {
    1: 'Choose HostName to test',
    2: 'Get Statistical Data from known Hostname',
    3: 'Exit App'
}

query_options = {
    1: 'Type A (IPv4)',
    2: 'Type AAAA (IPv6)',
    3: 'Type NS (An authoritative name server)',
    4: 'Type MX (A mail exchange)',
    5: 'Type TXT (text strings)',
    6: 'Type CNAME (Domain Name Alias)',
    7: 'Exit to Main Menu'
}



# -------------------- File treatment -----------------------

def createFile(hostname):
    if not os.path.exists(path):
        os.makedirs(path)

    file = os.path.join(path, hostname)
    filename = file.rstrip() + '.csv'
    header = ('Query','Start_time','Task_time (ms)')
    writerFile(header,[],filename,"create")
    return filename


# option de criar ou então dar update com nova row
def writerFile(header,data, filename_path,option):
    if option == 'create':
        with open(filename_path,'w') as csvfile:
            cenas = csv.writer(csvfile)
            cenas.writerow(header)
    else:
        with open(filename_path, 'a') as csvfile:
            w = csv.writer(csvfile)
            for x in data:
                w.writerow(x)

# -------------------- DNS Queries --------------------------

def option_query(queryType,hostname):
    print('---------------------------------------------^')
    print('HOSTNAME ' + hostname + ' :')

    resolver = dns.resolver.Resolver()

    # clear cache para real pesquisa dns
    print('--------------Flushing Cache-----------------^')
    os.system('ipconfig/flushdns')


    # start time
    queryStartTime = datetime.now()

    try:
        answer = resolver.resolve(hostname, queryType)

    except dns.rdatatype.UnknownRdatatype:
        print('Unkown DNS response - ' + queryType + ' @' + hostname)
        answer = ''

    except dns.resolver.NoAnswer:
        # No answer from DNS server
        print('No DNS answer - ' + queryType + ' @' + hostname)
        answer = ''

    except dns.exception.Timeout:
        # DNS Server timed out
        print('DNS Timeout - ' + queryType + ' @' + hostname)
        answer = ''

    except dns.resolver.NXDOMAIN:
        # NXDOMAIN response from DNS server
        print('NXDOMAIN response - ' + queryType + ' @' + hostname)
        answer = ''

    except dns.resolver.NoNameservers:
        # If there are no responses from name servers, display No Response.
        print('No response. ' + queryType + ' @' + hostname)
        answer = ''

    queryEndTime = datetime.now()

    # Calculate the difference between End Query Time and Start Query Time
    # Multiply the result by a 1000 to get millisecond response.
    queryTime = (queryEndTime - queryStartTime).total_seconds() * 1000

    # Format the queryTime response.
    s_queryTime = str("{:.1f}".format(queryTime))

    nameservers_history[hostname].append([queryType, queryStartTime, s_queryTime])

    print('---------------------------------------------^')
    for response in answer:
        if queryType == 'CNAME':
            queryResponse = response.target
            print('RESULT cname target address: ' ,queryResponse)
        elif queryType == 'AAAA':
            queryResponse = response.to_text()
            print('RESULT IPv6 address: '+ queryResponse)
        elif queryType == 'A':
            queryResponse = response.to_text()
            print('RESULT IPv4 address: ' + queryResponse)
        elif queryType == 'MX':
            print('RESULT Host ',response.exchange,'has preference ',response.preference)
        elif queryType == 'NS':
            for ans in answer.response.answer:
                for item in ans.items:
                   print( 'RESULT NS query: '+ item.to_text())
        elif queryType == 'TXT':
            queryResponse = response.to_text()
            print('RESULT TXT query: ' + queryResponse)

    print('---------------------------------------------^')
    print('Time taken: ' + s_queryTime + ' ms')
    print('---------------------------------------------^\n')

    data = [(queryType,str(queryStartTime),str(s_queryTime))]
    file = os.path.join(path, hostname + '.csv' )
    writerFile([],data,file,"update")


# -------------------- MainMenu and SubMenus --------------------------

def option_hostname(hostname):
    h = hostname.rstrip()
    while(True):
        print("---------------<CHOOSE QUERY>-----------------")
        for key in query_options.keys():
            print(key, '--', query_options[key])
        option = ''
        try:
            option = int(input('\nEnter your choice for Query Type or Exit: '))
        except:
            print('Wrong input. Please enter a number ...')
        # Check what choice was entered and act accordingly
        if option == 1: # A
            os.system('cls||clear')
            option_query('A',h)
        elif option == 2: # AAAA
            os.system('cls||clear')
            option_query('AAAA',h)
        elif option == 3: # NS
            os.system('cls||clear')
            option_query('NS',h)
        elif option == 4: # MX
            os.system('cls||clear')
            option_query('MX',h)
        elif option == 5: # TXT
            os.system('cls||clear')
            option_query('TXT',h)
        elif option == 6: # CNAME
            os.system('cls||clear')
            option_query('CNAME',h)
        elif option == 7:
            os.system('cls||clear')
            print('Going to Main Menu')
            break
        else:
            os.system('cls||clear')
            print('INVALID OPTION. Please enter a number between 1 and 9...')


# MainMenu
def print_mainMenu():
    os.system('cls||clear')
    print("---------------<MAIN MENU APP>-----------------")
    for key in mainMenu_options.keys():
        print(key, '--', mainMenu_options[key] )


# Files Available Menu
def print_FileStatMenu():
    os.chdir("stat_files/")
    index = 1
    files = {}
    for file in glob.glob("*.csv"):
        files[index] = file
        index += 1
    while (True):
        for key in files.keys():
            print(key, '--', files[key])
        print(index, '-- Average A query for all files')
        print(index+1, '-- Exit')
        option = ''
        try:
            option = int(input('\nEnter your choice for File or Exit: '))
        except:
            print('Wrong input. Please enter a number ...')

        if option == index+1:
            os.system('cls||clear')
            # TENHO DE ALTERAR ISTO PARA VIR
            os.chdir(main_directoy)
            print('Going to Main Menu')
            break

        elif option == index:
            os.system('cls||clear')
            getAqueryStatsAll(files.values())

        else:
            os.system('cls||clear')
            fd = pd.read_csv(files[option])
            types_q = queriesPerFile(fd)
            try:
                print_querieByFile(files[option],fd,types_q)
            except:
                break


# Queries By File Available Menu
def getAqueryStatsAll(files):
    queriebyfile = {}
    for fi in files:
        df = pd.read_csv(fi)
        query_a = df.loc[df['Query'] == 'A']
        queriebyfile[fi] = query_a

    # fazer média de cada ficheiro

    medias = {}
    for ft in queriebyfile:
        sum = 0
        results = queriebyfile[ft]
        for t in results['Task_time(ms)']:
            sum += t
        medias[ft] = sum/len(results['Task_time(ms)'])

    #desenhar gráfico de media de cada ficheiro
    # creating the dataset
    type_q = list(medias.keys())
    values = list(medias.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    bars = plt.bar(type_q, values, color='maroon',
            width=0.4)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval + .05, yval)
    plt.xlabel("Name Domains")
    plt.ylabel("Tempo Medido(ms)")
    plt.title("Tempo de resposta média a para cada domínio requisitado")
    plt.show()


def print_querieByFile(filename,fileDataframe, queries):
    dq = {}
    while (True):
        index = 1
        for q in queries:
            print(index, '--', q)
            dq[index] = q
            index+=1
        print(index, '-- Exit')
        option = ''
        try:
            option = int(input('\nEnter your choice for Query Statistic or Exit: '))
        except:
            print('Wrong input. Please enter a number ...')

        if option == index:
            os.system('cls||clear')
            print('Going to File Menu')
            break
        else:

            try:
                showQueryBarPlot(filename,fileDataframe, dq[option])
                os.system('cls||clear')

            except:
                os.system('cls||clear')
                break


# ----------------------- Métodos de estatísticas por query -----------------------

# Dá-me uma lista de queries feitas num nome de dominio
def queriesPerFile(file):
    queries = file['Query'].unique().tolist()
    return queries


# Apresenta um bar plot do ficheiro e da query requerida
def showQueryBarPlot(filename,fileDF,query):
    query_a = fileDF.loc[fileDF['Query'] == query]
    start_t = query_a['Start_time'].tolist()
    task_t = query_a['Task_time(ms)'].tolist()

    different_dates = {}
    for i, s in enumerate(start_t):
        # print(i, s)
        date_time_obj = datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')
        # getalldates[date_time_obj] = task_t[i]
        if str(date_time_obj.date()) not in different_dates:
            different_dates[str(date_time_obj.date())] = [0, 0]

        different_dates[str(date_time_obj.date())][0] += 1
        different_dates[str(date_time_obj.date())][1] += task_t[i]



    median_date = {}
    for d in different_dates:
        median_date[d] = round((different_dates[d][1] / different_dates[d][0]),2)



    type_q = list(median_date.keys())
    values = list(median_date.values())

    # Figure Size
    fig, ax = plt.subplots(figsize=(10, 5))



    # creating the bar plot
    bars = plt.bar(type_q, values, color='blue',
            width=0.4)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval + .05, yval)

    plt.title('Valores de tempo medido para ' + filename + ' em query ' + query)
    plt.xlabel('Data de Medição')
    plt.ylabel('Tempo medido(ms)')


    plt.show()


# ----------------------- Main Loop -----------------------

while True:
    print_mainMenu()
    option = ''
    try:
        option = int(input('Enter your choice: '))
    except:
        os.system('cls||clear')
        print('Wrong input. Please enter a number ...')
    # Check what choice was entered and act accordingly
    if option == 1:
        hostname = input("Enter the Domain Name: ")
        file_path = os.path.join(path, hostname + '.csv')
        file = hostname + '.csv'
        if not os.path.isfile(file_path):
            createFile(hostname)

        os.system('cls||clear')

        if hostname not in nameservers_history:
            nameservers_history[hostname] = [[]]
            option_hostname(hostname)
        else:
            option_hostname(hostname)

    elif option == 2:
        os.system('cls||clear')
        print_FileStatMenu()

    elif option == 3:
        os.system('cls||clear')
        print('Thanks for using APP !!')
        exit()
    else:
        os.system('cls||clear')
        print('Invalid option. Please enter a number between 1 and 2...')





























import dns.resolver
import socket
from datetime import datetime, timedelta
import os
import csv
from tempfile import NamedTemporaryFile

# Guardar histórico de pesquisas para depois aproveitarmos estatísticas
nameservers_history = {}
nameservers_query = {}


#hostname= input("Nome de Dominío a testar: ")
def queryTimeDNS(hostn,queryType,queryName):
    # Set the DNS Server
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [socket.gethostbyname(hostn)]

    queryStartTime = datetime.now()
    try:
        if queryType == "ptr":
            answer = resolver.resolve(queryName)
        else:
            answer = resolver.resolve(queryName, queryType)

            # End query time.
    except:
        pass

    queryEndTime = datetime.now()

    # Calculate the difference between End Query Time and Start Query Time
    # Multiply the result by a 1000 to get millisecond response.
    queryTime = (queryEndTime - queryStartTime).total_seconds() * 1000

    # Format the queryTime response.
    s_queryTime = str("{:.1f}".format(queryTime))

###################################################################3

path = "stat_files"

mainMenu_options = {
    1: 'Choose HostName to test',
    2: 'Exit DnsTest'
}

query_options = {
    1: 'Type A (IPv4)',
    2: 'Type AAAA (IPv6)',
    3: 'Type PTR (Domain Name pointer)',
    4: 'Type NS (An authoritative name server)',
    5: 'Type MX (A mail exchange)',
    6: 'Type TXT (text strings)',
    7: 'Type SRV (Service Record)',
    8: 'Type NAPTR (Naming authority pointer)',
    9: 'Type CNAME (Domain Name Alias)',
    10: 'Exit to Main Menu'
}

# -------------------- File treatment -----------------------

def createFile(hostname):
    if not os.path.exists(path):
        os.makedirs(path)

    file = os.path.join(path, hostname)
    filename = file.rstrip() + '.csv'
    header = ('Query','Start_time','Task_time')
    writerFile(header,[],filename,"create")
    return filename


# option de criar ou então dar update com nova row
def writerFile(header,data, filename_path,option):
    print("FILENAME_PATH",filename_path)
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
    queryStartTime = datetime.now()
    resolver = dns.resolver.Resolver()

    try:
        if queryType == "ptr":
            answer = resolver.resolve(queryType)
        else:
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

    #print('ANSWER: ' + answer + '\nTime taken: ' + s_queryTime)
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
        elif queryType == 'TXT':
            queryResponse = response.to_text()
            print('RESULT TXT query: ' + queryResponse)
    print('---------------------------------------------^')
    print('Time taken: ' + s_queryTime + ' ms')
    print('---------------------------------------------^')

    data = [(queryType,str(queryStartTime),str(s_queryTime))]
    file = os.path.join(path, hostname + '.csv' )
    writerFile([],data,file,"update")

def option_hostname(hostname):
    h = hostname.rstrip()
    while(True):
        print("---------------<CHOOSE QUERY>-----------------")
        for key in query_options.keys():
            print(key, '--', query_options[key])
        option = ''
        try:
            option = int(input('Enter your choice for Query Type: '))
        except:
            print('Wrong input. Please enter a number ...')
        # Check what choice was entered and act accordingly
        if option == 1: # A
            os.system('cls||clear')
            option_query('A',h)
        elif option == 2: # AAAA
            os.system('cls||clear')
            option_query('AAAA',h)
        elif option == 3: # PTR
            os.system('cls||clear')
            option_query('PTR',h)
        elif option == 4: # NS
            os.system('cls||clear')
            option_query('NS',h)
        elif option == 5: # MX
            os.system('cls||clear')
            option_query('MX',h)
        elif option == 6: # TXT
            os.system('cls||clear')
            option_query('TXT',h)
        elif option == 7: # SRV
            os.system('cls||clear')
            option_query('SRV',h)
        elif option == 8: # NAPTR
            os.system('cls||clear')
            option_query('naptr',h)
        elif option == 9: # CNAME
            os.system('cls||clear')
            option_query('CNAME',h)
        elif option == 10:
            os.system('cls||clear')
            print('Thanks message before exiting')
            break
        else:
            os.system('cls||clear')
            print('INVALID OPTION. Please enter a number between 1 and 10...')



def print_mainMenu():
    print("---------------<MAIN MENU DnsTest>-----------------")
    for key in mainMenu_options.keys():
        print(key, '--', mainMenu_options[key] )


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
        print('Thanks for using APP !!')
        break
    else:
        os.system('cls||clear')
        print('Invalid option. Please enter a number between 1 and 2...')





























import os.path
from CreateRRD import create
from getSNMP import consultaSNMP

def inicio(file):
    file_dispositivos = open(file)
    dispositivo = file_dispositivos.readline().split()
    while(dispositivo):
        if(consultaSNMP(dispositivo[2],dispositivo[0],'1.3.6.1.2.1.1.1.0') is None):
            print(dispositivo, 'is down')
        else:
            print(dispositivo, 'is up')
            interfaces = int(consultaSNMP(dispositivo[2], dispositivo[0], '1.3.6.1.2.1.2.1.0'))
            print('Interfaces: ', interfaces)
            for x in range(1,interfaces+1):
                status = ['up','down','testing']
                print('\tInterface: ',x)
                print('\tSatus: ', status[int(consultaSNMP(dispositivo[2], dispositivo[0], '1.3.6.1.2.1.2.2.1.7.'+str(x)))-1])
                descrip = consultaSNMP(dispositivo[2], dispositivo[0], '1.3.6.1.2.1.2.2.1.2.'+str(x))
                if(descrip[0:2]=='0x'):
                    descrip = bytes.fromhex(descrip[2:]).decode('ASCII')
                print('\tDescription: ', descrip)

            if(not os.path.exists('./baseD/'+dispositivo[4]+'.rrd')):
                create(dispositivo[4])

        dispositivo = file_dispositivos.readline().split()

    file_dispositivos.close()
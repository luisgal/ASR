import os
from CreateRRD import create

def alta(file):
    print('Para agregar un dispositivo asegurate de utilizar el siguiente formato: ')
    print('\t[hostName o iPAdress] -[version] [comunityName] [port] [name]')
    print('NOTA: [name] es una sola palabra')

    print('Dispositivo: ', end='')
    newDisp = input()
    file_dispositivos = open(file, 'a')
    file_dispositivos.write(newDisp)
    file_dispositivos.write('\n')
    file_dispositivos.close()
    create(newDisp.split()[4])

def baja(file):
    print('Eliminar un dispositivo, inserta hostName o iPAdress: ', end='')
    host = input()

    file_dispR = open(file, 'r')
    dispositivos = []
    disp = file_dispR.readline()
    while (disp):
        if (host != disp.split()[0]):
            dispositivos.append(disp)
        else:
            name = disp.split()[4]
            os.remove('./baseD/'+name+".rrd")
            os.remove('./baseD/'+name+".xml")
        disp = file_dispR.readline()
    file_dispR.close()

    file_dispW = open(file, 'w')
    for disp in dispositivos:
        file_dispW.write(disp)
    file_dispW.close()
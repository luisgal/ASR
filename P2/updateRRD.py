import os.path
import rrdtool
from getSNMP import consultaSNMP

def updateDisp(disp):
    if(disp[4]=='ivan'):
        ifInUcastPkts = int(consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.2.2.1.11.11')) #Wirless
    else:
        ifInUcastPkts = int(consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.2.2.1.11.2')) #Wireless
    ipInReceives = int(consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.4.3.0'))
    icmpOutEchos = int(consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.5.21.0')) #crear mensajes
    tcpInSegs = int(consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.6.10.0'))
    udpOutDatagrams = int(consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.7.4.0'))

    valor = "N:"+str(ifInUcastPkts)+':'+str(ipInReceives)+':'+str(icmpOutEchos)+':'+str(tcpInSegs)+':'+str(udpOutDatagrams)
    print(valor)

    if(os.path.exists('./baseD/'+disp[4]+".rrd")):
        rrdtool.update('./baseD/'+disp[4]+".rrd", valor)
        rrdtool.dump('./baseD/'+disp[4]+".rrd", './baseD/'+disp[4]+".xml")

while 1:
    file_dispR = open('dispositivos.txt', 'r')
    disp = file_dispR.readline()
    while (disp):
        updateDisp(disp.split())
        disp = file_dispR.readline()
    file_dispR.close()
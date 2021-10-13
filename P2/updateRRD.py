import os.path
import rrdtool
from P2.utilidades.getSNMP import consultaSNMP
from P2.utilidades.reporte import crearReport
import time

from P2.utilidades.sendEmail import sendWarningEmail


def updateDisp(disp, post):

    cpuU = consultaSNMP(disp[2], disp[0], '1.3.6.1.4.1.2021.11.9.0')
    cpuS = consultaSNMP(disp[2], disp[0], '1.3.6.1.4.1.2021.11.10.0')
    percentageCPU = post[0]
    if(cpuU != -1) and (cpuS != -1):
        percentageCPU = int(cpuU) + int(cpuS)
        post[0] = percentageCPU


    ramF = consultaSNMP(disp[2], disp[0], '1.3.6.1.4.1.2021.4.6.0')
    ramT = consultaSNMP(disp[2], disp[0], '1.3.6.1.4.1.2021.4.5.0')
    percentageRAM = post[1]
    if (ramF != -1) and (ramT != -1):
        percentageRAM = 100 - float(ramF)*100/float(ramT)
        post[1] = percentageRAM

    disk = consultaSNMP(disp[2], disp[0], '1.3.6.1.4.1.2021.9.1.9.1')
    percentageDisk = post[2]
    if disk != -1:
        percentageDisk = int(disk)
        post[2] = percentageDisk

    valor = "N:"+str(percentageCPU)+':'+str(percentageRAM)+':'+str(percentageDisk)
    print(valor)

    if(os.path.exists('./baseD/'+disp[4]+".rrd")):
        rrdtool.update('./baseD/'+disp[4]+".rrd", valor)
        rrdtool.dump('./baseD/'+disp[4]+".rrd", './baseD/'+disp[4]+".xml")

    return post



statusVar = {
    0: "Correcto",
    1: "Alerta",
    2: "Moderado",
    3: "Peligro"
}

intervalo = 150
tiempo = time.time() + intervalo
tiempo_ = tiempo
post = [1,1,1]

state = 0

while 1:
    file = 'dispositivos.txt'
    file_dispR = open(file, 'r')

    disp = file_dispR.readline()

    x = 1
    while (disp):
        post = updateDisp(disp.split(), post)

        if(time.time() >= tiempo):
            stat = crearReport(file, numFile=x, postName="_status", mostrar=False)
            tiempo_ = time.time() + intervalo
            if (stat != state) and (stat != 0):
                sendWarningEmail(subject="Status {0}-{1} - Dispositivo {2}".format(stat, statusVar[stat], disp.split()[4]),
                                 body="Se agrega el reporte del dispositivo que ha sufrido un cambio de status",
                                 filereport="./report/ReporteDisp" + disp.split()[4] + "_status.pdf")
                print("Correo enviado, cambio de status {0} a {1}".format(state,stat))
                state = stat

        disp = file_dispR.readline()
        x += 1

    tiempo = tiempo_

    file_dispR.close()
from P2.utilidades.graphRRD import graph
from reportlab.pdfgen import canvas
from P2.utilidades.getSNMP import consultaSNMP
from datetime import timedelta

def mostrarDispositivos(file, mostrar):
    file_dispR = open(file, 'r')
    dispositivos = []
    disp = file_dispR.readline()
    x = 0
    while (disp):
        x+=1
        if(mostrar):
            print("Dispositivo",x)
            print("\t",disp)
        dispositivos.append(disp)
        disp = file_dispR.readline()
    file_dispR.close()
    return dispositivos

def crearReport(file, umbral=[[77,65,40],[85,75,50],[90,75,30]], numFile=None, postName="", mostrar=True):
    dispositivos = mostrarDispositivos(file, mostrar)
    if(numFile==None):
        print("Elige el dispositivo que deseas consultar: ", end='')
        opc = input()
        disp = dispositivos[int(opc)-1].split()
    else:
        disp = dispositivos[numFile - 1].split()

    status = []

    status.append(graph('Porcentaje de CPU utiliazdo', "percentageCPU", disp[4], 'Porcentaje', umbral[0]))
    status.append(graph('Porcentaje de RAM utiliazdo', "percentageRAM", disp[4], 'Porcentaje', umbral[1]))
    status.append(graph('Porcentaje de Disk utiliazdo', "percentageDisk", disp[4], 'Porcentaje', umbral[2]))

    stat = max(status)

    #generar PDF
    c = canvas.Canvas("./report/ReporteDisp"+disp[4]+postName+".pdf")
    c.setFont("Helvetica",20) #Titulos
    c.drawString(25,800,"Resporte de Dispositivo")

    c.setFont("Helvetica",12) #Texto
    name = consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.1.5.0')
    version = consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.1.1.0')
    ubi = consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.1.6.0')
    tiempo = consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.1.3.0')
    dateT = consultaSNMP(disp[2], disp[0], '1.3.6.1.2.1.25.1.2.0')
    comunidad = disp[2]
    ip = disp [0]

    tiempo = int(tiempo)/100
    tiempo = timedelta(seconds=int(tiempo))

    dateT_ = "{0:04}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}:{6:02} UTC{7}{8:02}:{9:02}".format(
        int(dateT[2:6],16),         #Year
        int(dateT[6:8],16),         #Month
        int(dateT[8:10],16),        #Day
        int(dateT[10:12],16),       #Hour
        int(dateT[12:14],16),       #Minutes
        int(dateT[14:16],16),       #Seconds
        int(dateT[16:18],16),       #Deci-seconds
        chr(int(dateT[18:20],16)),  #Direction from UTC (ASCII format)
        int(dateT[20:22],16),       #Hoours from UTC
        int(dateT[22:24],16))       #Minutes from UTC

    c.drawString(25, 780, "Nombre del dispositivo: "+ str(name))
    c.drawString(25, 765, "Version: " + str(version))
    c.drawString(25, 750, "Ubicacion: " + str(ubi))
    c.drawString(25, 735, "Tiempo en actividad: " + str(tiempo))
    c.drawString(25, 720, "Hora del dispositivo: " + str(dateT_))
    c.drawString(25, 705, "Comunidad: " + str(comunidad))
    c.drawString(25, 690, "Host/IP: " + str(ip))

    c.drawImage("./graph/percentageCPU" + disp[4] + ".png", 25, 540, 265, 125)
    c.drawImage("./graph/percentageRAM" + disp[4] + ".png", 300, 540, 265, 125)
    c.drawImage("./graph/percentageDisk" + disp[4] + ".png", 25, 350, 265, 125)

    c.save()

    return stat

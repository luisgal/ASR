import sys
import rrdtool
import time
from P2.utilidades.sendEmail import sendWarningEmail

tiempo_actual = int(time.time())

def graph(title,name,dispName,describe, umbral=[75,50,25]):
    # Grafica desde el tiempo actual menos diez minutos
    ultima_lectura = int(rrdtool.last('./baseD/' + dispName + ".rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 3600

    ret = rrdtool.graph("./graph/"+name+dispName+".png",
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_final),
                        "--vertical-label="+name,
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "--title="+title,

                        "DEF:carga="+'./baseD/'+dispName+".rrd:"+name+":AVERAGE",

                        "VDEF:cargaMAX=carga,MAXIMUM",
                        "VDEF:cargaMIN=carga,MINIMUM",
                        "VDEF:cargaSTDEV=carga,STDEV",
                        "VDEF:cargaLAST=carga,LAST",

                        "HRULE:" + str(umbral[2]) + "#f3ff87:Alerta",
                        "HRULE:" + str(umbral[1]) + "#FF9F00:Moderado",
                        "HRULE:" + str(umbral[0]) + "#FF0000:Peligro",

                        "AREA:carga#00FF00:" + name,

                        "CDEF:umbral3=carga," + str(umbral[2]) + ",LT,0,carga,IF",
                        "AREA:umbral3#f3ff87:" + name + " mayor que " + str(umbral[2]),

                        "CDEF:umbral2=carga," + str(umbral[1]) + ",LT,0,carga,IF",
                        "AREA:umbral2#FF9F00:" + name + " mayor que " + str(umbral[1]),

                        "CDEF:umbral1=carga," + str(umbral[0]) + ",LT,0,carga,IF",
                        "AREA:umbral1#FF0000:" + name + " mayor que " + str(umbral[0]),

                        "PRINT:cargaLAST:%6.2lf",
                        "GPRINT:cargaMIN:%6.2lf %SMIN",
                        "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                        "GPRINT:cargaLAST:%6.2lf %SLAST")

    ultimo_valor = float(ret[2][0])
    status = 0

    if ultimo_valor > umbral[0]:
        print("Peligro")
        status = 3
    elif ultimo_valor > umbral[1]:
        status = 2
        print("Moderado")
    elif ultimo_valor > umbral[2]:
        status = 1
        print("Alerta")
    else:
        print("Correcto")

    return status

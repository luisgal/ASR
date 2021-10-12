import sys
import rrdtool
import time
tiempo_actual = int(time.time())

#Grafica desde el tiempo actual menos diez minutos
tiempo_inicial = tiempo_actual - 600

def graph(title,name,dispName,describe):
    ret = rrdtool.graph( "./graph/"+name+dispName+".png",
                         "--start",str(tiempo_inicial),
                         "--end","N",
                         "--title="+title,
                         "DEF:"+name+"="+'./baseD/'+dispName+".rrd:"+name+":AVERAGE",
                         "LINE3:"+name+"#0000FF:"+describe)
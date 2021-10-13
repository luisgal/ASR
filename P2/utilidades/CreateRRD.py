import rrdtool

def create(name):
    ret = rrdtool.create('./baseD/'+name+".rrd",
                         "--start",'N',
                         "--step",'5m',
                         "DS:percentageCPU:GAUGE:300:U:U",
                         "DS:percentageRAM:GAUGE:300:U:U",
                         "DS:percentageDisk:GAUGE:300:U:U",
                         "RRA:AVERAGE:0.5:1:1d",
                         )
    rrdtool.dump('./baseD/'+name+'.rrd','./baseD/'+name+'.xml')
    if ret:
        print (rrdtool.error())
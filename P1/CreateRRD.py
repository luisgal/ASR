import rrdtool

def create(name):
    ret = rrdtool.create('./baseD/'+name+".rrd",
                         "--start",'N',
                         "--step",'5m',
                         "DS:ifInUcastPkts:COUNTER:300:U:U",
                         "DS:ipInReceives:COUNTER:300:U:U",
                         "DS:icmpOutEchos:COUNTER:300:U:U",
                         "DS:tcpInSegs:COUNTER:300:U:U",
                         "DS:udpOutDatagrams:COUNTER:300:U:U",
                         "RRA:AVERAGE:0.5:1:1d",
                         "RRA:AVERAGE:0.5:1:1d",
                         "RRA:AVERAGE:0.5:1:1d",
                         "RRA:AVERAGE:0.5:1:1d",
                         "RRA:AVERAGE:0.5:1:1d"
                         )
    rrdtool.dump('./baseD/'+name+'.rrd','./baseD/'+name+'.xml')
    if ret:
        print (rrdtool.error())
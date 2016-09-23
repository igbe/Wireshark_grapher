import matplotlib
import pandas as pd
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np


ip_port_for_sort='192.168.0.199.20000'
what_to_plot='sent'
sent=[]
rcv=[]
data1=[]

rang=[]


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


#dos_sa_slave
#file=open('masterthirdcaptureblackhole.txt','r')
file=open('slavefourthcaptureDoS1.txt','r')
for i in file:
    line=i.strip().split(' ')
    #print line
    if line[3]==ip_port_for_sort:
        sent.append(line)
    else:
        rcv.append(line)
#print "sent=", sent
#print "rcv=", rcv
#a.split('.')[0]
if what_to_plot=="sent":
    start_time=sent[0][0]+' '+(sent[0][1]).split('.')[0]
    end_time=sent[len(sent)-1][0]+' '+ (sent[len(sent)-1][1]).split('.')[0]
    start_time=datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time=datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
else:
    start_time=rcv[0][0]+' '+(rcv[0][1]).split('.')[0]
    end_time=rcv[len(rcv)-1][0]+' '+ (rcv[len(rcv)-1][1]).split('.')[0]
    start_time=datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time=datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')



#print "start time=",start_time
#print "end time=",end_time
if end_time==start_time:
    time_range=start_time
    rang.append(time_range)
else:
    time_range=perdelta(start_time,end_time,timedelta(seconds=1))
    for result in time_range:
        #print result
        rang.append(result)
        #print rang
        #print "current size of rang", len(rang)

dictionary = dict(zip(rang, [0]*len(rang)))
s=0

if what_to_plot=="sent":
    for i in rang:
        for j in range(s,len(sent)):
            if  datetime.strptime((sent[j][0]+' '+(sent[j][1]).split('.')[0]), '%Y-%m-%d %H:%M:%S') <=i:
                dictionary[i]=dictionary[i]+1

            else:
                s=j
                break
else:
    for i in rang:
        for j in range(s,len(rcv)):
            if  datetime.strptime((rcv[j][0]+' '+(rcv[j][1]).split('.')[0]), '%Y-%m-%d %H:%M:%S') <=i:
                dictionary[i]=dictionary[i]+1

            else:
                s=j
                break


print dictionary

sortedList = sorted([(k, v) for k, v in dictionary.iteritems()])

print "new_dictionary=", sortedList
#print sortedList[0][1]
new_list=[]
for i in range(0,len(sortedList)):
    new_list.append(sortedList[i][1])


fig, ax1 = plt.subplots(1)
#print "rang=",rang
dates = matplotlib.dates.date2num(rang)
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
values=new_list
lowest_value=min(values)
ax1.set_ylabel('Packets per Second')


#print "dictionary.values()=",dictionary.values()
#print "dates=",dates
if end_time==start_time:
    ax1.plot_date(dates, new_list,'o')
else:
    ax1.plot_date(dates, new_list,'-')

ax1.fill_between(dates, new_list, lowest_value, facecolor='green', alpha=0.5)
ax1.grid(True)
plt.gcf().autofmt_xdate()
plt.show()
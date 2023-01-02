import sqlite3
import os.path
from os.path import isdir
from os import mkdir
from subprocess import check_output,CalledProcessError
import numpy as np
import matplotlib as mpl

mpl.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
try:
    plt.style.use('ggplot')
except:
    print "Matplotlib version " + mpl.__version__ + " does not support style argument"
import sys
import math

clean = 1
#if "-clean" in sys.argv:
#    clean = 1

print "Generating graphs using Matplotlib version " + mpl.__version__ + "and Pandas version " + pd.__version__
if clean: 
    font = {'weight' : 'normal',
            'size'   : 20}

    mpl.rc('font', **font)
    
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

DB_FILENAME = "results.db"

if not os.path.isfile(DB_FILENAME):
    print "Database file '" + DB_FILENAME + "' does not exist!"
    print "Run python create_db.py first."
    exit()

class StdevFunc:
    def __init__(self):
        self.M = 0.0
        self.S = 0.0
        self.k = 1

    def step(self, value):
        if value is None:
            return
        tM = self.M
        self.M += (value - tM) / self.k
        self.S += (value - tM) * (value - self.M)
        self.k += 1

    def finalize(self):
        if self.k < 3:
            return None
        return math.sqrt(self.S / (self.k-2))

metric = "(throughput/1000000.0)"
metric_name = "throughput"
metric1 =  "(update_throughput/1000000.0)"
metric1_name = "updates"
metric2 = "(find_throughput/1000000.0)"
metric2_name = "finds"
metric3 = "(total_rq/1000000.0)"
metric3_name = "rqs_throughput"
metric4 = "(throughput/1000000.0)"
metric4_name = "throughput"
  

datastructures= ["skiplist"]

def is_valid_key_range(ds,key_range):
    if key_range == "1000000" and ds== "list": return False
    if key_range == "100000" and ds== "list": return False
    if key_range == "10000" and ds != "list": return False
    if key_range == "1000" and ds != "list": return False
    return True

#check if HTM is enabled
try: 
    check_output('g++ ../common/test_htm_support.cpp -o ../common/test_htm_support > /dev/null; ../common/test_htm_support',shell=True)
    htm_enabled = True
except CalledProcessError:
    htm_enabled = False
    

if htm_enabled: 
    dsToAlgs = { "abtree" :         ["rwlock", "htm_rwlock", "lockfree"],
                 "bst" :            ["rwlock", "htm_rwlock", "lockfree"],
                 "lflist" :         ["rwlock", "htm_rwlock", "lockfree", "snapcollector"],
                 "lazylist" :       ["rwlock", "htm_rwlock", "lockfree", "rlu"],
                 "citrus" :         ["rwlock", "htm_rwlock", "lockfree", "rlu"],
                 "skiplistlock" :   ["rwlock", "htm_rwlock", "lockfree", "snapcollector"]
                }
    allalgs =[ "rwlock", "htm_rwlock", "lockfree", "snapcollector", "rlu", "unsafe"]
    
else:
    dsToAlgs = { "tree" :         ["Bundles", "EBR-RQ", "vCAS", "EEMARQ", "Unsafe"],
                 "skiplist" :            ["Bundles", "EBR-RQ", "vCAS", "EEMARQ", "Unsafe"],
                 "list" :         ["Bundles", "EBR-RQ", "vCAS", "EEMARQ", "Unsafe"]
                }
    allalgs =[ "lbundle", "lockfree", "vcas", "mvccvbr", "unsafe", "vbrunsafe"]
            
dsToName = { "tree" :         "Tree",
             "skiplist" :     "SkipList",
             "list" :         "List"
            }

dsToColor = {"tree" :       ['tab:green','tab:purple','tab:cyan','tab:pink','orange'],
             "skiplist" :   ['tab:green','tab:purple','tab:cyan','tab:pink','orange'],
             "list" :       ['tab:green','tab:purple','tab:cyan','tab:pink','orange']
            }
           
dsToMarker = {"tree" :        [ "x", '^', 'v', 'o', 's', '*', '+' ],
             "skiplist" :     [ "x", '^', 'v', 'o', 's', '*', '+' ],
             "list" :         [ "x", '^', 'v', 'o', 's', '*', '+' ]
            }

            
line_width = 5
conn = sqlite3.connect(DB_FILENAME)
#cursor = conn.cursor()

conn.create_aggregate("STDEV", 1, StdevFunc)

if not isdir("graphs"):
    mkdir("graphs")
outdir = "graphs/"



count = 0

############################################################################################################
algorithms = ['Bundles','EBR-RQ','vCAS','EEMARQ','Unsafe']
#labels = ['50', '100', '1K', '50K', '100K']
labels = ['1', '32', '64', '96', '128']
xlabel = "Number of threads" 
ylabel = "Throughput (Mop/s)"


def plot_png(df, labels, legend, xlabel, ylabel):
    colors = ['tab:green','tab:purple','tab:cyan','tab:pink','orange']
    markers = [ "x", '^', 'v', 'o', 's', '*', '+' ]
    df['Fake_X'] = range(1,df.shape[0]+1)
    fig = plt.figure()
    ax = plt.axes()
    x = df['Fake_X']
    

    for i in algorithms:
        ax.plot(x, df[i])

    for i, line in enumerate(ax.get_lines()):
                marker = markers[i]
                line.set_marker(marker) 
                line.set_color(colors[i])
                line.set_linestyle('-')
                line.set_markersize(8)
                line.set_linewidth(2)
    if legend:
        ax.legend(ax.get_lines(), algorithms, loc='best', fontsize=10)
    #else:
        #ax.plot(kind='line', legend=False)
    ymin,ymax = ax.get_ylim()
    ax.set_ylim(0-0.05*ymax,ymax+0.1*ymax)
    xmin,xmax = ax.get_xlim()
    ax.set_xlim(xmin-0.05*xmax,xmax+0.05*xmax)
    plt.xticks(x, labels, rotation=0)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(c='grey')
    if legend:
       plt.savefig(outdir+filename+".png", bbox_extra_artists=(ax.get_legend(),), bbox_inches='tight')
    else:
       plt.savefig(outdir+filename+".png")
    plt.close()
    

############################################################################################################

    
def plot_series_line(series,where,filename,user_title,xlabel,ylabel):
    query = ("SELECT " + series + " AS series, alg AS Algorithm, AVG("+metric+") AS y"
             " FROM results" 
             +where+
             " GROUP BY series, Algorithm" +
             " ORDER BY series, Algorithm")
    title = dsToName[ds]  
    df = pd.read_sql(query, conn)
    df = df.pivot(index='series', columns='Algorithm', values='y')
    newalgs = dsToAlgs[ds][:]
    #newalgs.append("unsafe")
    df = df.reindex(columns=newalgs)
    if True:
      df.to_csv(outdir+filename+".csv")
      plot_png(df, labels, legend=False, xlabel=xlabel, ylabel=ylabel)
    else:
      plt.figure()
      if not clean:
          title += "\n"+user_title
          ax = df.plot(kind='line', legend=False)#, title=title)
          plt.xlabel(xlabel)
          plt.ylabel(ylabel) 
          ax.legend(ax.get_lines(), df.columns, loc='best')        
      else:
          ax = df.plot(kind='line', legend=False)#, title=title)
          plt.xlabel(xlabel) 
          plt.ylabel(ylabel)
      for i, line in enumerate(ax.get_lines()):
              marker = dsToMarker[ds][i]
              line.set_marker(marker) 
              line.set_color(dsToColor[ds][i])
              line.set_linestyle('-')
              line.set_markersize(8)
              line.set_linewidth(2)
                
                
      plt.xticks(df.index.values)
      #labels = ['0.5K', '1K', '10K','20K']
      #plt.xticks(df.index.values, labels, rotation=0)
      ymin,ymax = ax.get_ylim()
      ax.set_ylim(0-0.05*ymax,ymax+0.1*ymax)
      xmin,xmax = ax.get_xlim()
      ax.set_xlim(xmin-0.05*xmax,xmax+0.05*xmax)
      plt.xticks(rotation=0) 
      ax.grid(color='grey', linestyle='-')
      if not clean: 
          plt.legend(fontsize=10)
          #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),handleheight=4, handlelength=4)
          plt.savefig(outdir+filename+".png", bbox_extra_artists=(ax.get_legend(),), bbox_inches='tight')
      else:
          plt.savefig(outdir+filename+".png",bbox_inches='tight')
      plt.close('all')

    

maxthreads = check_output('cat ../config.mk | grep "maxthreads=" | cut -d"=" -f2', shell=True)
maxthreads = maxthreads.strip()
maxrqthreads = check_output('cat ../config.mk | grep "maxrqthreads=" | cut -d"=" -f2', shell=True)
maxrqthreads = maxrqthreads.strip()


if True:
  print "generating graphs for EXPERIMENT 1 IMPACT OF INCREASING UPDATE THREAD COUNT ... "
  
  updates = ["50"]
  rq="0"
  rqsize="1000"
  nrq="0"
  key_ranges = ["1000000"]
  for ds in datastructures:
      print "generating graphs for " + ds + " ..."
      for k in key_ranges:
          for u in updates:
              if not is_valid_key_range(ds,k): continue
              where = (" WHERE ds='"+ds+"'"
                      " AND rq_th="+nrq+
                      " AND ins="+u+
                      " AND del="+u+
                      " AND rq="+rq+ 
                      " AND max_key="+k+
                      " AND rq_size="+rqsize)
              #if clean:
              #   where+= " AND work_th IN (1,8,16,24,32,40,47)"
              xlabel = "Number of threads" 
              ylabel = "Throughput (Mop/s)"
              state = ["k"+k,"u"+u,"rq"+rq,"rqsize"+rqsize]       
              title_end = " ".join(state)
              filename_end = "-".join(state)
  
              title = metric_name+"\n"+title_end
              filename = "-".join((ds,metric_name))+"-"+filename_end
              plot_series_line("work_th",where,filename,title,xlabel,ylabel)
              count+=1
else:
  print "generating graphs for EXPERIMENT 2 IMPACT OF INCREASING RANGE QUERY SIZE ... "
  
  updates = ["25"]
  rq="0"
  #rqsize="100"
  nrq="64"
  nwork="64"
  key_ranges = ["1000000"]
  for ds in datastructures:
      print "generating graphs for " + ds + " ..."
      for k in key_ranges:
          for u in updates:
              if not is_valid_key_range(ds,k): continue
              where = (" WHERE ds='"+ds+"'"
                      " AND rq_th="+nrq+
                      " AND ins="+u+
                      " AND del="+u+
                      " AND rq="+rq+ 
                      " AND max_key="+k+
                      " AND work_th="+nwork)
              #if clean:
              #   where+= " AND work_th IN (1,8,16,24,32,40,47)"
              xlabel = "Range Query Size" 
              ylabel = "RQs (Mop/s)"
              state = ["k"+k,"u"+u,"rq"+rq]       
              title_end = " ".join(state)
              filename_end = "-".join(state)
  
              title = metric_name+"\n"+title_end
              filename = "-".join((ds,metric_name))+"-"+filename_end
              plot_series_line("rq_size",where,filename,title,xlabel,ylabel)
              count+=1


print "Generated " + str(count) + " graphs"
conn.close()

#! /bin/bash

if [[ $# -ne 3 ]]; then
  echo "Incorrect number of arguments (expected=3, actual=$#)."
  echo "Usage: $0 <datadir> <num_trials> <listname>."
  exit
fi

datadir=$1
ntrials=$2
listname=$3
# Each algorithm should be isolated in its own directory.
algos=$(ls ${datadir})
# echo $algos

cd ${datadir}
outfile=${listname}.csv

currfile=""
rqthrupt=0
uthrupt=0
totthrupt=0
ulat=0
clat=0
rqlat=0
rqthrupt=0
uthrupt=0
totthrupt=0
avgrqlen=0
avgannounce=0
avgbag=0
reachable=0
avgbundle=0
expectedcount=0
trialcount=0
nobundlestats=0
echo "list,max_key,u_rate,rq_rate,wrk_threads,rq_threads,rq_size,u_latency,c_latency,rq_latency,tot_thruput,u_thruput,c_thruput,rq_thruput,rq_len,avg_in_announce,avg_in_bags,reachable_nodes,avg_bundle_size" >${outfile}
for algo in ${algos}; do
  files=$(ls ${algo} | grep ${listname})
  # echo $files
  for f in ${files}; do
    filename=${algo}/${f}
    # echo $filename
    # Only parse lines for given listname.
    if [[ "${listname}" != "" ]] && [[ "$(echo ${filename} | grep ${listname})" == "" ]]; then
      exit
    elif [[ "$(echo ${filename} | sed 's/.*[.]csv/.csv/')" == ".csv" ]]; then
      continue
    fi

    # Assumes trials are consecutive.
    rootname=$(echo ${filename} | sed -E 's/step[0-9]+[.]//' | sed -e 's/[.]trial.*//')
    if [[ ! "${rootname}" == "${currfile}" ]]; then
      trialcount=0
      currfile=${rootname}
      config=$(cat ${filename} | grep -B 10000 'BEGIN RUNNING')

      # Get name of list.
      list=$(echo ${filename} | sed -e "s/.*[.]${listname}[.]/${listname}-/" | sed -e 's/[.].*//')
      rqstrategy=$(echo "${list}" | sed -e "s/.*-//")

      # Get maximum key.
      maxkey=$(echo "${config}" | grep 'MAXKEY=' | sed -e 's/.*=//')

      nwrkthrds=$(echo "${config}" | grep 'WORK_THREADS=' | sed -e 's/.*=//')
      irate=$(echo "${config}" | grep 'INS=' | sed -e 's/.*=//')
      rrate=$(echo "${config}" | grep 'DEL=' | sed -e 's/.*=//')
      urate=$(echo "${irate} + ${rrate}" | bc)
      rqsize=$(echo "${config}" | grep 'RQSIZE=' | sed -e 's/.*=//')
      rqrate=$(echo "${config}" | grep 'RQ=' | sed -e 's/.*=//')
      rqthrds=$(echo "${config}" | grep 'RQ_THREADS=' | sed -e 's/.*=//')
    fi

    filecontents=$(cat ${filename} | grep -A 10000 'END RUNNING')
    if [[ "$(echo "${filecontents}" | grep 'garbage')" == "" ]]; then
      expectedcount=$((${expectedcount} + 1))
      continue
    fi

    # Latency statistics.
    ulat=$(($(echo "${filecontents}" | grep 'average latency_updates' | sed -e 's/.*=//') + ${ulat}))
    clat=$(($(echo "${filecontents}" | grep 'average latency_searches' | sed -e 's/.*=//') + ${clat}))
    rqlat=$(($(echo "${filecontents}" | grep 'average latency_rqs' | sed -e 's/.*=//') + ${rqlat}))

    # Throughput statistics.
    rqthrupt=$(($(echo "${filecontents}" | grep 'rq throughput' | sed -e 's/.*: //') + ${rqthrupt}))
    uthrupt=$(($(echo "${filecontents}" | grep 'update throughput' | sed -e 's/.*: //') + ${uthrupt}))
    totthrupt=$(($(echo "${filecontents}" | grep 'total throughput' | sed -e 's/.*: //') + ${totthrupt}))

    # Average range query length.
    avgrqlen=$(($(echo "${filecontents}" | grep 'average length_rqs' | sed -e 's/.*=//') + ${avgrqlen}))

    # EBR specific statistics.
    if [[ "${nobundlestats}" == 0 ]] && ([[ "${rqstrategy}" == "lbundle" ]] || [[ "${rqstrategy}" == "cbundle" ]]); then
      # Bundle specific statistics.
      reachable=$(($(echo "${filecontents}" | grep 'total reachable nodes' | sed -e 's/.*: //') + ${reachable}))
      if [[ ${reachable} != 0 ]]; then
        avgbundle=$(echo "$(echo "${filecontents}" | grep 'average bundle size' | sed -e 's/.*: //') + ${avgbundle}" | bc)
      fi
    else
      if [[ "${avgbundle}" != "0" ]]; then
        exit 1
      fi
      avgannounce=$(($(echo "${filecontents}" | grep 'average visited_in_announcements' | sed -e 's/.*=//') + ${avgannounce}))
      avgbag=$(($(echo "${filecontents}" | grep 'average visited_in_bags' | sed -e 's/.*=//') + ${avgbag}))
    fi

    trialcount=$((${trialcount} + 1))

    # Output previous averages.
    if [[ ${trialcount} == ${ntrials} ]]; then
      printf "%s,%d,%.2f,%.2f,%d,%d,%d" ${list} ${maxkey} ${urate} ${rqrate} ${nwrkthrds} ${rqthrds} ${rqsize} >>${outfile}
      printf ",%d" $((${ulat} / ${ntrials})) >>${outfile}
      printf ",%d" $((${clat} / ${ntrials})) >>${outfile}
      printf ",%d" $((${rqlat} / ${ntrials})) >>${outfile}
      printf ",%d" $((${totthrupt} / ${ntrials})) >>${outfile}
      printf ",%d" $((${uthrupt} / ${ntrials})) >>${outfile}
      printf ",%d" $((${totthrupt} - (${uthrupt} + ${rqthrupt}))) >>${outfile}
      printf ",%d" $((${rqthrupt} / ${ntrials})) >>${outfile}
      printf ",%d" $((${avgrqlen} / ${ntrials})) >>${outfile}
      printf ",%d" $((${avgannounce} / ${ntrials})) >>${outfile}
      printf ",%d" $((${avgbag} / ${ntrials})) >>${outfile}
      printf ",%d" $((${reachable} / ${ntrials})) >>${outfile}
      printf ",%.2f\n" $(echo "scale=4;$(echo ${avgbundle}) / ${ntrials}.0" | bc) >>${outfile}
      ulat=0
      clat=0
      rqlat=0
      rqthrupt=0
      uthrupt=0
      totthrupt=0
      avgrqlen=0
      avgannounce=0
      avgbag=0
      reachable=0
      avgbundle=0
    fi
  done
done

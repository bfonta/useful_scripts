eos_folder="/eos/user/b/bfontana/hhbbtautau/SKIMS_UL18/"
data_folder="/data_CMS/cms/alves/HHresonant_SKIMS/SKIMS_UL18_7Feb2023"

# for adir in ${data_folder}/*/; do
#     eos_type=`basename ${adir}`
#     n1=`find ${adir} -type f -name '*.root' -printf x | wc -c`
#     n2=`find ${eos_folder}${eos_type} -type f -name '*.root' -printf x | wc -c`
#     if [[ $n1 -ne $n2 ]]; then 
# 	echo  $n1 $n2 ${adir} ${eos_folder}${eos_type}
#     fi
# done

for adir in ${data_folder}/*/; do
    eos_type=`basename ${adir}`
    for afile in ${adir}/*root; do
	n1=$(python3 ndir.py -i ${afile} -t HTauTauTree)
	n2=$(python3 ndir.py -i ${eos_folder}${eos_type}/$(basename $afile) -t HTauTauTree)
	if [[ $n1 -ne $n2 ]]; then 
	    echo $n1 $n2 ${afile} ${eos_folder}${eos_type}/$(basename $afile)
	fi
    done
done


package main

import (
	"fmt"
	"os"
	"flag"
	"errors"
	"strings"
	"sync"
	fp "path/filepath"
	ex "os/exec"
	"regexp"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func create_dir(d string) {
	if _, err := os.Stat(d); errors.Is(err, os.ErrNotExist) {
		os.Mkdir(d, 0700) //os.Mkdir(d, os.ModeDir)
	}
}

func main() {
	masses  := [8]float{250, 350, 450, 550, 650, 750, 850, 950}
	sthetas := [3]float{0., 0.5, 1.0}
	lambdas112 := [2]float{-300., 300}
	kappas112 := [2]float{-5, 2}

	lambda112_sm := 125**2 / (2*246.), 6 //tri-linear Higgs coupling

	sed -i -e 's/automatic_html_opening = True/automatic_html_opening = False/g' Cards/me5_configuration.txt

	#change the number of events to 3
	sed -i -E -e 's/[0-9]+ = nevents/20000 = nevents/g' Cards/run_card.dat

	create_dir(Radion_bbtata_LR3tevLHC8)

	for i, line := range template_lines {
		// sed -i -E -e "s/ 9000001 [0-9]+?\.?[0-9]+?.* \# ImFmeio/ 9000001 ${ImFmeio[$i]} \# ImFmeio/g" Cards/param_card.dat
        // sed -i -E -e "s/ 9000003 [0-9]+?\.?[0-9]+?.* \# ReFmeio/ 9000003 ${ReFmeio[$i]} \# ReFmeio/g" Cards/param_card.dat
        // sed -i -E -e "s/ 35 [0-9]+?\.?[0-9]+?.* \# MH02/ 35 ${MR[$i]} \# MH02/g" Cards/param_card.dat

		exe := "./bin/generate_events"
		fmt.Println("Command: " + exe + " " + in + " " + out)
		cmd := ex.Command(exe, in, out)
		
	// 	./bin/generate_events 0 MR_${MR[$i]}_on run1

	// 	gunzip Events/MR_${MR[$i]}_on/unweighted_events.lhe.gz 
    //     mv Events/MR_${MR[$i]}_on/unweighted_events.lhe Radion_bbtata_LR3tevLHC8/MR_${MR[$i]}_on.lhe

    // sed -i -e 's/ 8   0/ 8   100/g' Radion_bbtata_LR3tevLHC8/MR_${MR[$i]}_on.lhe
    //     sed -i -e 's/ 9   0/ 9   100/g' Radion_bbtata_LR3tevLHC8/MR_${MR[$i]}_on.lhe
		
    // #take the CX
		// echo "MR" "${MR[$i]}" "$(grep -E '\#  Integrated weight \(pb\)  \:  ' Radion_bbtata_LR3tevLHC8/MR_${MR[$i]}_on.lhe)" >> Radion_bbtata_LR3tevLHC8/CX_LR3tev_LHC100.txt
	}
}

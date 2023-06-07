
package main

import (
	"fmt"
	"os"
	//"math"
	"os/exec"
	"errors"
	sc "strconv"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func check_cmd_error(cmd *exec.Cmd) {
    out, err := cmd.Output()
    if err != nil {
        fmt.Println(err.Error())
        return
    }
	fmt.Println(out)
	fmt.Println()
	fmt.Println(err)
}

func create_dir(d string) {
	if _, err := os.Stat(d); errors.Is(err, os.ErrNotExist) {
		os.Mkdir(d, 0700) //os.Mkdir(d, os.ModeDir)
	}
}

func replace_line(sed_line string) {
	cmd := exec.Command("sed", "-i", "-E", "-e", sed_line, "Cards/param_card.dat")
	check_cmd_error(cmd)
}

func calc_ctheta(stheta float64) string {
	sc.FormatFloat(stheta, 'f', -1, 64)
}

func main() {
	masses		:= []float64{250} //, 350, 450, 550, 650, 750, 850, 950}
	// sthetas		:= []float64{0.5}
	// lambdas112	:= []float64{-300.}
	// kappas112	:= []float64{-5}

	// lambda112_sm := math.Pow(125, 2) / (2*246.) //tri-linear Higgs coupling

	cmd := exec.Command("sed", "-i", "-e", "s/automatic_html_opening = True/automatic_html_opening = False/g", "Cards/me5_configuration.txt")
	check_cmd_error(cmd)
	
	// change the number of events to 3
	cmd = exec.Command("sed", "-i", "-E", "-e", "s/[0-9]+ = nevents/3 = nevents/g", "Cards/run_card.dat")
	check_cmd_error(cmd)

	create_dir("TEST_DIR")
	for _, mass := range masses {
		replace_line("s/ 99925 [0-9]+?\\.?[0-9]+?.* \\# Weta/ 99925 " +	sc.FormatFloat(mass, 'f', -1, 64) + " \\# Weta/g")

		for _, stheta := range sthetas {
			replace_line("s/ 14 [0-9]+?\\.?[0-9]+?.* \\# stheta/ 14 " + sc.FormatFloat(stheta, 'f', -1, 64) + " \\# stheta/g")
			replace_line("s/ 13 [0-9]+?\\.?[0-9]+?.* \\# ctheta/ 13 " + calc_ctheta(stheta) + " \\# ctheta/g")

			for _, lbd := range lambdas112 {

				for _, kap := range kappas112 {

		
		cmd = ex.Command("./bin/generate_events")
		check_cmd_error(cmd)
		// 	./bin/generate_events 0 MR_${MR[$i]}_on run1

		// 	gunzip Events/MR_${MR[$i]}_on/unweighted_events.lhe.gz 
		//     mv Events/MR_${MR[$i]}_on/unweighted_events.lhe Radion_bbtata_LR3tevLHC8/MR_${MR[$i]}_on.lhe

		// sed -i -e 's/ 8   0/ 8   100/g' Radion_bbtata_LR3tevLHC8/MR_${MR[$i]}_on.lhe
		//     sed -i -e 's/ 9   0/ 9   100/g' Radion_bbtata_LR3tevLHC8/MR_${MR[$i]}_on.lhe
		
		// #take the CX
		// echo "MR" "${MR[$i]}" "$(grep -E '\#  Integrated weight \(pb\)  \:  ' Radion_bbtata_LR3tevLHC8/MR_${MR[$i]}_on.lhe)" >> Radion_bbtata_LR3tevLHC8/CX_LR3tev_LHC100.txt
	}
}

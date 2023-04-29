#!/usr/bin/python

import sys
import os
import argparse
import fileinput 

def main(opt):

    dir_out = opt.out
    dir_template = opt.template
    model = opt.model
    
    # read template cards
    templateName = '{model}_hh_width_Mmass'.format(model=model)
    run_card_template       = open(dir_template + '/' + templateName + '_run_card.dat',       'r')
    customizecards_template = open(dir_template + '/' + templateName + '_customizecards.dat', 'r')
    proc_card_template      = open(dir_template + '/' + templateName + '_proc_card.dat',      'r')
    extra_card_template     = open(dir_template + '/' + templateName + '_extramodels.dat',    'r')
    run_content    = run_card_template.read()
    custom_content = customizecards_template.read()
    proc_content   = proc_card_template.read()
    extra_content  = extra_card_template.read()

    # list of mass points considered for Run 2 X->HH combination
    mass_points = ['260','270','300','350','400','450','500','550','600','650','700','800','900','1000','1100','1200','1300','1500','2000']
    
    # list of width hypotheses considered (arbitrary values between 10-30% + NWA)
    width_points = [0., 0.1, 0.15, 0.2, 0.25, 0.3]

    for mass in mass_points:
        for width in width_points:
            
            width_in_gev = '1.0e-03' if width==0 else str(width*float(mass))
            width_str = 'narrow' if width==0 else '{}pcts'.format(int(100*width))

            card_name = '{model}_hh_{width_str}_M{mass}'.format(model=model,width_str=width_str,mass=mass)
            dir_name = '{dir_out}/{card_dir}/'.format(dir_out=dir_out,card_dir=card_name)
            
            print("Generating {} cards".format(card_name))

            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            
            # run card can be copied from template with no modification
            run_card = open( dir_name + card_name + '_run_card.dat', 'w' )
            run_card.write( run_content )
            run_card.close()
        
            # model card can be copied from template with no modification
            extra_card = open( dir_name + card_name + '_extramodels.dat', 'w' )
            extra_card.write( extra_content )
            extra_card.close()
        
            # customize card needs mass & width to be updated
            customize_card = open( dir_name + card_name + '_customizecards.dat', 'w' )
            customize_card.write( custom_content )
            customize_card.close()
            for line in fileinput.input(dir_name + card_name +'_customizecards.dat', inplace=True): 
                if "Graviton" in model : 
                    pdgId_resonance = '39'
                if "Radion" in model : 
                    pdgId_resonance = '35'
                line = line.rstrip().replace('set param_card mass {pdg} MASS'.format(pdg=pdgId_resonance),
                                             'set param_card mass {pdg} {mass}'.format(pdg=pdgId_resonance,mass=mass))
                line = line.rstrip().replace('set param_card decay {pdg} WIDTH'.format(pdg=pdgId_resonance),
                                             '\nset param_card decay {pdg} {width}'.format(pdg=pdgId_resonance,
                                                                                           width=width_in_gev))
                if not line.isspace():
                    sys.stdout.write(line)
 
            # proc card needs output card name to be updated
            proc_card = open( dir_name + card_name +'_proc_card.dat', 'w' )            
            proc_card.write( proc_content )
            proc_card.close()
            for line in fileinput.input( dir_name + card_name + '_proc_card.dat', inplace=True): 
                line = line.rstrip().replace(model+'_hh_width_Mmass', card_name)+'\n' 
                if not line.isspace():
                    sys.stdout.write(line)

    run_card_template.close()
    customizecards_template.close()
    proc_card_template.close()
    extra_card_template.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Generate datacards. Example: 'python generateCards.py --model Radion --template Spin-0/cards_templates/ --out TEST/'")
    parser.add_argument('--out', help='Output directory for datacards')
    parser.add_argument('--template', help='Directory storing templates')
    parser.add_argument('--model', choices=('BulkGraviton', 'RSGraviton', 'Radion'), help='Model to process')
    FLAGS = parser.parse_args()
    main(FLAGS)

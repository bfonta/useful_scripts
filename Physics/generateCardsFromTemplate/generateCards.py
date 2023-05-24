#!/usr/bin/python

import sys
import os
import argparse
import fileinput as fp

class CardsContent:
    def __init__(self, dir_template, template_name):
        self.template_name = template_name
        self.run_card       = open(dir_template + '/' + self.template_name + '_run_card.dat',       'r')
        self.customize_card = open(dir_template + '/' + self.template_name + '_customizecards.dat', 'r')
        self.proc_card      = open(dir_template + '/' + self.template_name + '_proc_card.dat',      'r')
        self.extra_card     = open(dir_template + '/' + self.template_name + '_extramodels.dat',    'r')
        self.read()

    def read(self):
        self.run_card = self.run_card.read()
        self.customize_card = self.customize_card.read()
        self.proc_card = self.proc_card.read()
        self.extra_card = self.extra_card.read()

    def __exit__(self, exc_type, exc_value, traceback):
        self.run_card.close()
        self.customize_card.close()
        self.proc_card.close()
        self.extra_card.close()

def generate_card(pars, dir_name, card_name, model, content):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
            
    # run card can be copied from template with no modification
    with open(dir_name + card_name + '_run_card.dat', 'w') as run_card:
        run_card.write(content.run_card)
    
    # model card can be copied from template with no modification
    with open(dir_name + card_name + '_extramodels.dat', 'w') as extra_card:
        extra_card.write(content.extra_card)
    
    # customize card needs mass & width to be updated
    custcard_name = dir_name + card_name + '_customizecards.dat'
    customize_card = open(custcard_name, 'w')
    customize_card.write(content.customize_card)
    customize_card.close()

    for line in fp.input(custcard_name, inplace=True):
        if 'Graviton' in model: 
            pdgid = '39'
        elif 'Radion' in model: 
            pdgid = '35'
        elif 'Singlet' in model:
            pdgid = '99925'
            sthetaid = '14'
            kap112id = '16'
                    
        line = line.rstrip().replace('set param_card mass {} MASS'.format(pdgid),
                                     'set param_card mass {} {}'.format(pdgid, pars[0]))
        if 'Singlet' in model:
            line = line.rstrip().replace('set param_card bsm {} STHETA'.format(sthetaid),
                                         'set param_card bsm {} {}'.format(sthetaid, pars[1]))
            line = line.rstrip().replace('set param_card bsm {} KAP112'.format(kap112id),
                                         'set param_card bsm {} {}'.format(kap112id, pars[2]))
        else:
            line = line.rstrip().replace('set param_card decay {} WIDTH'.format(pdgid),
                                         'set param_card decay {} {}'.format(pdgid, pars[1]))
            
        if not line.isspace():
            sys.stdout.write(line + '\n')
 
    # proc card needs output card name to be updated
    proc_card = open(dir_name + card_name +'_proc_card.dat', 'w')
    proc_card.write(content.proc_card)
    proc_card.close()
    for line in fp.input(dir_name + card_name + '_proc_card.dat', inplace=True):
        line = line.rstrip().replace(content.template_name, card_name)
        if not line.isspace():
            sys.stdout.write(line + '\n')

def main(opt):
    dir_out = opt.out
    dir_template = opt.template
    model = opt.model
    
    # read template cards
    if 'Singlet' in model:
        template_name = '{model}_hh_width_Mmass'.format(model=model)
    else:
        template_name = '{model}_hh_STstheta_Kkap_Mmass'.format(model=model)
    cont = CardsContent(dir_template, template_name)

    # list of parameters being scanned
    # mass_points = ('250', '260', '270', '280', '300', '320', '350', '400',
    #                '450', '500', '550', '600', '650', '700', '750', '800',
    #                '850', '900', '1000', '1250', '1500', '1750', '2000', '2500', '3000')
    mass_points = ('250',)
    width_points = (0., 0.1,)
    stheta_points = (0.2, 0.5, 0.8)
    kap112_points = (1., 2., 3.) 
    
    common_pars = (model, cont)
    for mass in mass_points:
        if 'Singlet' in model:
            for stheta in stheta_points:
                st_str = str(stheta).replace('.', 'p')
                for kap in kap112_points:
                    kap_str = str(kap).replace('.', 'p')
                    card_name = '{model}_hh_ST{stheta}_K{kap}_M{mass}'.format(model=model, stheta=st_str, kap=kap_str, mass=mass)
                    dir_name = '{dir_out}/{card_dir}/'.format(dir_out=dir_out, card_dir=card_name)
                    print("Generating card {}".format(card_name))
                    generate_card((mass, stheta, kap), dir_name, card_name, *common_pars)
        else:
            for width in width_points:
                width_in_gev = '1.0e-03' if width==0 else str(width*float(mass))
                width_str = 'narrow' if width==0 else '{}pcts'.format(int(100*width))
                card_name = '{model}_hh_{width}_M{mass}'.format(model=model, width=width_str, mass=mass)
                dir_name = '{dir_out}/{card_dir}/'.format(dir_out=dir_out, card_dir=card_name)
                print("Generating card {}".format(card_name))
                generate_card((mass, width), dir_name, card_name, *common_pars)

if __name__=='__main__':
    example = 'python generateCards.py --out TestSinglet --template SingletModel/cards_templates/ --model Singlet'
    parser = argparse.ArgumentParser(description="Generate datacards. \nExample: " + example)
    parser.add_argument('--out', help='Output directory for datacards')
    parser.add_argument('--template', help='Directory storing templates')
    parser.add_argument('--model', choices=('BulkGraviton', 'RSGraviton', 'Radion', 'Singlet'),
                        help='Model to process')
    FLAGS = parser.parse_args()
    main(FLAGS)

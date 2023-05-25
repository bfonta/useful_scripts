#!/usr/bin/python

import sys
import os
import argparse
import fileinput as fp
import numpy as np
from tqdm import tqdm

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

def plot_width(widths):
    import matplotlib
    import matplotlib.pyplot as plt
    import mplhep as hep
    plt.style.use(hep.style.ROOT)
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    
    ax.plot(list(widths.keys()), list(widths.values()), color='black')
    ax.set_xscale('log')
    ax.set_xticks([100, 200, 300, 500, 1000])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    
    ax.set_xlabel('$M_{H}$ [GeV]')
    
    ax.set_yscale('log')
    ax.set_ylabel(r'$\Gamma_{H}$ [GeV]')
    
    linesoptv = dict(linestyle='--', linewidth=1.5, color='red')
    plt.axvline(x=250., **linesoptv)
    plt.axvline(x=125.09, **linesoptv)
    linesopth = dict(linestyle='--', linewidth=1.5, color='gray')
    for yv in (1E-2, 1E-1, 1E0, 1E1, 1E2, 1E3):
        plt.axhline(y=yv, **linesopth)
        
    plt.tight_layout()
    plt.savefig('HiggsLikeScalarBoson_MassVsWidth.png')
        
def calc_width(mres, stheta, lambda112, plot=False):
    """
    Calculate width of singlet scalar as given by https://arxiv.org/pdf/2010.00597.pdf
    in eqs. A.1 and A.3, where "1" refers to SM Higgs and "2" refers to the singlet scalar.
    """
    # in order: bb, tautau, mumu, cc, tt, gg, gammagamma, Zgamma, WW, ZZ
    w_sm = {20:     sum((5.244E-4, 3.949E-5, 1.465E-7, 2.936E-5, 0.,       1.895E-5, 2.861E-8, 0.000E0, 3.560E-11, 3.100E-12)),
            30:     sum((7.709E-4, 6.086E-5, 2.198E-7, 3.921E-5, 0.,       1.522E-5, 9.586E-8, 0.000E0, 6.432E-10, 1.586E-10)),
            40:     sum((9.752E-4, 8.193E-5, 2.932E-7, 4.851E-5, 0.,       1.939E-5, 2.246E-7, 0.000E0, 5.186E-9, 1.407E-9)),
            50:     sum((1.163E-3, 1.028E-4, 3.663E-7, 5.738E-5, 0.,       2.879E-5, 4.380E-7, 0.000E0, 2.720E-8, 7.734E-9)),
            60:     sum((1.342E-3, 1.237E-4, 4.397E-7, 6.601E-5, 0.,       4.305E-5, 7.642E-7, 0.000E0, 1.103E-7, 3.129E-8)),
            70:     sum((1.516E-3, 1.445E-4, 5.129E-7, 7.442E-5, 0.,       6.318E-5, 1.237E-6, 0.000E0, 3.839E-7, 1.080E-7)),
            80:     sum((1.684E-3, 1.653E-4, 5.862E-7, 8.258E-5, 0.,       9.002E-5, 1.898E-6, 0.000E0, 1.227E-6, 3.257E-7)),
            90:     sum((1.849E-3, 1.860E-4, 6.592E-7, 9.063E-5, 0.,       1.245E-4, 2.805E-6, 0.000E0, 4.509E-6, 9.188E-7)),
            100:    sum((2.011E-3, 2.068E-4, 7.325E-7, 9.852E-5, 0.,       1.674E-4, 4.035E-6, 1.226E-7, 2.67E-5, 2.775E-6)),
            110:    sum((2.170E-3, 2.275E-4, 8.058E-7, 1.063E-4, 0.,       2.198E-4, 5.699E-6, 1.114E-6, 1.327E-4, 1.234E-5)),
            120:    sum((2.328E-3, 2.483E-4, 8.791E-7, 1.140E-4, 0.,       2.827E-4, 7.977E-6, 3.881E-6, 4.826E-4, 5.536E-5)),
            125:    sum((2.406E-3, 2.587E-4, 9.159E-7, 1.178E-4, 0.,       3.185E-4, 9.428E-6, 6.266E-6, 8.489E-4, 1.066E-4)),
            125.09: sum((2.407E-3, 2.589E-4, 9.166E-7, 1.179E-4, 0.,       3.191E-4, 9.460E-6, 6.313E-6, 8.573E-4, 1.078E-4)),
            130:    sum((2.483E-3, 2.690E-4, 9.526E-7, 1.216E-4, 0.,       3.572E-4, 1.116E-5, 9.555E-6, 1.442E-3, 1.933E-4)),
            140:    sum((2.637E-3, 2.898E-4, 1.025E-6, 1.290E-4, 0.,       4.445E-4, 1.584E-5, 2.007E-5, 3.963E-3, 5.531E-4)),
            150:    sum((2.787E-3, 3.105E-4, 1.099E-6, 1.364E-4, 0.,       5.459E-4, 2.347E-5, 3.998E-5, 1.159E-2, 1.403E-3)),
            160:    sum((2.938E-3, 3.313E-4, 1.172E-6, 1.438E-4, 0.,       6.629E-4, 4.336E-5, 9.587E-5, 7.105E-2, 3.402E-3)),
            170:    sum((3.088E-3, 3.521E-4, 1.246E-6, 1.511E-4, 0.,       7.975E-4, 5.812E-5, 1.518E-4, 3.466E-1, 8.791E-3)),
            180:    sum((3.233E-3, 3.728E-4, 1.319E-6, 1.582E-4, 0.,       9.509E-4, 6.441E-5, 1.864E-4, 5.603E-1, 3.694E-2)),
            190:    sum((3.376E-3, 3.935E-4, 1.392E-6, 1.652E-4, 0.,       1.125E-3, 7.011E-5, 2.195E-4, 7.758E-1, 2.093E-1)),
            200:    sum((3.519E-3, 4.144E-4, 1.466E-6, 1.723E-4, 0.,       1.325E-3, 7.535E-5, 2.512E-4, 1.013E0, 3.521E-1)),
            210:    sum((3.659E-3, 4.349E-4, 1.539E-6, 1.790E-4, 0.,       1.549E-3, 8.011E-5, 2.810E-4, 1.280E0, 4.879E-1)),
            220:    sum((3.798E-3, 4.557E-4, 1.612E-6, 1.859E-4, 0.,       1.804E-3, 8.450E-5, 3.093E-4, 1.584E0, 6.319E-1)),
            230:    sum((3.938E-3, 4.765E-4, 1.685E-6, 1.927E-4, 0.,       2.093E-3, 8.855E-5, 3.360E-4, 1.928E0, 7.904E-1)),
            240:    sum((4.636E-3, 5.657E-4, 2.000E-6, 2.269E-4, 0.,       2.754E-3, 1.050E-4, 4.108E-4, 2.317E0, 9.673E-1)),
            250 :   sum((4.214E-3, 5.178E-4, 1.832E-6, 2.062E-4, 0.,       2.792E-3, 9.572E-5, 3.849E-4, 2.750E0, 1.166E0)),
            260 :   sum((4.351E-3, 5.384E-4, 1.905E-6, 2.129E-4, 1.946E-7, 3.215E-3, 9.890E-5, 4.072E-4, 3.232E0, 1.386E0)),
            270 :   sum((4.487E-3, 5.592E-4, 1.978E-6, 2.195E-4, 1.235E-5, 3.699E-3, 1.018E-4, 4.282E-4, 3.765E0, 1.632E0)),
            280 :   sum((4.689E-3, 5.885E-4, 2.081E-6, 2.294E-4, 7.015E-5, 4.315E-3, 1.061E-4, 4.545E-4, 4.351E0, 1.904E0)),
            290 :   sum((4.756E-3, 6.008E-4, 2.125E-6, 2.328E-4, 2.247E-4, 4.894E-3, 1.071E-4, 4.665E-4, 4.992E0, 2.202E0)),
            300 :   sum((4.890E-3, 6.215E-4, 2.198E-6, 2.393E-4, 5.767E-4, 5.644E-3, 1.094E-4, 4.840E-4, 5.690E0, 2.529E0)),
            320 :   sum((5.155E-3, 6.629E-4, 2.345E-6, 2.522E-4, 2.862E-3, 7.597E-3, 1.137E-4, 5.157E-4, 7.264E0, 3.271E0)),
            350 :   sum((5.549E-3, 7.250E-4, 2.564E-6, 2.715E-4, 2.420E-1, 1.363E-2, 1.156E-4, 5.537E-4, 1.010E1, 4.623E0)),
            400 :   sum((6.195E-3, 8.288E-4, 2.931E-6, 3.032E-4, 4.315E0,  2.573E-2, 7.226E-5, 5.545E-4, 1.623E1, 7.574E0)),
            450 :   sum((6.829E-3, 9.322E-4, 3.297E-6, 3.342E-4, 8.701E0,  3.420E-2, 3.885E-5, 5.369E-4, 2.432E1, 1.150E1)),
            500 :   sum((7.452E-3, 1.036E-3, 3.663E-6, 3.648E-4, 1.278E1,  4.052E-2, 1.802E-5, 5.151E-4, 3.460E1, 1.654E1)),
            550 :   sum((8.070E-3, 1.139E-3, 4.029E-6, 3.948E-4, 1.651E1,  4.539E-2, 7.930E-6, 4.925E-4, 4.734E1, 2.280E1)),
            600 :   sum((8.677E-3, 1.243E-3, 4.395E-6, 4.245E-4, 1.994E1,  4.921E-2, 7.031E-6, 4.707E-4, 6.274E1, 3.039E1)),
            650 :   sum((9.281E-3, 1.347E-3, 4.764E-6, 4.542E-4, 2.314E1,  5.243E-2, 1.429E-5, 4.508E-4, 8.110E1, 3.945E1)),
            700 :   sum((9.874E-3, 1.450E-3, 5.128E-6, 4.831E-4, 2.613E1,  5.497E-2, 2.905E-5, 4.325E-4, 1.026E2, 5.010E1)),
            750 :   sum((1.046E-2, 1.554E-3, 5.493E-6, 5.118E-4, 2.898E1,  5.711E-2, 5.099E-5, 4.173E-4, 1.275E2, 6.245E1)),
            800 :   sum((1.105E-2, 1.658E-3, 5.861E-6, 5.406E-4, 3.169E1,  5.896E-2, 7.996E-5, 4.051E-4, 1.561E2, 7.663E1)),
            850 :   sum((1.163E-2, 1.761E-3, 6.229E-6, 5.691E-4, 3.430E1,  6.050E-2, 1.159E-4, 3.961E-4, 1.886E2, 9.276E1)),
            900 :   sum((1.221E-2, 1.865E-3, 6.594E-6, 5.971E-4, 3.681E1,  6.179E-2, 1.587E-4, 3.911E-4, 2.252E2, 1.110E2)),
            950 :   sum((1.278E-2, 1.969E-3, 6.962E-6, 6.250E-4, 3.926E1,  6.293E-2, 2.087E-4, 3.899E-4, 2.662E2, 1.314E2)),
            1000:   sum((1.334E-2, 2.072E-3, 7.326E-6, 6.528E-4, 4.163E1,  6.392E-2, 2.660E-4, 3.932E-4, 3.118E2, 1.541E2))}

    if plot:
        plot_width(w_sm)
        
    m1 = 125. # GeV, recommended by the Yellow Report Section 4
    m2 = mres
    width_2_to_11 = (lambda112**2 * np.sqrt(1-4*m1**2/m2**2)) / (8*np.pi*m2)
    width_2 = stheta**2*w_sm[m2] + width_2_to_11
    return np.round(width_2, 6)
    
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
            lambda111id = '15'
            lambda112id = '16'
                    
        line = line.rstrip().replace('set param_card mass {} MASS'.format(pdgid),
                                     'set param_card mass {} {}'.format(pdgid, pars[0]))
        if 'Singlet' in model:
            line = line.rstrip().replace('set param_card bsm {} STHETA'.format(sthetaid),
                                         'set param_card bsm {} {}'.format(sthetaid, pars[1]))
            line = line.rstrip().replace('set param_card bsm {} LAMBDA112'.format(lambda112id),
                                         'set param_card bsm {} {}'.format(lambda112id, pars[2]))
            line = line.rstrip().replace('set param_card bsm {} LAMBDA111'.format(lambda111id),
                                         'set param_card bsm {} {}'.format(lambda111id, pars[3]))
            wres = calc_width(mres=pars[0], stheta=pars[1], lambda112=pars[2])
            line = line.rstrip().replace('set param_card decay {} WIDTH'.format(pdgid),
                                         'set param_card decay {} {}'.format(pdgid, wres))
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

def ntos(n, around=None):
    """Converts float to string"""
    if around is not None:
        n = np.round(n, around)
    return str(n).replace('.', 'p').replace('-', 'm')

def main(opt):
    model = opt.model
    template_dirs = {'Singlet_nores': 'SingletModel/cards_templates_nores/',
                     'Singlet_resonly': 'SingletModel/cards_templates_resonly/',
                     'Singlet_all': 'SingletModel/cards_templates_all/'}
    dir_out = opt.out
    dir_template = template_dirs[dir_out]
    
    ## read template cards
    if 'Singlet' in model:
        template_name = '{model}_hh_STstheta_Llambda_Kkap_Mmass'.format(model=model)
    else:
        template_name = '{model}_hh_width_Mmass'.format(model=model)
    cont = CardsContent(dir_template, template_name)

    ## list of parameters being scanned
    # mass_points = (250, 260, 270, 280, 290, 300, 320, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800,
    #                850, 900, 950, 1000)
    mass_points = (250, 350, 450, 550, 650, 750, 850, 950)
    stheta_points = np.arange(0.,1.1,.2) # sine of theta mixing between the new scalar and the SM Higgs
    lambda112_points = np.arange(-300,301,100) # resonance coupling with two Higgses
    lambda111_sm = np.round(125**2 / (2*246.), 6) # tri-linear Higgs coupling
    k111_points = (1.,) #np.arange(-7,12) # tri-linear kappa

    common_pars = (model, cont)
    for mass in tqdm(mass_points):
        if 'Singlet' in model:
            for stheta in stheta_points:
                for k111 in k111_points:
                    for lbd112 in lambda112_points:
                        card_name = model + '_hh_ST' + ntos(stheta, 1) + '_L' + ntos(lbd112) + '_K' + ntos(k111) + '_M' + str(mass)
                        dir_name = '{dir_out}/{card_dir}/'.format(dir_out=dir_out, card_dir=card_name)
                        generate_card((mass, stheta, lbd112, k111*lambda111_sm), dir_name, card_name, *common_pars)
        
        else:
            width_points = (0., 0.1,)
            for width in width_points:
                width_in_gev = '1.0e-03' if width==0 else str(width*float(mass))
                width_str = 'narrow' if width==0 else '{}pcts'.format(int(100*width))
                card_name = '{model}_hh_{width}_M{mass}'.format(model=model, width=width_str, mass=mass)
                dir_name = '{dir_out}/{card_dir}/'.format(dir_out=dir_out, card_dir=card_name)
                generate_card((mass, width), dir_name, card_name, *common_pars)
          

    if 'Singlet' in model:
        print("{} cards were generated.".format(len(mass_points)*len(stheta_points)*len(lambda112_points)*len(k111_points)))
    else:
        print("{} cards were generated.".format(len(width_points)))
        
if __name__=='__main__':
    example = 'python generateCards.py --out TestSinglet --template SingletModel/cards_templates/ --model Singlet'
    parser = argparse.ArgumentParser(description="Generate datacards. \nExample: " + example)
    parser.add_argument('--out', choices=('Singlet_resonly', 'Singlet_nores', 'Singlet_all'),
                        help='Output directory for datacards')
    parser.add_argument('--model', choices=('BulkGraviton', 'RSGraviton', 'Radion', 'Singlet'),
                        help='Model to process')
    FLAGS = parser.parse_args()
    main(FLAGS)

import numpy as np
import matplotlib.pyplot as plt
from rebin import rebinSAS
from scipy.optimize import curve_fit
import subprocess

# plot data? - and related choices
PLOT_DATA       = False
PLOT_PR_FIT     = False
PLOT_HIGHLIGHT  = False
q1,q2           = 0.065,0.085
SCALE           = True  
LOG             = True
ERRORBAR        = True
LEGEND          = False
AGE             = False
SPECIAL         = False  # graphical abstract
NM              = True
if NM:
    q1 *= 10
    q2 *= 10

# plot Guinier?
PLOT_GUINIER    = False

# plot p(r)?
PLOT_PR         = False
norm_pr         = 2 # 1: I0, 2: pr_max
MINIMA_ONLY     = False

# prepare input files for fit - and related choices
PREPARE_FIT     = False
# selected_models = [1] # polymer
# selected_models = [2,3,4] # ellipsoids
# selected_models = [5,6,7] # polydisperse spheres
# selected_models = [0]
selected_models = [10]

# run fits (call bash script)
RUN_FIT         = False

# plot fit - related choices: SCALE, LOG, POLYMER, ELLIPSOID
PLOT_FIT        = False

# plot fit all - related choices: SCALE, LOG, selected_models
PLOT_FIT_ALL    = False

# plot series of data with best models
PLOT_FIT_BEST   = False
# best_models     = [7,7,5,5,6,6,6] # polydisperse fuzzy spheres (5) with hard sphere (6) or larger population (7)
best_models     = [7,7,7,7,6,6,6] # polydisperse fuzzy spheres (5) with hard sphere (6) or larger population (7)
# best_models     = [4,4,2,3,3,3,3] # fuzzy ellipsoids (2) with hard-sphere (3) or larger population (4)

# plot one each data with alternative models
PLOT_FIT_ALTERNATIVE  = True
# alternative_models    = [2,3,4] # ellipsoids models
# alternative_models    = [5,6,7] # pd spheres models
# alternative_models    = [2,5,1] # ellipsoids                      vs    pd spheres                      vs       polymers
# alternative_models    = [2,5] # ellipsoids                        vs    pd spheres
# alternative_models    = [2,5,7] # ellipsoids                      vs    pd spheres                      vs      pd spheres + large population   
# alternative_models    = [2,5,7,1] # ellipsoids                    vs    pd spheres                      vs      pd spheres + large population     vs      polymer
# alternative_models    = [3,5] # ellipsoids with hard-sphere       vs    pd spheres 
# alternative_models    = [3,5,7] # ellipsoids with hard-sphere     vs    pd spheres                      vs      pd spheres + large population
# alternative_models    = [3,5,7,1] # ellipsoids with hard-sphere   vs    pd spheres                      vs      pd spheres + large population     vs polymer
# alternative_models    = [3,6] # ellipsoids with hard-sphere         vs    pd spheres with hard-sphere
# alternative_models    = [3,7] # ellipsoids with hard-sphere       vs    pd spheres + large population
# alternative_models    = [4,7] # ellipsoids + large population     vs    pd spheres + large population
alternative_models    = [0,10] # smalp                            vs    smalp + smalp bimodal      

# common plot save plot options
SAVE            = True
fileformat      = '.svg'

# Models: 
Models = [\
    ['','SMALP NDs','green'], # 0\
    ['_polymer','polymer','teal'],# 1\
    ['_ellipsoid','fuzzy ellipsoid','black'],# 2\
    ['_ellipsoid_HS','ellipsoid, hard-sphere','black'],# 3\
    ['_ellipsoids2','ellipsoids + large pop.','black'],# 4\
    ['_fuzzy_sphere','polydisperse fuzzy spheres','red'],# 5\
    ['_fuzzy_sphere_HS','pd fuzzy sphere, hard-sphere','red'],# 6\
    ['_fuzzy_spheres2','pd fuzzy spheres + large pop.','grey'],# 7\
    ['_fuzzy_sphere_wrong','fuzzy sphere, wrong pd distribution','orange'],# 8\
    ['_fuzzy_sphere_wrong_HS','fuzzy sphere hard-sphere, wrong pd distribution','purple'],# 9\
    ['_bimodal','SMALP NDs + large SMALP NDs','blue'], # 10\

]

SMA = [\
    # ['467467_SMA_0p5prc','#d70303','0.5%'],\
    # ['467466_SMA_1prc','#d2691e','1.0%'],\
    # ['467465_SMA_1p5prc','#f0b300','1.5%'],\
    # ['467464_SMA_2prc','#1f9e55','2.0%'],\
    ['467463_SMA_2p5prc','#00bae8','2.5%'],\
    # ['467462_SMA_3prc','#1644FC','3.0%'],\
    # ['467461_SMA_5prc','#af1edf','5.0%'],\
]

SMALP = [\
    # August samples
    ['467480_SMA0p5_DMPC_Aug',"#d70303",'0.5'],\
    # ['467482_SMA1p0_DMPC_Aug','#d2691e','1.0'],\
    # ['467483_SMA1p5_DMPC_Aug',"#f0b300",'1.5'],\
    # ['467484_SMA2p0_DMPC_Aug',"#1f9e55",'2.0'],\
    # ['467485_SMA2p5_DMPC_Aug',"#00bae8",'2.5'],\
    # ['467486_SMA3p0_DMPC_Aug',"#1644FC",'3.0'],\
    # ['467487_SMA5p0_DMPC_Aug',"#af1edf",'5.0'],\

    # June samples
    # ['467488_SMA0p5_DMPC_Jun','#d70303','0.5'],\
    # ['467489_SMA1p0_DMPC_Jun','#d2691e','1.0'],\
    # ['467490_SMA1p5_DMPC_Jun','#f0b300','1.5'],\
    # ['467491_SMA2p0_DMPC_Jun','#1f9e55','2.0'],\
    # ['467492_SMA2p5_DMPC_Jun','#00bae8','2.5'],\
    # ['467493_SMA3p0_DMPC_Jun','#1644FC','3.0'],\
    # ['467494_SMA5p0_DMPC_Peak1_Jun','#af1edf','5.0'],\
    # ['467495_SMA5p0_DMPC_Peak2_Jun','grey','5.0 [2 months], Peak 2'],\
    # ['467495_SMA5p0_DMPC_Peak2_Jun','grey','5.0'],\
]

datasets = {
    "SMALP": (SMALP,"SMALP",'.',10),
    # "SMA": (SMA,"SMA","polymer",50),
}
    
for title,(elements,short_name,folder,skip) in datasets.items():
    
    if short_name not in ['SMA','SMALP']:
        print('short_name option does not exist for short_name: ' + short_name)
        exit()

    if PLOT_DATA:
        if SCALE:
            plt.figure(figsize=(5,8))
        else:
            if SPECIAL:
                #plt.figure(figsize=(10,5))
                plt.figure(figsize=(5,5))
            else:
                plt.figure(figsize=(5,8))
        plt.rcParams.update({'font.size': 11.5})
        scale = 1
        for element in elements:

            # import data
            name,color,label = element
            zorder = 1
            scale_extra = 1
            if AGE: 
                if '_Jun' in name:
                    label += ' [2 months]'
                    color = 'black'
                    scale_extra = 1e7
                    if 'Peak2' in name:
                        color = 'grey'
                        label += ', Peak 2 '
                        zorder = 2
                    if 'Peak1' in name:
                        label += ', Peak 1 '
                elif '_Aug' in name:
                    label += ' [1 week]'
                    zorder = 3
                
            color_prev = color
            filename = folder + '/' + name + '.dat'
            q,I,dI = np.genfromtxt(filename,comments='#',unpack=True)
            if NM: 
                q *= 10

            # skip first points
            q,I,dI = q[skip:],I[skip:],dI[skip:] 

            # rebin data
            q,I,dI = rebinSAS(q,I,dI,'log',1.03)
            filename_RB = folder + '/' + name + '_RB.dat'
            with open(filename_RB,'w') as f:
                f.write('# Rebinned data: %s\n' % filename_RB)
                f.write('# Original data: %s\n' % filename)
                f.write('# q I dI\n')
                for i in range(len(q)):
                    f.write('%f %f %f\n' % (q[i],I[i],dI[i]))

            if PLOT_PR_FIT:
                filename = 'results_' + name + '.dat/fit.dat'
                q_pr,I_pr = np.genfromtxt(filename,usecols=[0,1],unpack=True)
                if NM:
                    q_pr *= 10

            # normalization
            if short_name == "SMA":
                q_norm          = 0.2
            elif short_name == 'SMALP':
                q_norm          = 0.13
            if NM:
                    q_norm *= 10
            idx = np.where(q>q_norm)
            idx_norm = idx[0][0]
            I_norm = I[idx_norm]
            I /= I_norm
            dI /= I_norm
            if PLOT_PR_FIT:
                I_pr /=I_norm

            # scale
            if SCALE:
                I *= scale*scale_extra
                dI *= scale*scale_extra
                if PLOT_PR_FIT:
                    I_pr *= scale*scale_extra
                scale *= 0.1

            # plot data
            if ERRORBAR:
                plt.errorbar(q,I,yerr=dI,linestyle='none',marker='.',markersize=10,zorder=0,color=color,label=label)
            else:
                if SPECIAL:
                    plt.plot(q,I,linestyle='none',marker='.',markersize=10,zorder=0,color='darkred',label=label)
                    #plt.plot(q,I,linestyle='none',marker='.',markersize=10,zorder=0,color='grey',label=label)
                    #plt.plot(q,I,linestyle='none',marker='.',markersize=10,zorder=0,color='brown',label=label)
                else:
                    plt.plot(q,I,linestyle='none',marker='.',markersize=10,zorder=zorder,color=color,label=label) #markersize=10
            if PLOT_PR_FIT:
                # plt.plot(q_pr,I_pr,zorder=1,color='black')
                plt.plot(q_pr,I_pr,zorder=1,color='black')
        if short_name == 'SMA':
            if NM:
                plt.xlim(0.1,4)
            else:
                plt.xlim(0.01,0.4)
        elif short_name == 'SMALP':
            if NM:
                plt.xlim(0.08,4)
            else:
                plt.xlim(0.008,0.4)
        if LOG:
            plt.xscale('log')
        plt.yscale('log')
        if not SPECIAL:
            if NM:
                plt.xlabel(r'$q$ [nm$^{-1}$]')
            else:
                plt.xlabel(r'$q$ [$\mathrm{\AA}^{-1}$]')

        if SCALE: 
            if not SPECIAL:
                plt.ylabel(r'$I(q)$ [a.u]')
            if LEGEND:
                plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
        else:
            if not SPECIAL:
                if NM:
                    plt.ylabel(r'Normalized intensity, $I(q)/I(q=%1.2f$ nm$^{-1})$' % q_norm)
                else:
                    plt.ylabel(r'Normalized intensity, $I(q)/I(q=%1.2f$ $\mathrm{\AA}^{-1})$' % q_norm)
            if LEGEND:
                if short_name == 'SMA': 
                    plt.legend(frameon=False,title='conc. (w/v)')
                elif short_name == 'SMALP':
                    plt.legend(frameon=False,title='polymer/lipid ratio (w/w)')
        plt.tight_layout()
        if PLOT_HIGHLIGHT:
            ymin, ymax = plt.ylim()
            plt.fill_betweenx([ymin, ymax],q1,q2,color="lightgrey",alpha=0.3,zorder=0) 
            plt.ylim(ymin,ymax)
        
        if SPECIAL:
            plt.xticks([])
            plt.yticks([])
            for pos in ['right', 'top', 'bottom', 'left']:
            #for pos in ['right', 'top']:
                plt.gca().spines[pos].set_visible(False)
            plt.tick_params(axis='x', which='both', bottom=False,top=False, labelbottom=False)
            plt.tick_params(axis='y', which='both', right=False,left=False, labelleft=False)

        if SAVE:
            if SPECIAL:
                 plt.savefig(short_name + '_special' + fileformat)
            elif SCALE:
                plt.savefig(short_name + '_scale' + fileformat)
            else: 
                plt.savefig(short_name + fileformat)

    if PLOT_GUINIER:
        plt.figure(figsize=(5,8))
        scale = 1
        if short_name == 'SMA':
            q2_min = 0.00014
            q2_max = 0.006
        elif short_name == 'SMALP':
            q2_min = 0.0
            q2_max = 0.0020
            plt.xticks([0.0000, 0.0005, 0.0010, 0.0015, 0.0020])  
            if NM:
                 plt.xticks([0.00, 0.05, 0.10, 0.15, 0.20]) 
        if NM: 
            q2_min *= 100
            q2_max *= 100

        for element in elements:

            # import data
            name,color,label = element
            filename = folder + '/' + name + '_RB.dat'
            q,I,dI = np.genfromtxt(filename,comments='#',unpack=True)

            # truncation
            idx = np.where((q**2<q2_max) & (q**2>q2_min))
            
            # transformation
            q2 = q[idx]**2
            lnI = np.log(I[idx])
            dlnI = dI[idx]/I[idx]

            # fit
            def func(q2, slope, lnI0):
                return slope * q2 + lnI0
            popt, pcov = curve_fit(func, q2, lnI, sigma=dlnI)
            # popt, pcov = curve_fit(func, q2[20:], lnI[20:], sigma=dlnI[20:])
            lnI_fit = func(q2,*popt)
            print(f"Guinier fit slope: {popt[0]:.1f}")

            # normalization
            lnI_norm = -lnI[0]
            lnI /= lnI_norm
            dlnI /= lnI_norm
            lnI_fit /= lnI_norm

            # scale
            if SCALE:
                lnI += scale - 1
                lnI_fit += scale - 1
                scale += 0.05

            plt.errorbar(q2,lnI,linestyle='none',marker='.',markersize=10,color=color,zorder=0,label=name)
            plt.plot(q2,lnI_fit,color='black')
        plt.xlim(0.0,q2_max)
        if NM:
            plt.xlabel(r'$q^2$ [nm$^{-2}$]')
        else:
            plt.xlabel(r'$q^2$ [$\mathrm{\AA}^{-2}$]')

        if SCALE: 
            plt.ylabel(r'$\ln(I)$ [a.u]')
            if LEGEND:
                plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
        else:
            plt.ylabel(r'$lnI(q^2)$')
            if LEGEND: 
                plt.legend()
        plt.tight_layout()

        if SAVE:
            if SCALE:
                plt.savefig(short_name + '_guinier_scale' + fileformat)
            else: 
                plt.savefig(short_name + '_guinier' + fileformat)

    if PLOT_PR:
        if MINIMA_ONLY:
            plt.figure(figsize=(5,4))
            plt.rcParams.update({'font.size': 20})
            linewidth=5
        else:
            plt.figure(figsize=(5,8))
            linewidth=2
        r_max = 0
        for element in elements:      
            
            # import p(r)
            name,color,label = element
            #name += '_RB'
            filename = 'results_' + name + '.dat/pr.dat'
            r,pr = np.genfromtxt(filename,usecols=[0,1],unpack=True)
            if NM:
                r *= 0.1
                unit = 'nm'
            else:
                unit = 'Å'
            print(f"p(r) min at: {r[np.argmin(pr)]:.1f} {unit}")
            print(f"p(r) max at: {r[np.argmax(pr)]:.1f} {unit}")
            if norm_pr == 1:
                dr = r[6]-r[5]
                norm = np.sum(pr)*dr
            elif norm_pr == 2:
                norm = np.max(pr)
            pr /= norm
            plt.plot(r,pr,linewidth=linewidth,color=color,label=name)
            if np.max(r) > r_max:
                r_max = np.max(r)
        if NM:
            r_max = np.floor(r_max/2.5)*2.5
        else:
            r_max = np.floor(r_max/25)*25
        plt.plot([0,r_max],[0,0],linestyle='--',color='black')
        if LEGEND:
            plt.legend()
        plt.xlim(0,r_max)
        if MINIMA_ONLY:
            if NM:
                plt.xlim(2.2,3.6)
            else:
                plt.xlim(22,36)
            plt.ylim(-0.4,0.4)
            plt.yticks([])
            plt.grid()
        else:
            if NM:
                plt.xlabel(r'$r$[nm]')
            else:
                plt.xlabel(r'$r$[$\mathrm{\AA}$]')
            plt.ylabel(r'$p(r)$')
        #plt.title(title)
        plt.tight_layout()
        if SAVE:
            plt.savefig(short_name + '_pr' + fileformat)

    if PREPARE_FIT or RUN_FIT or PLOT_FIT or PLOT_FIT_ALL:
  
        Models_selected = [Models[i] for i in selected_models]

        for Model in Models_selected:
            
            extension,name,model_color = Model

            if PREPARE_FIT:
                plt.figure(figsize=(5,8))
                for element in elements:
                    # import data
                    name,color,label = element
                    number = name.split('_')[0]
                    number += extension

                    # read from template input file
                    f_template_name = 'input_NUMBER'
                    f_template_name += extension    
                    f_template = open(f_template_name,'r')
                    lines = f_template.readlines()
                    f_template.close()

                    # make input file with rebinned data
                    number_RB = number + '_RB'
                    filename_RB = folder + '/' + name + '_RB.dat'
                    input_filename_RB = 'input_' + number_RB 
                    f_RB = open(input_filename_RB,'w')
                    out_dir = folder + '/' + number_RB
                    f_RB.write('%s   \t# output folder\n' % out_dir)
                    f_RB.write('1			# number of datasets\n')
                    f_RB.write('%s \t# data\n' % filename_RB)
                    for line in lines[3:]:
                        f_RB.write('%s' % line)
                    f_RB.close()
                    print('input file: ' + input_filename_RB)
                    
                if extension:
                    f_run_template_name = 'run_diamondEXTENSION_RB.sh'
                else:
                    f_run_template_name = 'run_diamond_RB.sh'
                f_run_template = open(f_run_template_name,'r')
                lines_run = f_run_template.readlines()
                f_run_template.close()

                # make run file
                f_run_filename = 'run_diamond' + extension + '_RB.sh'
                f_run = open(f_run_filename,'w')
                for line in lines_run:
                    if 'EXTENSION' in line:
                        f_run.write('name=%s%s%s_RB\n' % ('$','{inp}',extension))
                    else:
                        f_run.write('%s' % line)
                f_run.close()
                print('run file: ' + f_run_filename)

            if RUN_FIT:
                f_run_filename = 'run_diamond' + extension + '_RB.sh'
                rc = subprocess.call(['bash',f_run_filename])

            if PLOT_FIT:
                
                for element in elements:
                    # import data
                    name,color,label = element
                    number = name.split('_')[0]
                    number += extension
                    number_RB = number + '_RB'
                    filename_RB = folder + '/' + number_RB + '/fit_dataset0.dat'
                    print('plotting: ' + filename_RB)
                    q,I,dI,Ifit = np.genfromtxt(filename_RB,skip_header=1,usecols=[0,1,2,4],unpack=True)
                    if NM:
                        q *= 10
                    R = (I-Ifit)/dI
                    Rmax = np.ceil(np.amax(abs(R)))

                    chi2r = np.sum(R**2)/(len(q)-5)

                    if AGE: 
                        if '_Jun' in name:
                            label += ' [2 months]'
                            color = 'black'
                            scale_extra = 1e7
                            if 'Peak2' in name:
                                color = 'grey'
                                label += ', Peak 2 '
                                zorder = 2
                            if 'Peak1' in name:
                                label += ', Peak 1 '
                        elif '_Aug' in name:
                            label += ' [1 week]'
                            zorder = 3

                    fig,(p0,p1) = plt.subplots(2,1,gridspec_kw={'height_ratios': [4,1]},sharex=True)
                    p0.errorbar(q,I,yerr=dI,linestyle='none',marker='.',markersize=10,color=color,zorder=1,label='%s $\chi^2_r$: %1.1f' % (label,chi2r))
                    p0.plot(q,Ifit,color='black')
                    if LOG: 
                        p0.set_xscale('log')
                    p0.set_yscale('log')
                    p0.legend(frameon=False)
                    p0.set_ylabel(r'$I(q) [cm^{-1}]$')

                    p1.plot(q,R,linestyle='none',marker='.',markersize=10,color=color,zorder=1)
                    xlim = p0.get_xlim()
                    p1.plot(xlim,np.zeros(2),color='black')
                    if Rmax > 3:
                        p1.set_ylim(-Rmax,Rmax)
                        if Rmax < 10:
                            p1.set_yticks([-Rmax,-3,0,3,Rmax])
                            p1.plot(xlim,np.ones(2)*-3,color='black',linestyle='--')
                            p1.plot(xlim,np.ones(2)*3,color='black',linestyle='--')
                        else:
                            p1.set_yticks([-Rmax,0,Rmax])  
                    if LOG:          
                        p1.set_xscale('log')
                    if NM: 
                        p1.set_xlabel(r'q [nm$^{-1}$]')
                    else:
                        p1.set_xlabel(r'q [$\mathrm{\AA}^{-1}$]')
                    p1.set_ylabel(r'$\Delta I/\sigma$')

                    plt.tight_layout()

                    if SAVE:
                        plt.savefig(name + '_fit' + fileformat)

            if PLOT_FIT_ALL:
                plt.figure(figsize=(5,8))
                scale = 1
                for element in elements:
                    # import data
                    name,color,label = element
                    number = name.split('_')[0]
                    number += extension
                    number_RB = number + '_RB'
                    if extension == '_bimodal':
                        filename_RB = folder + '/' + number_RB + '/fit_dataset0.dat'
                    else:
                        filename_RB = folder + '/' + number_RB + '/fit_' + number_RB + '_dataset0.dat'
                    print(filename_RB)
                    q,I,dI,Ifit = np.genfromtxt(filename_RB,skip_header=1,usecols=[0,1,2,4],unpack=True)
                    if NM:
                        q *= 10

                    # normalization
                    q_norm = 0.13
                    if NM:
                        q_norm *= 10
                    idx = np.where(q>q_norm)
                    idx_norm = idx[0][0]
                    factor = I[idx_norm]
                    I /= factor
                    dI /= factor
                    Ifit /= factor

                    # scale
                    if SCALE:
                        I *= scale
                        dI *= scale
                        Ifit *= scale
                        scale *= 0.1  

                    # plot data and fit
                    plt.errorbar(q,I,yerr=dI,linestyle='none',marker='.',markersize=10,color=color,zorder=0,label=name)
                    plt.plot(q,Ifit,color='black',zorder=1)
                
                if LOG:
                    plt.xscale('log')
                plt.yscale('log')
                if NM:
                    plt.xlabel(r'q [nm$^{-1}$]')
                else:
                    plt.xlabel(r'q [$\mathrm{\AA}^{-1}$]')
                if SCALE: 
                    plt.ylabel(r'$I(q)$ [a.u]')
                    if LEGEND:
                        plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
                else:
                    plt.ylabel(r'$I(q)/I(q=%1.2f)$' % q_norm)
                    if LEGEND:
                        plt.legend()
                plt.tight_layout()
                if SAVE:
                    if SCALE:
                        plt.savefig(short_name + '_fit_scale' + fileformat)
                    else: 
                        plt.savefig(short_name + '_fit' + fileformat)

    if PLOT_FIT_ALTERNATIVE:
        Models_alternative = [Models[i] for i in alternative_models]
        for i,element in enumerate(elements):
                for element in elements:

                    fig,(p0,p1) = plt.subplots(2,1,gridspec_kw={'height_ratios': [4,1]},sharex=True,figsize=(5,8))
                    Rmax = 0
                    for i,M in enumerate(Models_alternative):

                        extension,model_name,model_color = M

                        # import data
                        name,color,label = element
                        number = name.split('_')[0]
                        number += extension
                        number_RB = number + '_RB'
                        filename_RB = folder + '/' + number_RB + '/fit_dataset0.dat'
                        print('plotting: ' + filename_RB)

                        q,I,dI,Ifit = np.genfromtxt(filename_RB,skip_header=1,usecols=[0,1,2,4],unpack=True)
                        R = (Ifit-I)/dI
                        chi2r = np.sum(R**2)/(len(q)-5)
                        Rmax = np.max([np.ceil(np.amax(abs(R))),Rmax])
                        if NM:
                            q *= 10
                        if i == 0:
                            # p0.errorbar(q,I,yerr=dI,linestyle='none',marker='.',color='black',zorder=1,label=name)
                            # p1.plot(q,np.zeros_like(q),linestyle='none',marker='.',color='black')
                            p0.errorbar(q,I,yerr=dI,linestyle='none',marker='.',markersize=10,color=color,zorder=1,label='SMA ' + label)
                            p1.plot(q,np.zeros_like(q),linestyle='none',marker='.',markersize=10,color=color)
                        p0.plot(q,Ifit,color=model_color,label='%s $\chi^2_r$: %1.1f' % (model_name,chi2r))
                        p1.plot(q,R,color=model_color)
                    if LOG: 
                        p0.set_xscale('log')
                    p0.set_yscale('log')
                    p0.legend(frameon=False)
                    p0.set_ylabel(r'$I(q) [cm^{-1}]$')

                    xlim = p0.get_xlim()
                    #p1.plot(xlim,np.zeros(2),color='black')
                    if Rmax > 3:
                        p1.set_ylim(-Rmax,Rmax)
                        if Rmax < 10:
                            p1.set_yticks([-Rmax,-3,0,3,Rmax])
                            p1.plot(xlim,np.ones(2)*-3,color='black',linestyle='--')
                            p1.plot(xlim,np.ones(2)*3,color='black',linestyle='--')
                        else:
                            p1.set_yticks([-Rmax,0,Rmax])  
                    if LOG:          
                        p1.set_xscale('log')
                    if 1 in alternative_models:
                        p0.set_ylim(2e-3,0.13)
                    if NM:
                        p1.set_xlabel(r'q [nm$^{-1}$]')
                    else:
                        p1.set_xlabel(r'q [$\mathrm{\AA}^{-1}$]')
                    p1.set_ylabel(r'$\Delta I/\sigma$')

                    plt.tight_layout()
                    if SAVE:
                        plt.savefig(short_name + '_fit_alternatives' + fileformat)

    if PLOT_FIT_BEST:
        plt.figure(figsize=(5,8))
        Models_best = [Models[i] for i in best_models]
        scale = 1
        for i,element in enumerate(elements):
            extension,model_name,model_color = Models_best[i]

            # import data
            name,color,label = element
            number = name.split('_')[0]
            number += extension
            number_RB = number + '_RB'
            filename_RB = folder + '/' + number_RB + '/fit_dataset0.dat'
            print('data: ' + filename_RB + ' fitted with ' + model_name)
            q,I,dI,Ifit = np.genfromtxt(filename_RB,skip_header=1,usecols=[0,1,2,4],unpack=True)
            if NM: 
                q *= 10

            # normalization
            q_norm = 0.13
            if NM:
                q_norm *= 10
            idx = np.where(q>q_norm)
            idx_norm = idx[0][0]
            factor = I[idx_norm]
            I /= factor
            dI /= factor
            Ifit /= factor

            # scale
            if SCALE:
                I *= scale
                dI *= scale
                Ifit *= scale
                scale *= 0.1  

            # plot data and fit
            plt.errorbar(q,I,yerr=dI,linestyle='none',marker='.',markersize=10,color=color,zorder=0,label=name)
            plt.plot(q,Ifit,color='black',zorder=1)

        if LOG:
            plt.xscale('log')
        plt.yscale('log')
        plt.xlabel(r'q [$\mathrm{\AA}^{-1}$]')
        
        if SCALE: 
            plt.ylabel(r'$I(q)$ [a.u]')
            if LEGEND:
                plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
        else:
            plt.ylabel(r'$I(q)/I(q=%1.2f)$' % q_norm)
            if LEGEND:
                plt.legend()
        plt.tight_layout()
        if SAVE:
            if SCALE:
                plt.savefig(short_name + '_fit_best_scale' + fileformat)
            else: 
                plt.savefig(short_name + '_fit_best' + fileformat)

if PLOT_PR or PLOT_DATA or PLOT_GUINIER or PLOT_FIT or PLOT_FIT_ALL or PLOT_FIT_BEST or PLOT_FIT_ALTERNATIVE:
    plt.show()

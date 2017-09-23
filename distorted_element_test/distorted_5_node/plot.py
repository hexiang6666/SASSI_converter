import numpy as np
import matplotlib.pyplot as plt  
import h5py 

def h52stressStrain(h5in_filename):
	h5in=h5py.File(h5in_filename,"r")
	outputs_all=h5in['/Model/Elements/Gauss_Outputs'][()]
	stress = 1e-6*outputs_all[16 , 1:-1]
	strain = outputs_all[4  , 1:-1]
	return [stress, strain]

[stress_load,   strain_load]   = h52stressStrain("vm_2shearing.h5.feioutput")
[stress_unload, strain_unload] = h52stressStrain("vm_3unloading.h5.feioutput")
[stress_reload, strain_reload] = h52stressStrain("vm_4reloading.h5.feioutput")

stress  = np.concatenate((stress_load,stress_unload,stress_reload))
strain  = np.concatenate((strain_load,strain_unload,strain_reload))



def h52Dis(h5in_filename,initial_num):
	h5in = h5py.File(h5in_filename, "r")
	output_dis =h5in['/Model/Nodes/Generalized_Displacements'][()]
	dis =  output_dis[6,:]    ## 6 corresponds to node ID 3 
	Num_time_step = len(dis)
	time_step = list(range(initial_num, initial_num+Num_time_step))
	return [dis, time_step]



[dis_confine, time_step_confine] = h52Dis("vm_1Confine.h5.feioutput",0)

[dis_load, time_step_load] = h52Dis("vm_2shearing.h5.feioutput", time_step_confine[-1]+1)

[dis_unload, time_step_unload] = h52Dis("vm_3unloading.h5.feioutput", time_step_load[-1]+1)

[dis_reload, time_step_reload] = h52Dis("vm_4reloading.h5.feioutput", time_step_unload[-1]+1)

dis = np.concatenate((dis_confine, dis_load, dis_unload, dis_reload))

time_step = np.concatenate((time_step_confine,time_step_load,time_step_unload,time_step_reload))

# print dis, time_step

if len(dis) == len(time_step) :
	plt.plot(time_step, dis, 'k', linewidth=3)
	plt.xlabel('Time step', fontname='Arial', fontsize=42, labelpad=15) #fontweight='bold')
	plt.ylabel('$Displacement$ [m]', fontname='Arial', fontsize=42)   #fontweight='bold')
	plt.show()






#============================== Written by Yuan to plot the stress strain relationship =============================================

# plt.plot(strain, stress, 'k', linewidth= 3)
# plt.xlabel('$\epsilon$', fontname='Arial', fontsize=42, labelpad=15) #fontweight='bold')
# plt.ylabel('$\sigma$ [MPa]', fontname='Arial', fontsize=42)   #fontweight='bold')
# # plt.title('Material Behavior: Stress-Strain')
# plt.grid(False)
# plt.axis('on')

# plt.tick_params(axis='both', which='major', labelsize= 36)
# # plt.box()
# plt.savefig('standard_stress_strain.pdf')
# plt.show()

#=================================================================================================================================

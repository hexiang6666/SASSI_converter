import numpy as np
import matplotlib.pyplot as plt  
import h5py 

plt.rc('legend',**{'fontsize': 26})

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

dis_8_node = np.concatenate((dis_confine, dis_load, dis_unload, dis_reload))

time_step_8_node = np.concatenate((time_step_confine,time_step_load,time_step_unload,time_step_reload))



[dis_confine, time_step_confine] = h52Dis("../distorted_7_node/vm_1Confine.h5.feioutput",0)

[dis_load, time_step_load] = h52Dis("../distorted_7_node/vm_2shearing.h5.feioutput", time_step_confine[-1]+1)

[dis_unload, time_step_unload] = h52Dis("../distorted_7_node/vm_3unloading.h5.feioutput", time_step_load[-1]+1)

[dis_reload, time_step_reload] = h52Dis("../distorted_7_node/vm_4reloading.h5.feioutput", time_step_unload[-1]+1)

dis_7_node = np.concatenate((dis_confine, dis_load, dis_unload, dis_reload))

time_step_7_node = np.concatenate((time_step_confine,time_step_load,time_step_unload,time_step_reload))



[dis_confine, time_step_confine] = h52Dis("../distorted_6_node/vm_1Confine.h5.feioutput",0)

[dis_load, time_step_load] = h52Dis("../distorted_6_node/vm_2shearing.h5.feioutput", time_step_confine[-1]+1)

[dis_unload, time_step_unload] = h52Dis("../distorted_6_node/vm_3unloading.h5.feioutput", time_step_load[-1]+1)

[dis_reload, time_step_reload] = h52Dis("../distorted_6_node/vm_4reloading.h5.feioutput", time_step_unload[-1]+1)

dis_6_node = np.concatenate((dis_confine, dis_load, dis_unload, dis_reload))

time_step_6_node = np.concatenate((time_step_confine,time_step_load,time_step_unload,time_step_reload))


[dis_confine, time_step_confine] = h52Dis("../distorted_5_node/vm_1Confine.h5.feioutput",0)

[dis_load, time_step_load] = h52Dis("../distorted_5_node/vm_2shearing.h5.feioutput", time_step_confine[-1]+1)

[dis_unload, time_step_unload] = h52Dis("../distorted_5_node/vm_3unloading.h5.feioutput", time_step_load[-1]+1)

[dis_reload, time_step_reload] = h52Dis("../distorted_5_node/vm_4reloading.h5.feioutput", time_step_unload[-1]+1)

dis_5_node = np.concatenate((dis_confine, dis_load, dis_unload, dis_reload))

time_step_5_node = np.concatenate((time_step_confine,time_step_load,time_step_unload,time_step_reload))

# print dis, time_step

if len(dis_8_node) == len(time_step_8_node) :
	line1, = plt.plot(time_step_8_node, dis_8_node, 'k', linewidth=3, label='standard 8-node element')
	line2, = plt.plot(time_step_7_node, dis_7_node, '--r', linewidth=3, label='distorted 7-node element')
	line3, = plt.plot(time_step_6_node, dis_6_node, '*g', linewidth=3, label='distorted 6-node element')
	line4, = plt.plot(time_step_5_node, dis_5_node, '^b', linewidth=3, label= 'distorted 5-node element')
	
	# plt.legend([line1, line2, line3, line4], ['standard 8-node element', 'distorted 7-node element','distorted 6-node element', 'distorted 5-node element'])

	legend=plt.legend(bbox_to_anchor=(0.02, 0.02, 0.1, .502), loc=0, ncol=1, borderaxespad=0.)

	legend.get_frame().set_edgecolor("black")

	plt.xlabel('Time step', fontname='Arial', fontsize=42, labelpad=10) #fontweight='bold')
	plt.ylabel('$Displacement$ [m]', fontname='Arial', fontsize=42)   #fontweight='bold')
	plt.axis('on')
	plt.tick_params(axis='both', which='major', labelsize=36)
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

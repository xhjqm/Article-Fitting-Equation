import pandas as pd
import numpy as np
import os
from scipy.interpolate import make_interp_spline
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


###################################################################
#                           Input file
###################################################################
print('\nInput:')
print('---------------------------------------------------')
director_path=input('Please enter the file path of the data you want to process:\n>>>')
print('---------------------------------------------------\n')
#-----------------------------------------------------------------#


###################################################################
#     Change the working path to the path of the input file
###################################################################
director_path=director_path.replace('\\','\\')
os.chdir(director_path)
#------------------------------------------------------------------

###################################################################
#                      Split test data
#    Some text may include series times of test, for example,
#    if a text have 2 columns and 73 lines, the first columns
#    is a list from 0 to 72, represents the test angle
#    from 0 to 720, thus it contain 2 times of test (0-360 is
#    the first test, 360-720 is the second test).
###################################################################
for filename in os.listdir(director_path):
    if filename.endswith('.txt'):
        folder_name = filename[:-4]
        os.mkdir(folder_name)
        datas = pd.read_csv(filename, names=['theta', 'value'], header=None, sep='\t')
        theta = datas.loc[:, 'theta']
        line_number=len(theta)

                      #####################################################################  
        interval = 10 # This value represent the interval of test angle (can be modified) #
                      #####################################################################  
        line = []
        K = True
        while K:
            try:
                for i in range(100):
                    index = datas[datas.theta*interval== 360 * i].index.tolist()[0]
                    line.append(index)
            except:
                K = False
        G=True
        while G:
            try:
                for j in range(len(line)):
                    theta_r = datas.loc[line[j]:line[j+1], 'theta']*interval
                    value_r = datas.loc[line[j]:line[j+1], 'value']
                    data_r = pd.DataFrame({'theta': theta_r, 'value': value_r})
                    output_filename = f'{folder_name}\\Test{j + 1}.txt'
                    data_r.to_csv(output_filename, sep='\t', index=False, header=False)
            except:
                G=False
#------------------------------------------------------------------

###################################################################
#            Available color for drawing plots
###################################################################
color = ['b', 'm', 'k', 'y','tan','orange','gold','yellowgreen','hotpink','cyan','crimson']
i=-1
plt.rc('font',family='Times New Roman')
#------------------------------------------------------------------

###################################################################
#            Find test data and fit them
###################################################################
director_list=[]
for director in os.listdir(director_path):
    if os.path.isdir(director):
        director_list.append(director)
num=0
for num_director in range(len(director_list)):
    Dir=f'{director_path}\\{director_list[num_director]}'
    os.chdir(Dir)
    all_data=[]
    theta1_new_list=[]
    y_smooth_list=[]
    residuals_list=[]

    for txt in os.listdir(Dir):
        num=num+1
        print('Task:',num)
        if txt.endswith('.txt'):
            file_path = f'{Dir}\\{txt}'
            datas = pd.read_csv(file_path, names=['theta', 'value'], header=None, sep='\t')
            all_data.append(datas)
            theta1 = datas.loc[:, 'theta'] * np.pi / 180
            value1 = datas.loc[:, 'value']


            picture_name = txt[:-4]

            #################################################################################################
            # The values in next lines (A_range_of_FE, B_range_of_FE, C_range_of_FE, D_range_of_FE) can be modified to speed up fitting process
            #################################################################################################
            
            A_range_of_FE= np.inf
            B_range_of_FE = np.inf
            C_range_of_FE = 25000
            D_range_of_FE=1e-30 # use it when the scatters are axisymmetric
            #D_range_of_FE=np.inf # use it when the scatters are nonaxisymmetric
            bounds = ([0, 0, -C_range_of_FE ,  -D_range_of_FE,0],
                      [A_range_of_FE, B_range_of_FE, C_range_of_FE,D_range_of_FE,180])

            i += 1
            if i == 10:
                i = -1

            methods=['dogbox','trf']
            for method in methods:

                print('Fitting method:',method)
                try:
                    # The Fitting equation----------------------------------------------
                    def target_func(t, A, B, C, D, phi):

                        return (A) ** 2 * np.sin(t + phi * np.pi / 180) ** 4 + B ** 2 * np.cos(
                            t + phi * np.pi / 180) ** 4 + C  * np.sin(t + phi * np.pi / 180) ** 2 * np.cos(
                            t + phi * np.pi / 180) ** 2+ D*np.sin(t + phi * np.pi / 180)*np.cos(t + phi * np.pi / 180)
                    # ------------------------------------------------------------------

                    t = theta1
                    popt, povc = curve_fit(target_func, t, value1,bounds=bounds,method=method,maxfev=500)
                    y = [target_func(xx, popt[0], popt[1], popt[2], popt[3], popt[4]) for xx in t]
                    residuals = value1 - y

                    # Calculate the coefficients of Determination (R^2)-----------------
                    mean=np.mean(value1)
                    ss_tot=np.sum((value1-mean)**2)
                    ss_res=np.sum((value1-y)**2)
                    r_2=1-(ss_res/ss_tot)
                    # ------------------------------------------------------------------

                    # Calculate the max and mean residual-------------------------------
                    max_residuals = np.max(abs(residuals))
                    mean_residuals = np.mean(abs(residuals))
                    # ------------------------------------------------------------------

                    # Draw fitting results-------------------------------------------
                    theta1_new = np.linspace(theta1.min(), theta1.max(), 1000)
                    y_smooth = make_interp_spline(theta1, y)(theta1_new)
                    theta1_new_list.append(theta1_new)
                    y_smooth_list.append(y_smooth)
                    font = {'family': 'serif',
                            'serif': 'Times New Roman',
                            'weight': 'bold',
                            'size': 10}
                    plt.rc('font', **font)
                    plt.figure(figsize=(10, 6))
                    bx = plt.subplot(111, projection='polar')
                    plot_scatter2 = bx.scatter(theta1, value1, linewidth=1, color=color[i], label=txt[:-4])
                    bx.plot(theta1_new, y_smooth, color='r', linewidth=1, label='fit')
                    plt.title(f'{director_list[num_director]}-{picture_name}', fontweight='bold')
                    plt.legend(frameon=False, loc=(1, 1), fontsize=10)
                    plt.savefig(f"{file_path[:-4]}.svg", dpi=300, format="svg")
                    plt.savefig(f"{file_path[:-4]}.jpg", dpi=300, format="jpg")
                    plt.tight_layout()
                    plt.show()
                    fit_plot = pd.DataFrame({'theta_fit': theta1_new * 180 / np.pi, 'fit': y_smooth})
                    fit_plot.to_csv(f'{file_path[:-4]}-fit-point.txt', sep='\t', index=False)
                    # ------------------------------------------------------------------

                    # Drawing residuals plot--------------------------------------------
                    plt.figure(figsize=(6, 4))
                    plt.plot(datas.loc[:, 'theta'], residuals, 'o-', label='Residuals')
                    plt.xlabel('Theta')
                    plt.ylabel('Residuals')
                    plt.title(f'Residuals for {picture_name}')
                    plt.legend()
                    plt.savefig(f"{file_path[:-4]}-residuals.jpg", dpi=300, format="jpg")
                    plt.tight_layout()
                    plt.show()
                    # ------------------------------------------------------------------

                    # Record fitting parameters in to a file--------------------------------------
                    D = popt[3] if popt[0] > popt[1] else -popt[3]
                    rotate = popt[4] if popt[0] > popt[1] else popt[4] - 90
                    rotate = rotate if rotate >= 0 else 180 + rotate
                    A = popt[0] if popt[0] > popt[1] else popt[1]
                    B = popt[1] if popt[1] < popt[0] else popt[0]
                    f = open(rf'{file_path[:-4]}-formula.txt', 'w', encoding='utf-8')
                    f.write(
                        f'formula：\n\ny={A ** 2}*(np.sin((t+{rotate})*np.pi/180))**4+{B ** 2}*(np.cos((t+{rotate})*np.pi/180))**4+{popt[2]}*(np.sin((t+{rotate})*np.pi/180))**2*(np.cos((t+{rotate})*np.pi/180))**2+{D}*np.sin((t+{rotate})*np.pi/180)*np.cos((t+{rotate})*np.pi/180)')
                    f.write(
                        f'\n\na={A}\nb={B}\nc={popt[2]}\nd={D}\nPhi={rotate}°\nGamma={np.arctan(D / (A ** 2 - B ** 2)) * 180 / np.pi}')
                    f.close()
                    # ------------------------------------------------------------------

                    # Printing results--------------------------------------------------
                    print('######################')
                    print(
                        f'Test data name: {director_list[num_director]}-{picture_name}\n\nFitting Parameters:\nA={A};\nB={B};\nC={popt[2]};\nD={D};\nPhi={rotate}°;\nGamma={np.arctan(D / (A ** 2 - B ** 2)) * 180 / np.pi};')
                    print('######################\n')
                    print(f'Coefficients of Determination (R^2): {r_2}')
                    print('Max residual of this set of data: ',max_residuals)
                    print('Mean residual of this set of data: ', mean_residuals,'\n')
                    print('----------End----------\n')
                    # ------------------------------------------------------------------
                except RuntimeError:
                    maxfev = 5000
                    continue
                else:
                    break
os.chdir(director_path)
print('---------------------------------------------------\n')
print('Finish\nExit program')

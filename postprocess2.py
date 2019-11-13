import csv
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from pyomo.core import Var


def pyomo_postprocess(instance, results,data_name):
    
    instance.solutions.load_from(results)

    var_list = list()
    for v in instance.component_objects(Var, active= True):
        print('Variable',v)

        u = dict()
        u['name']= str(v)
        varobject = getattr(instance, str(v))
        for index in varobject:

            u[index]= varobject[index].value

        var_list.append(u)

    writer1 = pd.ExcelWriter('RESULTADOS_'+data_name+'.xlsx', engine='openpyxl')
    
    for variable in var_list:

        if variable['name']== 'x':
            variable.pop('name',None)
            u0 = max(key[0] for key in variable.keys())
            u1= max(key[1] for key in variable.keys())
            u2= max(key[2] for key in variable.keys())
            matrix_x = np.zeros(shape=(u2, u0, u1))
            for key in variable.keys():
                (a,b,c)=key
                matrix_x[(c-1,a-1,b-1)]=variable[key]
            print(matrix_x)

            dfx0 =pd.DataFrame(data=matrix_x[0,:,:].astype(float))
            dfx1 = pd.DataFrame(data=matrix_x[1, :, :].astype(float))
            dfx2 = pd.DataFrame(data=matrix_x[2, :, :].astype(float))
            dfx3 = pd.DataFrame(data=matrix_x[3, :, :].astype(float))
            dfx4 = pd.DataFrame(data=matrix_x[4, :, :].astype(float))
            dfx0.to_excel(writer1, sheet_name='X', startrow=0, startcol=0)
            writer1.save()
            dfx1.to_excel(writer1, sheet_name='X', startrow=0, startcol=61)
            writer1.save()
            dfx2.to_excel(writer1, sheet_name='X', startrow=0, startcol=122)
            writer1.save()
            dfx3.to_excel(writer1, sheet_name='X', startrow=0, startcol=183)
            writer1.save()
            dfx4.to_excel(writer1, sheet_name='X', startrow=0, startcol=244)
            writer1.save()
            writer1.close()

        elif variable['name'] == 'pe':
            variable.pop('name', None)
            u0 = max(key[0] for key in variable.keys())
            u1 = max(key[1] for key in variable.keys())
            u2 = max(key[2] for key in variable.keys())
            matrix_pe = np.zeros(shape=(u2, u0, u1))
            for key in variable.keys():
                (a, b, c) = key
                matrix_pe[(c - 1, a - 1, b - 1)] = variable[key]
            print(matrix_pe)

            dfpe0 = pd.DataFrame(data=matrix_pe[0, :, :].astype(float))
            dfpe1 = pd.DataFrame(data=matrix_pe[1, :, :].astype(float))
            dfpe2 = pd.DataFrame(data=matrix_pe[2, :, :].astype(float))
            dfpe3 = pd.DataFrame(data=matrix_pe[3, :, :].astype(float))
            dfpe4 = pd.DataFrame(data=matrix_pe[4, :, :].astype(float))

            dfpe0.to_excel(writer1, sheet_name='pe', startrow=0, startcol=0)
            writer1.save()
            dfpe1.to_excel(writer1, sheet_name='pe', startrow=0, startcol=6)
            writer1.save()
            dfpe2.to_excel(writer1, sheet_name='pe', startrow=0, startcol=12)
            writer1.save()
            dfpe3.to_excel(writer1, sheet_name='pe', startrow=0, startcol=18)
            writer1.save()
            dfpe4.to_excel(writer1, sheet_name='pe', startrow=0, startcol=24)
            writer1.save()
            writer1.close()

        elif variable['name'] == 't': 
            variable.pop('name', None)
            u0 = max(key[0] for key in variable.keys())
            u1 = max(key[1] for key in variable.keys())
            matrix_t = np.zeros(shape=(u0, u1))
            for key in variable.keys():
                (a, b) = key

                matrix_t[( a - 1, b - 1)] = variable[key]
            print(matrix_t)


            dft = pd.DataFrame(data=matrix_t.astype(float))
            dft.to_excel(writer1, sheet_name='t', startrow=0, startcol=0)
            writer1.save()
			writer1.close()

        elif variable['name'] == 'y':
            variable.pop('name', None)
            u0 = max(key[0] for key in variable.keys())
            u1 = max(key[1] for key in variable.keys())
            matrix_y = np.zeros(shape=(u0, u1))
            for key in variable.keys():

                (a, b) = key
                matrix_y[(a - 1, b - 1)] = variable[key]
            print(matrix_y)

            dfy = pd.DataFrame(data=matrix_y.astype(float))


            dfy.to_excel(writer1, sheet_name='y', startrow=0, startcol=0)
            writer1.save()
            writer1.close()

        elif variable['name'] == 'w':
            variable.pop('name', None)
            u0 = max(key[0] for key in variable.keys())
            u1 = max(key[1] for key in variable.keys())
            matrix_w = np.zeros(shape=(u0, u1))
            for key in variable.keys():
                (a, b) = key
                matrix_w[(a - 1, b - 1)] = variable[key]
            print(matrix_w)

            dfw = pd.DataFrame(data=matrix_w.astype(float))

            dfw.to_excel(writer1, sheet_name='w', startrow=0, startcol=0)
            writer1.save()
            writer1.close()

        elif variable['name'] == 'zmaxi':
            variable.pop('name', None)
            print(variable)

            matrix_z = np.zeros(shape=1)
            matrix_z[0]=variable[None]
            dfz = pd.DataFrame(data=matrix_z.astype(float))

            dfz.to_excel(writer1, sheet_name='z', startrow=0, startcol=0)
            writer1.save()
            writer1.close()











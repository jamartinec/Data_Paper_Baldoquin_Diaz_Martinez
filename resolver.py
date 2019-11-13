# parallel.py
from __future__ import division
from pyomo.environ import *
from GJJ_f1 import model
#from GJJ_f2 import model
#from GJJ_f3 import model 
from postprocess2 import pyomo_postprocess
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition
from pyomo.opt.parallel import SolverManagerFactory
import sys
import xlsxwriter
import time

def main():

    data = open(sys.argv[1])
    data_name = str(sys.argv[1])
    

    action_handle_map = {} 
    optsolver = SolverFactory('gurobi')
    optsolver.options['TimeLimit'] = 3600
    optsolver.options['ResultFile'] = 'gurobi' + data_name + '.sol'
    optsolver.options['OutputFlag'] = 1
    optsolver.options['LogFile'] = 'proceso' + data_name + '.txt'


    instance1 = model.create_instance(data_name)
    start = time.time()
	results = optsolver.solve(instance1, tee=True, load_solutions = False)
	end = time.time()
	tiempo = (end - start)

    if (results.solver.status == SolverStatus.ok) and (
            results.solver.termination_condition == TerminationCondition.optimal):

        registro = open('registro'+data_name+'.txt', 'w+')
        registro.write('optimal and feasible\n')
        registro.write('Clock python:' + str(tiempo) + '\n')
        registro.close()
        pyomo_postprocess(instance1, results,data_name)

    elif (( (results.solver.status == SolverStatus.aborted) or (results.solver.termination_condition == TerminationCondition.maxTimeLimit) )
          and (len(results.solution) >0)):
        results.solver.status = SolverStatus.ok
        registro = open('registro' + data_name + '.txt', 'w+')
        registro.write('aborted with feasible solution\n')
        registro.write(str(results.solver.status)+str(results.solver.termination_condition))
        registro.write('Clock python:' + str(tiempo) + '\n')
        registro.close()
        pyomo_postprocess(instance1, results, data_name)

    else:

        registro = open('registro'+data_name+'.txt', 'w+')
        registro.write(str(results.solver.status) + '\n')
        registro.write(str(TerminationCondition))
        registro.close()



if __name__ == '__main__':
    main()




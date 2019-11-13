from pyomo.environ import *

model = AbstractModel(name="m2_gulnara_version_mayo7")

model.n = Param(within=NonNegativeIntegers)

model.t_days = Param(within=NonNegativeIntegers)

model.m = Param(within=NonNegativeIntegers)

model.p_num = Param(within=NonNegativeIntegers)

model.D = Param(within=NonNegativeReals)

model.v = RangeSet(model.n+2)

model.v_n1 = RangeSet(model.n+1)

model.v_0 = RangeSet(2, model.n+2)

model.v_cst = RangeSet(2, model.n+1)

model.T = RangeSet(model.t_days)

model.M = RangeSet(model.m)

model.P = RangeSet(model.p_num)

model.d = Param(model.v, model.v, within=NonNegativeReals)

model.a = Param(model.P, model.T, within=Binary)

model.tao = Param(model.v_n1,within=NonNegativeReals)

model.e = Param(model.v_n1, within=NonNegativeReals)

model.L = Param(model.v_cst, within=NonNegativeReals)

model.nv = Param(model.v_cst, within=NonNegativeIntegers)

model.subcl1 = Set(within=model.v_cst) 

model.subcl2 = Set(within=model.v_cst) 

model.L2 = Set(within=model.P) 

model.L1 = Set(within=model.P) 

model.x = Var(model.v, model.v, model.T, within=Binary)

model.w= Var(model.v_cst, model.M, within=Binary)

model.t = Var(model.v_n1, model.T, within=NonNegativeReals)

model.y = Var(model.v_cst, model.P, within= Binary)

model.zmaxicli = Var(within=NonNegativeReals)

def cost_rule(model):
    return  sum(sum(sum (model.d[i,j]*model.x[i,j,l] for i in model.v) for j in model.v) for l in model.T)
model.cost = Objective(rule=cost_rule)

def R1(model):
    return sum(model.t[1,l] for l in model.T)== 0
model.R1= Constraint( rule=R1)

def R2(model, i):
    return sum(model.y[i,p] for p in model.L1)==1
model.R2 = Constraint(model.subcl1,rule=R2)

def R2_a(model, i):
    return sum(model.y[i,p] for p in model.L2)==1
model.R1a2 = Constraint(model.subcl2,rule=R2_a)

def R3(model,i, l):
    return sum(model.x[i,j, l] for j in model.v_0.difference({i}))== sum(model.a[p,l]*model.y[i,p] for p in model.L1)
model.R3 = Constraint(model.subcl1,model.T, rule=R3)

def R3_a(model,i, l):
    return sum(model.x[i,j, l] for j in model.v_0.difference({i}))== sum(model.a[p,l]*model.y[i,p] for p in model.L2)
model.R3_a = Constraint(model.subcl2,model.T, rule=R3_a)

def R4(model,l):
    return sum(model.x[1,j,l] for j in model.v_cst)<= model.m
model.R4 = Constraint(model.T,rule=R4)

def R5(model,l):
    return sum(model.x[1,j,l] for j in model.v_cst) - sum(model.x[i,model.n+2,l] for i in model.v_cst)==0
model.R5 = Constraint(model.T,rule=R5)

def R6(model,i,l):
    return sum(model.x[j,i,l]  for j in model.v_n1.difference({i}))-sum(model.x[i,j,l] for j in model.v_0.difference({i}))==0
model.R6=Constraint(model.v_cst, model.T,rule=R6)

def R7a(model, i, l):
    return model.t[i,l] >= model.e[i]
model.R7a = Constraint(model.v_cst, model.T, rule=R7a)

#
def R7b(model, i, l):
    return model.t[i,l] <= model.L[i]-model.tao[i]
model.R7b = Constraint(model.v_cst, model.T,rule= R7b)

# def R6a(model,l,k):
#     return model.t[1,l,k] == 0
# model.R6= Constraint(model.T, model.M, rule=R6a)
#
# def R6b(model, i, l,k):
#      return model.t[i,l,k] >= model.e[i]
# model.R6b = Constraint(model.v_cst, model.T, model.M, rule=R6b)
#
# def R6c(model, i, l,k):
#      return model.t[i,l,k] <= model.L[i]-model.tao[i]
# model.R6c = Constraint(model.v_cst, model.T,  model.M, rule= R6c)

def R8(model, i,j,l,k):
    return model.t[i,l] + model.d[i,j] + model.tao[i] - model.t[j,l] <= model.D*(1-model.x[i,j,l])
model.R8 = Constraint(model.v_n1,model.v_cst, model.T, model.M,rule=R8)

def R8b(model, i,l):
    return model.t[i,l]  <= model.zmaxicli
model.R8b = Constraint(model.v_cst, model.T,rule=R8b)

def R9(model, i,l):
    return model.t[i,l] + model.tao[i] + model.d[i,model.n+2]*model.x[i,model.n+2,l] <= model.D
model.R9 = Constraint(model.v_cst, model.T,rule=R9)

def R10(model, i):
    return sum(model.w[i,k] for k in model.M) == 1
model.R10 = Constraint(model.v_cst,rule=R10)

#R11 IS COMMENTED ONLY FOR THE EXPERIMENT WITH DISAGGREGATED RESTRICTION (R11 IS REMOVED AND IN ITS PLACE R25 IS ACTIVATED)!
def R11(model, i,j, k):
    return sum(model.x[i,j,l]  for l in model.T ) <= model.nv[i]*(1 - model.w[i, k] + model.w[j, k] )
model.R11= Constraint(model.v_cst,model.v_cst,model.M,rule=R11)

def R12(model, i, j, l, k):
    if (i==j):
        return Constraint.Skip
    else:
        return model.x[1, i, l] + model.x[1, j, l] <= 3 - (model.w[i, k] + model.w[j, k])
model.R12 = Constraint(model.v_cst,model.v_cst,model.T,model.M, rule= R12)

#disaggregated constraint (it is activated instead R11) (Equation 31 paper)
#def R25(model, i, j, l, k):
#    if (i==j):
#        return Constraint.Skip
#    else:
#        return model.x[i,j,l] <= 1-model.w[i,k] + model.w[j,k]
#model.R25 = Constraint(model.v_cst,model.v_cst,model.T,model.M, rule= R25)


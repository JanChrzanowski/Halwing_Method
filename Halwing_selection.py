import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats



def Hellwig_Selection(corr,method = ["cons", "min_max","T_student"]):

    #Method Selection to determine treshold
    if method == "min_max":

        r_values = []
        for i in corr.columns:
            cor = corr[i].loc[corr[i] < 1 ].max()
            r_values.append(cor)
            treshold = min(r_values)

    if method == "cons":
        treshold = 0.5

    if method == "T_student":
        treshold = ((stats.t.ppf(0.95, len(corr)))**2/ ((stats.t.ppf(0.95, len(corr))**2) + len(corr) - 2))**(1/2)
    
    #Absolute value of Migration Matrix
    abs_corr = abs(corr)

    #Selection of variables
    var_to_check = abs_corr.replace({1:0}).sum().idxmax()
    vars_Satellite = list(abs_corr[var_to_check].loc[abs_corr[var_to_check].values > treshold].index)
    vars_Satellite.append(var_to_check)
    return var_to_check , vars_Satellite
    
#Final Loop    
def find_variables(corr, method):

    final_variables = []    

    while not corr.empty:
        print(Hellwig_Selection(corr,method = method))
        final_variables.append(Hellwig_Selection(corr,method = method)[0])
        corr = corr.drop(Hellwig_Selection(corr,method = method)[1],axis=1).drop(Hellwig_Selection(corr,method = method)[1],axis=0)
    return final_variables


#Example of Use 

find_variables(corr , "T_student")
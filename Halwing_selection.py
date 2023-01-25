import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler



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

#Standard Scaler on prepared dataset

def standard_scaler(dataset, vars_to_stanard = []):

    ct = ColumnTransformer([('Name', StandardScaler(), vars_to_stanard )], remainder='passthrough')
    Standard = ct.fit_transform(dataset)
    Standarized_data = pd.DataFrame(Standard, columns= dataset.columns)
    
    return Standarized_data

# Stimulation of variables (only on Standarized variables!)
def Stimulation_process(dataset , list_of_destimulation = []):
    for i in list_of_destimulation:
        dataset[i] = dataset[i] * (-1)
    return dataset

def sum_ranking_method(dataset, choosen_vars):

    dataset['Sum'] = dataset[Choosen_vars].sum(axis = 1)
    dataset['Sum_scaled'] = dataset['Sum'] -  dataset['Sum'].min()
    dataset['Sum_scaled_%'] = (dataset['Sum_scaled']/ dataset['Sum_scaled'].max()) * 100
    
    return dataset.drop(choosen_vars , axis = 1).sort_values("Sum_scaled_%" , ascending = False)

def Group_STD(x,y,z):
    
    # x = value of s y = mean of s z = std of S 
    if  x < y - z:
        return "G1"
    if y > x > y - z:
        return "G2"
    if y + z > x> y:
        return "G3"
    if x > y + z:
        return "G4"



#Example of Use 

#find_variables(Correlation matrix from the dataset  , One of the method)
#standard_scaler(dataset , choosen vars from previous algorithm)
#Stimulation_process(dataset, list_of_destimulation= ['var1', 'var2' , 'var3'] as a list destimulated variables)
#sum_ranking_method(Standarized_data , Choosen_vars)
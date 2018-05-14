###########################################################################################################################
# Title: Stepwise Predictors Selection Method
# Course: Math B7800 - Advanced Mathematical Statistics II
# Instructor: Professor Shirshendu Chatterjee
# Due Date: May/15/2018, Wednesday
# Author: Minwoo Bae (minubae.math@gmail.com)
# Institute: The Department of Mathematics, City College of New York, CUNY

# Project Description:
# Consider the Benzene concentration as response Y variable and others as predictors.
# Carry out Stepwise Variable selection method to select an appropriate subset of assumptions.
# Use AIC, Adjusted R^2, and C_p plot to select suitable subset of variable.

# Data Set Information:
# The dataset contains 9358 instances of hourly averaged responses from an array of 5 metal oxide chemical sensors embedded
# in an Air Quality Chemical Multisensor Device. The device was located on the field in a significantly polluted area,
# at road level,within an Italian city. Data were recorded from March 2004 to February 2005 (one year)representing
# the longest freely available recordings of on field deployed air quality chemical sensor devices responses.
# Ground Truth hourly averaged concentrations for CO, Non Metanic Hydrocarbons, Benzene, Total Nitrogen Oxides (NOx) and
# Nitrogen Dioxide (NO2) and were provided by a co-located reference certified analyzer. Evidences of cross-sensitivities
# as well as both concept and sensor drifts are present as described in De Vito et al., Sens. And Act. B, Vol. 129,2,2008
# (citation required)eventually affecting sensors concentration estimation capabilities.
# Missing values are tagged with -200 value.
# This dataset can be used exclusively for research purposes. Commercial purposes are fully excluded.

# Data Set Sources: https://archive.ics.uci.edu/ml/datasets/Air+quality
###########################################################################################################################
import numpy as np
from numpy import transpose as T
from scipy.stats import f
from numpy.linalg import inv
from numpy import dot
import matplotlib.pyplot as plt

begin = 1
end_row = 9358 #9358
###################################################################################
# Import data from a CSV file: 'AirQualityUCI/AirQualityUCI.csv'
###################################################################################

end_col = 14
# end_col = 10
csv_url = 'AirQualityUCI/AirQualityUCI.csv'
data = np.genfromtxt(csv_url, delimiter=';', usecols = range(2,end_col), skip_header = 1, dtype=float, max_rows = end_row)
data = np.array(data, dtype=float)

# Get the Benzene concentration as a Response vector Y from the data
Y = data[begin:end_row,3]

# Get the number of observations
n = Y.shape[0]
# print('n:', n)

# Get a Data Matrix Z from the data
Z = np.delete(data,3,axis=1)[begin:end_row,] # axis=1 -- select a column, axis=0 -- select a row.

# Insert one vector into the data matrix Z
Z = np.insert(Z, 0, np.ones(n), axis=1)
Z = Z.astype(float)
# Get the number of variables in the data matrix Z
r = Z.shape[1]-1
# print('Z:')
# print(Z)
# print('r: ', r)
# print('Original Data:')
# print(data.astype(int))
###################################################################################
# Function for computing Beta_hat
###################################################################################
def getBetaHat(data, response):

    # Initialize variables
    z=[]; y=[]; beta_hat=[]

    # Set variables
    z = data; y = response

    # Compute the beta_hat
    beta_hat = inv(z.T.dot(z)).dot(z.T).dot(y)

    return beta_hat

# print('Beta_hat:')
# print(getBetaHat(Z, Y))

def isInvertible(data):
    z=0; result=0
    z = data
    result = z.shape[0] == z.shape[1] and np.linalg.matrix_rank(z) == z.shape[0]
    return result


###################################################################################
# Function for computing Projection Matrix, i.e., Pz
###################################################################################
def getProjectionMatrix(data, where):

    # Initialize variables
    z=[]; Pz=[]
    # Set variables
    z = data.astype(int)

    # w = where
    # print('where: ', w)
    # print('z')
    # print(z)

    # Compute the Projection Matrix Pz
    Pz = z.dot(inv(z.T.dot(z))).dot(z.T)

    return Pz

# print(getProjectionMatrix(Z))

###################################################################################
# Function for computing Mean Projection Matrix, i.e., P1_n
###################################################################################
def getMeanProjectionMatrix(observations):

    # Initialize variables
    n=0; P1=[]

    # Set variables
    n = observations

    # Compute the Mean Projection Matrix P1_n
    P1 = np.ones((n,n))/n

    return P1

# print('P1: ')
# print(getMeanProjectionMatrix(n))

###################################################################################
# Function for computing Predcted Response, i.e., Y_hat
###################################################################################
def getPredictedResponse(data, response):

    # Initialize variables
    Pz=[]; z=[]; y=[]; y_hat=0; y_hat1=0

    # Set variables
    z = data; y = response

    # Get the Projection Matrix Pz
    Pz = getProjectionMatrix(z, 'getPredictedResponse')

    # Get the Beta_hat
    beta_hat = getBetaHat(z, y)

    # Compute the Predicted Response y_hat
    y_hat =  Pz.dot(y)
    # y_hat1 = z.dot(beta_hat)

    return y_hat

# print('Y_hat:')
# print(getPredictedResponse(Z, Y))

###################################################################################
# Function for computing Residual Sum of Squares
###################################################################################
def getResidualSS(data, response, observations):

    # Initialize variables
    z=[]; y=[]; Pz=[]; n=0;eye=0;resSS=0;

    # Set variables
    z = data; y = response; n = observations

    # Compute the n x n identity matrix
    I = np.eye(n)

    # Get the Projection Matrix Pz
    Pz = getProjectionMatrix(z, 'getResidualSS')

    # Compute the Residual Sum of Squares
    resSS = y.T.dot(I-Pz).dot(y)

    return resSS

# print('ResidualSS: ', getResidualSS(Z,Y,n))

###################################################################################
# Function for computing Unbiased Residual Sum of Squares
###################################################################################
def getUnbiasedResidualSS(data, response, observations, variables):

    # Initialize variables
    z=[]; y=[]; n=0; r=0; s2=0

    # Set variables
    z = data; y = response; n = observations; r = variables

    # Get the Residual Sum of Squares
    residualSS = getResidualSS(z, y, n)

    # Compute the Unbiased Residual Sum of Squares, i.e., s^2
    s2 = residualSS/(n-r-1)

    return s2

# print('UnbiasedResidualSS: ', getUnbiasedResidualSS(Z, Y, n, r))

###################################################################################
# Function for computing Regression Sum of Squares
###################################################################################
def getRegressionSS(data, response, observations):

    # Initialize variables
    z=[]; y=[]; n=0; regSS=0
    z = data; y = response; n = observations

    # Get the Projection Matrix Pz
    Pz = getProjectionMatrix(z, 'getRegressionSS')

    # Get the Mean Projection Matrix P1_n
    P1 = getMeanProjectionMatrix(n)

    # Compute the Regression Sum of Squares
    regSS = y.T.dot(Pz-P1).dot(y)
    return regSS

# print('RegressionSS: ', getRegressionSS(Z, Y, n))

###################################################################################
# Function for computing Total Sum of Squares about Mean
###################################################################################
def getTotalMeanSS(data, response, observations):

    # Initialize variables
    z=[]; y=[]; n=0; totSS=0

    # Set variables
    z = data; y = response; n = observations

    # Compute the n x n Identity Matrix
    I = np.eye(n)

    # Get the Mean Projection Matrix
    P1 = getMeanProjectionMatrix(n)

    # Get the Residual Sum of Squares
    resSS = getResidualSS(z,y,n)

    # Get the Regression Sum of Squares
    regSS = getRegressionSS(z,y,n)

    # Compute the Total Sum of Squares about Mean
    # totSS = y.T.dot(I-P1).dot(y)
    totSS = resSS + regSS

    return totSS

# print('totSS: ', getTotalMeanSS(Z,Y,n))


###################################################################################
# Function for computing R2 (Ratio of Regression Sum of Squares)
###################################################################################
def getRatioRegressionSS(data, response, observations):

    # Initialize variables
    z=[]; y=[]; n=0; R2=0

    # Set variables
    z = data; y = response; n = observations

    # Get RegressionSS
    regSS = getRegressionSS(z, y, n)

    # Get Total SS about Mean
    totSS = getTotalMeanSS(z,y,n)

    # Compute the Ration of Regression SS
    R2 = regSS/totSS

    return R2

# print('R2: ', getRatioRegressionSS(Z, Y, n))

###################################################################################
# Function for computing Adjusted R2 (Adjusted Ratio of Regression Sum of Squares)
###################################################################################
def getAdjustedRatioRegressionSS(data, response, observations, variables):

    # Initialize variables
    z=[]; y=[]; n=0; r=0; Adjusted_R2=0

    # Set variables
    z = data; y = response; r = variables; n = observations

    # Get the Ration of Regression SS, i.e., R2
    R2 = getRatioRegressionSS(z, y, n)

    # Compute the Adjusted R2:
    Adjusted_R2 = 1-(1-R2)*((n-1)/(n-r-1))

    return Adjusted_R2

# print('Adjusted_R2: ', getAdjustedRatioRegressionSS(Z, Y, n, r))

def isPredictorSignificant(data, data1, response, alpha_value):

    # Initialize variables
    z=[]; z1=[]; Pz=[]; Pz1=[]; I=[]
    r=0; n=0; y=0; alpha=0; df1=0; df2=0; p_value=0; c_value=0

    # Set variables
    z = data; z1 = data1; y = response; alpha = alpha_value

    r = z.shape[1]-1
    n = z.shape[0]
    q = r-1

    I = np.eye(n)
    df1 = r-q
    df2 = n-r-1
    print('')
    print('r: ', r)
    print('q: ', q)
    print('n: ', n)
    print('df1: ', df1)
    print('df2: ', df2)

    # Get projection matrices: Pz and Pz1
    Pz = getProjectionMatrix(z, 'isPredictorSignificant')
    # print(Pz)

    if r==1:

        Pz1 = getMeanProjectionMatrix(n)
        # print(Pz1)
    else:

        Pz1 = getProjectionMatrix(z1, 'isPredictorSignificant')

    # Compute F-ratio and p-value of F-ratio on the F distribution
    numerator = y.T.dot(Pz -Pz1).dot(y)/(df1)
    denomenator = y.T.dot(I -Pz).dot(y)/(df2)

    F = numerator/denomenator
    c_value = f.ppf(1-alpha, df1, df2)

    # p_value = f.cdf(F, df1, df2)
    # print('P-value: ', p_value)

    print('F-ratio: ', F)
    print('C-value: ', c_value)
    print('level of alpha: ', 1-alpha)

    # Hypothesis test: Reject Ho or not
    if F > c_value:
        # Reject the null hypothesis H0. So the predictor is significant
        return True

    return False


###################################################################################
# Compute Akaike's Information Criterion (AIC)
# Select models having the smaller values of AIC
###################################################################################
def getAIC(data, response, observations, variables):

    z=[]; y=[]; n=0; r=0; p=0; AIC=0

    z = data; y = response; n = observations; r = variables

    p = r+1

    resSS = getResidualSS(z, y, n)
    AIC = n*np.log(resSS/n)+(2*p)

    return AIC

###################################################################################
# Compute C_p value: Select models with minimum C_p
###################################################################################
def getCp(data, data_subset, response, observations, variables):

    z=[]; zi=[]; y=[]; r=0; n=0; p=0
    numerator=0; denomenator=0; Cp=0

    z = data; zi = data_subset; y = response; r = variables
    n = observations; p = r+1

    numerator = getResidualSS(zi, y, n)
    denomenator = getResidualSS(z, y, n)

    Cp = numerator/denomenator - (n-2*p)

    return Cp

###################################################################################
# Get a Subset of Data Matrix
###################################################################################
def getSubsetDataMatrix(data, col_index):

    z=[]; zi=[]; ones=[]; index=0; n=0

    z = data; index = col_index

    n = z.shape[0]
    ones = np.ones(n)
    zi = z[:, index]

    zi = np.column_stack((ones, zi))

    return zi

###################################################################################
# Compute a predictor having the most contribution to the Regression SS:
###################################################################################
def getMostPredictorToRegSS(data, response):

    p=0; n=0; predictor_index=0
    R2=0; Adj_R2=0; AIC=0; Cp=0

    R2_vec=[]; Adj_R2_vec=[]; AIC_vec=[]
    Cp_vec=[]; index_vec=[]; z=[]; y=[]

    z = data; y = response

    p = z.shape[1]
    n = z.shape[0]

    for i in range(1,p):

        zi = getSubsetDataMatrix(z, i)

        R2 = getRatioRegressionSS(zi, y, n)
        # R2_vec = np.append(R2_vec, R2)
        R2_vec.append(R2)

        Adj_R2 = getAdjustedRatioRegressionSS(zi, y, n, 1)
        # Adj_R2_vec = np.append(Adj_R2_vec, Adj_R2)
        Adj_R2_vec.append(Adj_R2)


        AIC = getAIC(zi, y, n, 1)
        # AIC_vec = np.append(AIC_vec, AIC)
        AIC_vec.append(AIC)

        Cp = getCp(z, zi, y, n, 1)
        # Cp_vec = np.append(Cp_vec, Cp)
        Cp_vec.append(Cp)

    # print('R2', R2_vec)

    R2_max_index = np.argmax(R2_vec)+1

    Adjusted_R2_max_index = np.argmax(Adj_R2_vec)+1

    AIC_min_index = np.argmin(AIC_vec)+1

    Cp_min_index = np.argmin(Cp_vec)+1

    index_vec = np.append(index_vec, [R2_max_index, Adjusted_R2_max_index, AIC_min_index, Cp_min_index]).astype(int)

    predictor_index = np.bincount(index_vec).argmax()


    # plot = [R2_max_index, Adjusted_R2_max_index, AIC_min_index, Cp_min_index]

    return predictor_index

###################################################################################
# Compute an Initial Data matrix with a predictor showing the most contribution
# to the Regression Sum of Squares.
###################################################################################
def getInitDataMatrix(data, response, alpha_value):

    z=[]; zi=[]; y=[]
    index=0; alpha=0; test=False

    z = data; y = response; alpha = alpha_value
    index = getMostPredictorToRegSS(z, y)

    zi = getSubsetDataMatrix(z, index)

    test = isPredictorSignificant(zi, zi[:,0], y, alpha)

    if test == True:

        return zi

    else:

        print('sorry, please try it again')
        z = np.delete(z,index,axis=1)

        return getInitDataMatrix(z, y, alpha)


def getUpdatedDataMatrix(init_data, data, response, alpha_value):
    z_int=[]; z_temp=[]; z_updated=[]; z_new=[]; z=[]; y=[]; regSS_vec=[]
    index_vec=[]

    temp=0; max_index=0; alpha=0; check1=False; check2=False; isEqual=False

    z_int = init_data; z = data; y = response; alpha = alpha_value

    n = z_int.shape[0]
    p1 = z_int.shape[1]
    p2 = z.shape[1]

    for i in range(p1):

        for j in range(p2):

            isEqual = np.array_equal(z_int[:,i], z[:,j])

            if isEqual == True:

                index_vec.append(j)

    z_updated = np.delete(z,index_vec,axis=1)

    print('z_update:')
    print(z_updated.astype(int))

    p2_new = z_updated.shape[1]


    for i in range(p2_new):

        z_temp = np.insert(z_int, p1, z_updated[:,i], axis=1)

        regSS = getRegressionSS(z_temp, y, n)

        if  regSS > temp:

            temp = regSS
            max_index = i

            print('max_index: ', max_index)

        z_temp=[]

    z1 = np.column_stack((np.ones(n), z_updated[:,max_index]))

    test = isPredictorSignificant(z_int, z1, y, alpha)

    print('test:', test)

    if test == True:

        z_new = np.insert(z_int, p1, z_updated[:,max_index], axis=1)

        return z_new

    else:

        print('Find a another predictor.')

        z = np.delete(z_updated, max_index, axis=1)

        return getUpdatedDataMatrix(z_int, z, y, alpha)


def getPredictorValidation(data, response, alpha_value):

    z=[]; y=[]; z_update=[]; validation=[]
    n=0; p=0; r=0; add=0;leaves=0; test=False
    z = data; y = response; alpha = alpha_value

    n = z.shape[0]
    p = z.shape[1]
    r = p-1

    z_update = z

    for i in range(1, p):
        print(i)
        zi = z[:,i]

        zi = np.column_stack((np.ones(n), zi))
        # print('zi: ')
        # print(zi.astype(int))

        test = isPredictorSignificant(z, zi, y, alpha)

        if test == False:
            # print('hi')
            z_update = np.delete(z, i, axis=1)
            leaves += 1

        else:

            add += 1

    print('added: ', add)
    print('leaves: ', leaves)
    # print('test: ', test)
    print('')

    validation.append(z_update)
    validation.append(add)
    validation.append(leaves)
    validation = np.array(validation)

    return validation

# print(getPredictorValidation(updatedDataMatrix, Y, alpha))


# isEqual = np.array_equal(z_int[:,i], z[:,j])

def getStepwisePredictors(data, init_data, response, alpha_value):

    alpha=0; add=0; leaves=0; n=0; p=0; r=0
    int_data=[]; validation=[]; updated_data=[]; z=[]; y=[]

    z = data; int_data = init_data; y = response; alpha = alpha_value

    n = z.shape[0]
    p = z.shape[1]
    r = p-1

    print('n: ', n)
    print('r: ', r)

    updated_data = getUpdatedDataMatrix(int_data, z, y, alpha)

    validation = getPredictorValidation(updated_data, y, alpha)

    updated_data = validation[0]

    add = validation[1]
    leaves = validation[2]

    print('Updated Data')
    print(updated_data.astype(int))

    print('add: ', add)
    print('leaves: ', leaves)

    if add+leaves < r:

        print('Sorry, please try steps further.', r)

        return getStepwisePredictors(z, updated_data, y, alpha)

    else:

        return updated_data



alpha = 0.05
init_data = getInitDataMatrix(Z, Y, alpha)

updated_model = getStepwisePredictors(Z, init_data, Y, alpha)
print('Stepwise Predictors: ')
print(updated_model.astype(int))
# print('init_data:')
# print(init_data.astype(int))


beta_hat = getBetaHat(Z, Y)
# print(beta_hat.astype(float))

p = Z.shape[1]
p1 = updated_model.shape[1]
index_vec = []
# Z = Z.astype(int)

for i in range(p1):
    for j in range(p):
        isEqual = np.array_equal(updated_model[:,i], Z[:,j])
        if isEqual == True:
            # print('delete:')
            # print(z[:,j])
            index_vec.append(j)

print(index_vec)
















# print('Hello')

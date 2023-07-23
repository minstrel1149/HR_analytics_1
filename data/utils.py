# classifying character
import pandas as pd
import numpy as np

def add_experience(df):
    df = df.assign(Experienced=lambda df: np.where(df['NumCompaniesWorked'] == 0, 'NewEmp',
                                                   np.where((df['TotalWorkingYears'] - df['YearsAtCompany']) / df['NumCompaniesWorked'] <= 1,
                                                            'FreqMove', 'ExpEmp')))
    return df

def feature_classification(df, classify='character', return_dataframe=False):
    if classify == 'character':
        char_dict = {'ID':['EmployeeNumber'],
                     'Compensation':['MonthlyIncome', 'PercentSalaryHike', 'StockOptionLevel'],
                     'Biodata':['Age', 'Gender', 'MaritalStatus', 'Education', 'EducationField', 
                                'DistanceFromHome', 'NumCompaniesWorked', 'TotalWorkingYears', 'Experienced'],
                     'Work':['Department', 'BusinessTravel', 'JobLevel', 'JobRole', 'JobInvolvement', 'OverTime', 
                             'WorkLifeBalance', 'TrainingTimesLastYear', 'YearsAtCompany', 
                             'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager'],
                     'result':['EnvironmentSatisfaction', 'JobSatisfaction', 'PerformanceRating', 'RelationshipSatisfaction', 'Attrition']}
        if return_dataframe is True:
            all_features = char_dict['ID'] + char_dict['Compensation'] + char_dict['Biodata'] + char_dict['Work'] + char_dict['result']
            return df[all_features]
        return char_dict

def astype_category(df):
    astype_category = ['Attrition', 'BusinessTravel', 'Department', 'Education', 'EducationField', 'EnvironmentSatisfaction',
                   'Gender', 'JobRole', 'MaritalStatus', 'OverTime']
    astype_dict = dict.fromkeys(astype_category, 'category')
    df = df.astype(astype_dict)
    return df


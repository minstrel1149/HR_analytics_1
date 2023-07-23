# classifying character
import pandas as pd

def feature_classification(df, classify='character'):
    if classify == 'character':
        char_dict = {'ID':['EmployeeNumber'],
                     'Compensation':['DailyRate', 'HourlyRate', 'MonthlyRate', 'MonthlyIncome', 'PercentSalaryHike', 'StockOptionLevel'],
                     'Biodata':['Age', 'Over18', 'Gender', 'MaritalStatus', 'Education', 'EducationField', 
                                'DistanceFromHome', 'NumCompaniesWorked', 'TotalWorkingYears'],
                     'Work':['Department', 'BusinessTravel', 'JobLevel', 'JobRole', 'JobInvolvement', 'OverTime', 
                             'WorkLifeBalance', 'StandardHours', 'TrainingTimesLastYear', 'YearsAtCompany', 
                             'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager'],
                     'result':['EnvironmentSatisfaction', 'JobSatisfaction', 'PerformanceRating', 'RelationshipSatisfaction', 'Attrition']}
        return char_dict
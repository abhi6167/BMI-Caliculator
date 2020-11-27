# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 16:41:01 2020

@author: User
"""

import pandas as pd
import sys
import re

def func_inputdata():
    input_data = [
                  {"Gender":"Male","HeightCm":171,"WeightKg":96},
                  {"Gender":"Male","HeightCm":161,"WeightKg":85},
                  {"Gender":"Male","HeightCm":180,"WeightKg":77},
                  {"Gender":"Female","HeightCm":166,"WeightKg":62},
                  {"Gender":"Female","HeightCm":150,"WeightKg":77},
                  {"Gender":"Female","HeightCm":167,"WeightKg":82},
                 ]
    return input_data

def func_CreateDataframe(list_data):
    try:
        df = pd.DataFrame.from_dict(list_data)
        return df
    except Exception as e:
        print("input is not correct")
        sys.exit(1)

def func_convert_cm_to_metersq(df,power):
    #pandas code to convert the cm into m
    try:
        df["HeightInMtrs (m2)"] = (df["HeightCm"]/100)**power
        #code to caliculate the BMI
        df["BMI (kg/m2)"] = df["WeightKg"]/df["HeightInMtrs (m2)"]
    except Exception as e:
        print(e)
        print("Enter the valid powers")
        sys.exit(1)
    return df

def func_createBMITable():
    #Creatig the BMI Category And Health Risk Table
    #this condition can be furhter read drom the excel sheet also
    category    = ["Underweight","Normal Weight","Overweight","Moderately obese",
                   "Severely Obese","Very severely obese"]
    BMI_Range   = ["18.4 and below","18.5-24.9","25-29.9",
                   "30-34.9","35-39.9","40 and above"]
    Health_Risk = ["Malnutrition risk","Low risk","Enhanced risk","Medium risk",
                   "High risk","Very high risk"]

    df_Table = pd.DataFrame({"BMI Category":category,
                         "BMI Range":BMI_Range,
                         "Health_Risk":Health_Risk})
    return df_Table

def get_BMI_Range(BMITable,Category,column_name):
    try:
        bmi_range = BMITable[BMITable[column_name]==Category]["BMI Range"].tolist()
        if len(bmi_range) == 1:
            pass
            #print("Range is valid")
        else:
            print("There should be only one range for one category")
            sys.exit(1)
    except Exception as e:
        print("Enter the correct column name")
        sys.exit(1)
    return bmi_range

def func_count(df,lower_val,upper_val):
    if type(upper_val) != str:
        counts = df[(df["BMI (kg/m2)"] > lower_val) & (df["BMI (kg/m2)"] < upper_val)]["BMI (kg/m2)"].count()
        return counts
    elif ((type(upper_val)) == str) and (str(upper_val) == "below"):
        counts = df[(df["BMI (kg/m2)"] < lower_val)]["BMI (kg/m2)"].count()
        return counts
    else:
        counts = df[(df["BMI (kg/m2)"] > lower_val)]["BMI (kg/m2)"].count()
        return counts
    
def main():
    li_data  = func_inputdata()
    df       = func_CreateDataframe(li_data)
    power    = 2
    df       = func_convert_cm_to_metersq(df,power)
    BMITable = func_createBMITable()
    column_name = "BMI Category"
    Category = "Overweight"
    bounds   = get_BMI_Range(BMITable,Category,column_name)
    if bounds[0].find("below") != -1:
        lower_bound = re.findall('[0-9\.]+', bounds[0])
        count = func_count(df,float(lower_bound[0]),"below")
        print("Count of "+Category+" people is:",count)
    elif bounds[0].find("above") != -1:
        lower_bound = re.findall('[0-9\.]+', bounds[0])
        count = func_count(df,float(lower_bound[0]),"above")
        print("Count of "+Category+" people is:",count)
    else:
        lower_bound = re.findall('[-]+', bounds[0])
        cond = bounds[0].split(lower_bound[0])
        count = func_count(df,float(cond[0]),float(cond[1]))
        print("Count of "+Category+" people is:",count)
        
    '''
    #Code to get the count of all the category
    Category = BMITable["BMI Category"].tolist()
    for i in Category:
        bounds   = get_BMI_Range(BMITable,i,column_name)
        if bounds[0].find("below") != -1:
            lower_bound = re.findall('[0-9\.]+', bounds[0])
            count = func_count(df,float(lower_bound[0]),"below")
            print("Count of "+i+" people is:",count)
        elif bounds[0].find("above") != -1:
            lower_bound = re.findall('[0-9\.]+', bounds[0])
            count = func_count(df,float(lower_bound[0]),"above")
            print("Count of "+i+" people is:",count)
        else:
            lower_bound = re.findall('[-]+', bounds[0])
            cond = bounds[0].split(lower_bound[0])
            count = func_count(df,float(cond[0]),float(cond[1]))
            print("Count of "+i+" people is:",count)
    '''
main()
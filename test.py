# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 10:48:44 2023

@author: atan1
"""

import numpy as np
import pandas as pd
# =============================================================================
# import seaborn as sb
# import matplotlib.pyplot as plt
# sb.set()
# =============================================================================

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

#hello

# =============================================================================
# from sklearn.model_selection import train_test_split
# from sklearn import linear_model
# from sklearn.linear_model import LinearRegression , LogisticRegression
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import classification_report, confusion_matrix
# lm = LinearRegression()
# logmodel = LogisticRegression()
# =============================================================================

#Opening Tkinter GUI to open File
Tk().withdraw()
print('Look for open window to open saved file')
filename = askopenfilename(title = 'Open File')
print(filename)
productDF = pd.read_excel(filename)

print("product shape: ",productDF.shape)
print(productDF.head())

#pull unique factors during deciding which car
#pull unique external componenets to customise
#pull unique internal components to customise
#assign range for category of car
#assign range for relationship
#assign range for customisation likelihood
#assign range for car customisation fee

#Creating dataframes for each header
productDF=productDF.drop(productDF.columns[0], axis=1)
productDF['factors'] = productDF['Which of these factors are important to you when deciding which car to purchase?'].str.split(";", n = -1, expand = False)
productDF['external'] = productDF['Which of the following exterior components would you choose to customise (texture, layout, size, etc)? '].str.split(";", n = -1, expand = False)
productDF['internal'] = productDF['Which of the following interior components would you choose to customise (texture, layout, size, etc)? '].str.split(";", n = -1, expand = False)

#length of how many customisations of car
productDF['fact_length'] = productDF['factors'].str.len()
productDF['ext_length'] = productDF['external'].str.len()
productDF['int_length'] = productDF['internal'].str.len()

#Saving dataframe into excel file to analyse on R
productDF.to_excel('stringed_survey.xlsx', index=False)

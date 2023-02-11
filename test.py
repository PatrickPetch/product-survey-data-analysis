# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 10:48:44 2023

@author: atan1
"""

import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
sb.set()

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from sklearn.preprocessing import LabelEncoder


#Opening Tkinter GUI to open File
Tk().withdraw()
print('Look for open window to open saved file')
filename = askopenfilename(title = 'Open File')
print(filename)
productDF = pd.read_excel(filename)

print("product shape: ",productDF.shape)
print(productDF.head())

#sb.heatmap(productDF.isnull(),yticklabels=False,cbar=False,cmap='Blues')

# Renaming dataframe columns
productDF.columns = ["No.", "Age", "Gender", "Category", "MarriageStatus", "FactorsPurchase", \
                     "FreeCustomization", "ExteriorComponents", "InteriorComponents", \
                     "WTSCustomization", "WantOwnPersonalization", "WTSPersonalization", "PersonalizationJob"]

#Creating dataframes for each header
productDF=productDF.drop(productDF.columns[0], axis=1)
productDF['factors'] = productDF['FactorsPurchase'].str.split(";", n = -1, expand = False)
productDF['external'] = productDF['ExteriorComponents'].str.split(";", n = -1, expand = False)
productDF['internal'] = productDF['InteriorComponents'].str.split(";", n = -1, expand = False)

#length of how many customisations of car
productDF['fact_length'] = productDF['factors'].str.len()
productDF['ext_length'] = productDF['external'].str.len()
productDF['int_length'] = productDF['internal'].str.len()

productDF['WTSCustomization']= productDF['WTSCustomization'].astype(str)
productDF['WTSPersonalization']= productDF['WTSPersonalization'].astype(str)

# Encoding categorical ordinal data
productDF['Age_label_encoded']=LabelEncoder().fit_transform(productDF.Age)
productDF['Gender_label_encoded']=LabelEncoder().fit_transform(productDF.Gender)
productDF['Category_label_encoded']=LabelEncoder().fit_transform(productDF.Category)
productDF['MarriageStatus_label_encoded']=LabelEncoder().fit_transform(productDF.MarriageStatus)
productDF['FreeCustomization_label_encoded']=LabelEncoder().fit_transform(productDF.FreeCustomization)
productDF['WTSCustomization_label_encoded']=LabelEncoder().fit_transform(productDF.WTSCustomization)
productDF['WantOwnPersonalization_label_encoded']=LabelEncoder().fit_transform(productDF.WantOwnPersonalization)
productDF['WTSPersonalization_label_encoded']=LabelEncoder().fit_transform(productDF.WTSPersonalization)
productDF['PersonalizationJob_label_encoded']=LabelEncoder().fit_transform(productDF.PersonalizationJob)


rangeDF = productDF[["Age", "Gender", "Category", "MarriageStatus","FreeCustomization","WTSCustomization",\
                     "WantOwnPersonalization","WTSPersonalization","PersonalizationJob"]]
encodeDF = productDF[['Age_label_encoded','Gender_label_encoded','Category_label_encoded','MarriageStatus_label_encoded',\
                      'FreeCustomization_label_encoded','WTSCustomization_label_encoded','WantOwnPersonalization_label_encoded',\
                          'WTSPersonalization_label_encoded','PersonalizationJob_label_encoded','fact_length','ext_length','int_length']]

plt.figure(figsize=(12,8))
sb.stripplot(x='MarriageStatus', y='Age', data=rangeDF, jitter=True, hue='Category', dodge=True, palette='viridis')

plt.figure(figsize=(12,8))
sb.stripplot(x='Gender', y='Age', data=rangeDF, jitter=True, hue='FreeCustomization', dodge=True, palette='viridis')


#checking number of customisations affected by age and car ownership
plt.figure(figsize=(12,8))
sb.stripplot(x='Category', y='fact_length', data=productDF, jitter=True, hue='Age', dodge=True, palette='viridis')
plt.figure(figsize=(12,8))
sb.stripplot(x='Category', y='ext_length', data=productDF, jitter=True, hue='Age', dodge=True, palette='viridis')
plt.figure(figsize=(12,8))
sb.stripplot(x='Category', y='int_length', data=productDF, jitter=True, hue='Age', dodge=True, palette='viridis')

# checking number of customisations affected by gender and car ownership
plt.figure(figsize=(12,8))
sb.stripplot(x='Category', y='fact_length', data=productDF, jitter=True, hue='Gender', dodge=True, palette='viridis')
plt.figure(figsize=(12,8))
sb.stripplot(x='Category', y='ext_length', data=productDF, jitter=True, hue='Gender', dodge=True, palette='viridis')
plt.figure(figsize=(12,8))
sb.stripplot(x='Category', y='int_length', data=productDF, jitter=True, hue='Gender', dodge=True, palette='viridis')

# 
plt.figure(figsize=(12,8))
sb.stripplot(x='Category', y='fact_length', data=productDF, jitter=True, hue='MarriageStatus', dodge=True, palette='viridis')
plt.figure(figsize=(12,8))
sb.stripplot(x='Category', y='ext_length', data=productDF, jitter=True, hue='MarriageStatus', dodge=True, palette='viridis')
plt.figure(figsize=(12,8))
sb.stripplot(x='Category', y='int_length', data=productDF, jitter=True, hue='MarriageStatus', dodge=True, palette='viridis')

#checking relationship between willingness to customize, price customer willing to pay and number of customizations
plt.figure(figsize=(12,8))
sb.stripplot(x='FreeCustomization', y='int_length', data=productDF, jitter=True, hue='WTSCustomization', dodge=True, palette='viridis')
plt.figure(figsize=(12,8))
sb.stripplot(x='FreeCustomization', y='ext_length', data=productDF, jitter=True, hue='WTSCustomization', dodge=True, palette='viridis')
plt.figure(figsize=(12,8))
sb.stripplot(x='FreeCustomization', y='MarriageStatus', data=productDF, jitter=True, hue='WTSCustomization', dodge=True, palette='viridis')

# Identifying number of unique factors, external and internal customizations from data
def to_1D(series):
  return pd.Series([x for _list in series for x in _list])

productDF["factors"].replace(np.NaN,"",inplace=True)

unique_fac = to_1D(productDF["factors"]).value_counts()
unique_fac = pd.DataFrame({'Factor':unique_fac.index, 'Count':unique_fac.values})
unique_factors = to_1D(productDF["factors"]).value_counts().index.tolist()
unqiue_factor_count = to_1D(productDF["factors"]).value_counts().values

## Create plot for factors
fig, ax = plt.subplots(figsize = (14,4))
ax.bar(unique_factors, unqiue_factor_count)
ax.set_ylabel("Frequency", size = 12)
ax.set_title("Top factors", size = 14)
plt.savefig("bar_viz.jpg", dpi = 100)

#=================================

productDF["external"].replace(np.NaN,"",inplace=True)

unique_ext = to_1D(productDF["external"]).value_counts()
unique_ext = pd.DataFrame({'External':unique_ext.index, 'Count':unique_ext.values})
unique_externals = to_1D(productDF["external"]).value_counts().index.tolist()
unqiue_external_count = to_1D(productDF["external"]).value_counts().values

## Create plot for externals
fig, ax = plt.subplots(figsize = (14,4))
ax.bar(unique_externals, unqiue_external_count)
ax.set_ylabel("Frequency", size = 12)
ax.set_title("Top externals", size = 14)
plt.savefig("bar_viz.jpg", dpi = 100)

#=================================

productDF["internal"].replace(np.NaN,"",inplace=True)

unique_int = to_1D(productDF["internal"]).value_counts()
unique_int = pd.DataFrame({'Internal':unique_int.index, 'Count':unique_int.values})
unique_internals = to_1D(productDF["internal"]).value_counts().index.tolist()
unqiue_internal_count = to_1D(productDF["internal"]).value_counts().values

## Create plot for internals
fig, ax = plt.subplots(figsize = (14,4))
ax.bar(unique_internals, unqiue_internal_count)
ax.set_ylabel("Frequency", size = 12)
ax.set_title("Top internals", size = 14)
plt.savefig("bar_viz.jpg", dpi = 100)


#Saving DFs as xlsx
productDF.to_excel('stringed_survey.xlsx', index=False)
rangeDF.to_excel('range_survey.xlsx', index=False)
encodeDF.to_excel('encoded_data.xlsx', index=False)

with pd.ExcelWriter('factors.xlsx') as writer:
    unique_fac.to_excel(writer, sheet_name="Factors", index=False)
    unique_int.to_excel(writer, sheet_name="Internal Cust", index=False)
    unique_ext.to_excel(writer, sheet_name="External Cust", index=False)
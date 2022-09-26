# -*- coding: utf-8 -*-
"""Assignment-2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jzof9VkugiHv0xQz3f8TW5YsXMp5haIn

# 1. Dataset is downloaded

# 2. Load the Dataset
"""

import pandas as pd

df = pd.read_csv("Churn_Modelling.csv")

df

"""# 3. Perform Below Visualizations.

## Univariate Analysis
"""

import matplotlib.pyplot as plt

plt.hist(df['CreditScore'], edgecolor = 'black')
plt.title("Credit Score")

"""## Bi - Variate Analysis"""

plt.scatter(df.CreditScore, df.Age)
plt.title("CreditScore vs Age")
plt.xlabel('Credit Score')
plt.ylabel('Age')

"""## Multi - Variate Analysis

"""

import seaborn as sns

sns.barplot(x='Gender',
    y='Age',
    data = df,
    palette = 'bright',
    hue = 'Geography');

"""# 4. Perform descriptive statistics on the dataset.

"""

import numpy as np

df.describe(include=['object'])

df.describe(include=['number'])

"""# 5. Handle the Missing values."""

df.isnull()

df.isnull().sum()

"""# 6.  Find the outliers and replace the outliers

## Finding Outliers
"""

df1 = df.copy()
df1.drop(columns=['RowNumber','CustomerId','Surname','Geography','Gender','Tenure','NumOfProducts','HasCrCard',
                  'IsActiveMember', 'Balance', 'EstimatedSalary', 'Exited'])

Q1,Q3 = np.percentile(df1.CreditScore, [25,75])
IQR = Q3 - Q1
upperlimit = Q3 + 1.5 * IQR
lowerlimit = Q1 - 1.5 * IQR
outliers = df1.CreditScore[(df1.CreditScore > upperlimit) | (df1.CreditScore < lowerlimit)]
np.array(outliers)

"""## Replacing Outliers with median"""

median = np.percentile(df1.CreditScore, 50) # median = 652
df1['CreditScore'] = np.where(df1.CreditScore < lowerlimit, 652 , df1['CreditScore'])
df1.describe()

"""# 7.  Check for Categorical columns and perform encoding."""

gender = pd.get_dummies(df1.Gender, drop_first = False)

gender

df1 = pd.concat([df1, gender], axis=1)
df1.drop('Gender', axis = 1, inplace = True)
df1.head()

"""# 8. Split the data into dependent and independent variables.

"""

df1.drop('Geography', axis = 1, inplace = True)

# x - Independent , y - Dependent

x = df1.drop('Exited', axis = 1)

y = df1['Exited']

x.head()

y.head()

"""# 9. Scale the independent variables

"""

from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
x = ss.fit_transform(x)
x

"""# 10. Split the data into training and testing"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split( x, y, test_size = 0.2, random_state = 0 )

x_train.shape

x_test.shape

y_train.shape

y_test.shape
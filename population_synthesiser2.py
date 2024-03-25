

import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Reading the data and making a dataframe of it
source_data = pd.read_csv("D:\Data Science\Pandas\Data_cistup.csv")
df = pd.DataFrame(source_data)


# frequency of each category
age_counts = df[('Age_category')].value_counts()
education_counts = df['Highest_education_level'].value_counts()
sex_counts = df['Sex'].value_counts()

# frequency of each category in the data
total_samples = len(df)
age_proportions = age_counts / total_samples
education_proportions = education_counts / total_samples
sex_proportions = sex_counts / total_samples

age_frequencies = age_proportions.to_dict()
sex_frequencies = sex_proportions.to_dict()
education_frequencies = education_proportions.to_dict()

age_categories = np.array(list(age_frequencies.keys()))
age_probabilities = np.array(list(age_frequencies.values()))
age_counts_population = np.random.multinomial(4800, age_probabilities)

#we will concatenate new dataframe to input data , for that we need to make new population of 4800 individuals.
sex_categories = np.array(list(sex_frequencies.keys()))
sex_probabilities = np.array(list(sex_frequencies.values()))
sex_counts_population = np.random.multinomial(4800, sex_probabilities).tolist()

#calculating the number of males and females in new population
male_count = sex_counts_population[0]
female_count = sex_counts_population[1]

education_categories = np.array(list(education_frequencies.keys()))
education_probabilities = np.array(list(education_frequencies.values()))
education_counts_population = list(np.random.multinomial(4800, education_probabilities))


#for the source/input data the below 3 lines will show distribution in form of a pandas series. using this we can know the distribution of each category in our data
education_sex_age_freq = source_data.groupby(['Sex', 'Age_category', 'Highest_education_level']).size()
education_sex_age_freq = education_sex_age_freq / total_samples
education_sex_age_freq = education_sex_age_freq.groupby(level=[0]).apply(lambda x: x / x.sum())



""" Please note that i have taken the frequency distribution according to sex category. then the output of print(education_sex_age_freq) will have the sum of freq for sex ==1 as 1 and same for sex ==2"""

# Multiplying the frequency with their population size in distribution
education_sex_age_freq[education_sex_age_freq.index.get_level_values('Sex') == 1] *= male_count
education_sex_age_freq[education_sex_age_freq.index.get_level_values('Sex') == 2] *= female_count

# Rounding the entries to int values and making new_df ( dataframe ) using it
education_sex_age_freq = education_sex_age_freq.astype(int).to_dict()
new_df = pd.DataFrame(columns=['Sex', 'Age_category', 'Highest_education_level'])

#filling new_df
for i in education_sex_age_freq:
    for j in range(education_sex_age_freq[i]):
        new_df = new_df.append({'Sex': i[0], 'Age_category': i[1], 'Highest_education_level': i[2]}, ignore_index=True)
new_df = new_df.sample(frac=1).reset_index(drop=True)

#When we rounded the values, it affected the entries and hence the number of rows(individuals) is not exactly 4800, so we find the difference.
actual_length=len(new_df)
addition_required=4800-actual_length


#if the difference is greater than 0 (len(new_df)<4800), then we add some random rows from the dataframe into the dataframe to make the len(new_df)==4800.
#if the difference is negative, then we drop some number of random rows from dataframe to make the len(new_df)==4800.
if addition_required>0:
    for i in range(addition_required):
        new_df=new_df.append(new_df.iloc[random.randint(0,actual_length-1)],ignore_index=True)
elif addition_required<0:
    for i in range(addition_required):
        new_df = new_df.drop(random.sample(range(actual_length), abs(addition_required)))


# frequency of each category
age_counts_new = new_df[('Age_category')].value_counts()
education_counts_new = new_df['Highest_education_level'].value_counts()
sex_counts_new = new_df['Sex'].value_counts()
# frequency
total_samples_new = len(new_df)
age_proportions_new = age_counts_new / total_samples_new
education_proportions_new = education_counts_new / total_samples_new
sex_proportions_new = sex_counts_new / total_samples_new

# print(age_proportions_new,sex_proportions_new,education_proportions_new)
# print(new_df)


"""Now we will anaylse how similar the input data is to this new data we have synthesised."""


# frequency of each category
age_counts_new = new_df[('Age_category')].value_counts()
education_counts_new = new_df['Highest_education_level'].value_counts()
sex_counts_new = new_df['Sex'].value_counts()

#frequency
total_samples_new = len(new_df)
age_proportions_new = age_counts_new / total_samples_new
education_proportions_new = education_counts_new / total_samples_new
sex_proportions_new = sex_counts_new / total_samples_new

#these 2 lines will show the frequency of source_data and new_df.
# print(age_proportions,sex_proportions,education_proportions)
# print(age_proportions_new,sex_proportions_new,education_proportions_new)
#Outputs are
# for source data:
#     2 - 0.590
#     1 - 0.355
#     3 - 0.055
#     Name: Age_category, dtype: float64
#     1 - 0.515
#     2 - 0.485
#     Name: Sex, dtype: float64
#     2 - 0.49
#     3 - 0.22
#     0 - 0.16
#     1 - 0.13
#     Name: Highest_education_level, dtype: float64

# for new data:
#     2 - 0.590417
#     1 - 0.355000
#     3 - 0.054583
#     Name: Age_category, dtype: float64
#     1 - 0.517083
#     2 - 0.482917
#     Name: Sex, dtype: float64
#     2 - 0.490208
#     3 - 0.220208
#     0 - 0.159583
#     1 - 0.130000
#     Name: Highest_education_level, dtype: float64

#finally we concatenate both the dataframes into new_df

# new_df = new_df.append(df, ignore_index=True)
# print(new_df)

#Now we will give the output table
new_df['Sex'] = new_df['Sex'].replace({1: 'male', 2: 'female'})
new_df['Age_category'] = new_df['Age_category'].replace({1: 'below 22', 2: '22 to 66', 3: 'above 66'})
new_df['Highest_education_level'] = new_df['Highest_education_level'].replace({0: 'No formal education',
                                                                               1: 'primary education',
                                                                               2: 'secondary education',
                                                                               3: 'graduation or above'})

final = new_df.groupby(['Sex', 'Age_category', 'Highest_education_level']).size()
print(type(final))
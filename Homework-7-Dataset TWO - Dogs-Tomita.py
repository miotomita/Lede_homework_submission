#!/usr/bin/env python
# coding: utf-8

# # Homework 7, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


#df = pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx')


# In[3]:


df = pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx', nrows=30000)


# In[4]:


df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.
# 
# * *Tip: there's an option with `.read_csv` to only read in a certain number of rows*

# In[5]:


#number of raws in the data
df.shape[0]


# In[6]:


#data types of each columns
df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# ----
# <font color="blue"><b>**my answer**</b>:</font><br>
# Each row is a registered pet in New York City.<br><br>
# `Owner Zip Code` is a zip code of the owner's address.<br>
# `Vaccinated` is whether the pet is vaccinated or not. Shown as <YES/NO><br>
# ----

# In[7]:


#check column names
df.columns


# In[8]:


#check data in Vaccinated column
df.Vaccinated.unique()


# In[9]:


#check data in Owner Zip Code
df['Owner Zip Code'].unique()


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# ---
# <font color="blue">**my questions**:</font><br>
# <li>What percentage of the pets are vaccinated?</li>
# <li>What percentage of the pets are guard or trained?</li>
# <li>What percentage of the pets are spayed or neut?</li>
# <li>What are the popular breeds?</li>
# <li>Is license issued without delay for all the owners?</li>
# <li>If there are pets with shorter duration of licence, why is it? Are there any difference by vaccination status or training status etc?</li><br>
# 
# ---

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[16]:


#top 10 breed
df['Primary Breed'].value_counts().head(10)


# In[20]:


#replace 'Unknown'
df['Primary Breed'] = df['Primary Breed'].replace('Unknown', np.nan)


# In[21]:


#top 10 breed excluding unknown
df['Primary Breed'].value_counts().head(10)


# In[22]:


#top 10 graph
df['Primary Breed'].value_counts().head(10).sort_values().plot(kind='barh')
plt.title('The most popular primary breeds of dogs')
plt.show()


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown
# 
# * *Tip: Maybe you want to go back to your `.read_csv` and use `na_values=`? Maybe not? Up to you!*

# In[23]:


#I have done it with 3.1


# ## What are the most popular dog names?

# In[26]:


#popular names
df['Animal Name'].value_counts().head(10)


# In[27]:


#replace names "Unknown" with np.nan
df.loc[df['Animal Name'].str.contains('unknown', case=False, na=False),'Animal Name'] =np.nan


# In[28]:


#popular names excluding unknown
df['Animal Name'].value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[30]:


#cleaning data
#strip
df['Animal Name'] = df['Animal Name'].apply(lambda x: str(x).strip())
df['Animal Name'] = df['Animal Name'].replace('nan', np.nan)


# In[86]:


#all the max names
names = df.loc[df['Animal Name'].str.contains('Max', case=False, na=False),'Animal Name'].unique()
numbers = df[df['Animal Name'].str.contains('Max', case=False, na=False)].shape[0]

print(f"There are {numbers} dogs with Max names.\n")
print('Names:\n', ', '.join(names))


# In[85]:


#Only"Max (with either upper/lowercase)"
names = df[df['Animal Name'].str.contains('^Max$', case=False, na=False, regex=True)]['Animal Name'].unique()
numbers = df[df['Animal Name'].str.contains('^Max$', case=False, na=False, regex=True)].shape[0]

print(f"Among them, {numbers} dogs are registered as 'Max'.\n")
print('Names:\n', ', '.join(names))


# In[79]:


#all the Maxwell names
names = df[df['Animal Name'].str.contains('Maxwell', case=False, na=False, regex=True)]['Animal Name'].unique()
numbers = df[df['Animal Name'].str.contains('Maxwell', case=False, na=False, regex=True)].shape[0]

print(f'{numbers} dogs are named "Maxwell".\n')
print('Names:\n', ', '.join(names))


# In[84]:


#Only "Maxwell(with either upper/lowercase)"
names = df[df['Animal Name'].str.contains('^Maxwell$', case=False, na=False, regex=True)]['Animal Name'].unique()
numbers = df[df['Animal Name'].str.contains('^Maxwell$', case=False, na=False, regex=True)].shape[0]

print(f"Among them, {numbers} dogs are registered as 'Maxwell'.\n")
print('Names:\n', ', '.join(names))


# ## What percentage of dogs are guard dogs?

# In[88]:


#check data
df['Guard or Trained'].unique()


# In[91]:


# percentage excluding na values
df['Guard or Trained'].value_counts(normalize=True) *100


# In[92]:


# percentage including na values
df['Guard or Trained'].value_counts(dropna=False, normalize=True) *100


# ## What are the actual numbers?

# In[93]:


df['Guard or Trained'].value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`. Think about missing data!

# In[100]:


# if you add that up, is it the same as your number of rows?
#add numbers up
#It's NOT the same as the number of all the rows (30000)
df['Guard or Trained'].value_counts().sum()


# In[112]:


#Where are the other dogs????
print(f"{len(df) - df['Guard or Trained'].value_counts().sum()} are missing because they have 'na' values for 'Guard ot Trained' column.")


# In[113]:


#How can we find them??????
#by filtering na data
df[df['Guard or Trained'].isna()].head()


# ## Maybe fill in all of those empty "Guard or Trained" columns with "No"? Or as `NaN`? 
# 
# Can we make an assumption either way? Then check your result with another `.value_counts()`

# In[117]:


#Yes/No + counting NaN 
df['Guard or Trained'].value_counts(dropna=False, normalize=True) * 100


# In[120]:


#counting NaN as "No"
df['Guard or Trained'].fillna('No').value_counts(normalize=True) * 100


# ## What are the top dog breeds for guard dogs? 

# In[122]:


#the top dog breeds for guard dogs
df.loc[df['Guard or Trained']=='Yes','Primary Breed'].value_counts().head(5)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[123]:


#take out year and assign it as a new column
df['year'] = df['Animal Birth'].apply(lambda birth: birth.year)


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[124]:


#calculate age and assign it as a new column
df['age'] = 2022 - df.year


# In[128]:


#average age of dogs
print(f"Dogs are {df.age.mean():.1f} years old on average.")


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[130]:


#read zipcode data
zipcode = pd.read_csv('zipcodes-neighborhoods.csv')


# In[132]:


#check data
zipcode.head()


# In[134]:


#check data types
zipcode.dtypes


# In[135]:


#check data in borough column
zipcode.borough.unique()


# In[136]:


#check data in neighborhood column
zipcode.neighborhood.unique()


# In[137]:


#merge data
df = df.merge(zipcode, left_on='Owner Zip Code', right_on='zip')


# In[139]:


#check merged data
df.head()


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?
# 
# You'll want to do these separately, and filter for each.

# In[140]:


#What is the most popular dog name in all parts of the Bronx?
df[df.borough=='Bronx']['Animal Name'].value_counts().head()


# In[141]:


#How about Brooklyn? 
df[df.borough=='Brooklyn']['Animal Name'].value_counts().head()


# In[142]:


#The Upper East Side?
df[df.neighborhood=='Upper East Side']['Animal Name'].value_counts().head()


# ## What is the most common dog breed in each of the neighborhoods of NYC?
# 
# * *Tip: There are a few ways to do this, and some are awful (see the "top 5 breeds in each borough" question below).*

# In[166]:


#counting numbers of dogs of each breed in each neighborhoods
breed_count = df.groupby(['neighborhood','Primary Breed']).count().borough.unstack()


# In[167]:


#rank by number
breed_rank = breed_count.rank(method="min",ascending=False, axis=1)


# In[186]:


#top5 table
breed_top5 = breed_rank.where(breed_rank<=5)
breed_top5 = breed_top5.dropna(how="all").dropna(how="all",axis=1)


# In[197]:


#show table
breed_top5[breed_top5.mean().sort_values().index].fillna('')


# In[223]:


#print
for neighborhood in breed_top5.index:
    breeds = breed_top5.loc[neighborhood]
    breeds = breeds.dropna().sort_values().to_dict()
    text = ','.join(['(' + str(int(val))+')' + key for key, val in breeds.items()])
    print(neighborhood, ':\n', text, '\n----')


# ## What breed of dogs are the least likely to be spayed? Male or female?
# 
# * *Tip: This has a handful of interpretations, and some are easier than others. Feel free to skip it if you can't figure it out to your satisfaction.*

# In[224]:


#check how data looks like
df['Spayed or Neut'].unique()


# In[229]:


#change <Yes/No> to <True/False> to calculate numbers in the following cells
df['spayed_or_neut'] = df['Spayed or Neut'].replace({'Yes': True, 'No': False})


# In[230]:


#What breed of dogs are the least likely to be spayed?
#breeds with low numbers
df.groupby(['Primary Breed'])['spayed_or_neut'].mean().sort_values().head(15)


# In[234]:


#Male or female?
#by gender
#Male dogs are least likely to be spayed
df.groupby(['Animal Gender']).mean().spayed_or_neut.sort_values()


# In[233]:


#by gender AND breed
df.groupby(['Primary Breed','Animal Gender']).mean().spayed_or_neut.sort_values().head(25)


# ## Make a new column called `monochrome` that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[236]:


#list of columns with color names
color_cols = [col for col in df.columns if 'Color' in col]
print(color_cols)


# In[239]:


#names of all the colors
colors = set(df['Animal Dominant Color'])|set(df['Animal Secondary Color'])|set(df['Animal Third Color'])
print(colors)


# In[265]:


#names of monochrome colors
#add na
mono_colors = [color for color in colors if any(mono in str(color).lower() for mono in ['black','white','gray'])]
mono_colors = mono_colors + [np.nan]
print(mono_colors)


# In[301]:


#filter rows with only monochrome colors & na
df['monochrome'] = (df[color_cols].isin(mono_colors).sum(axis=1)==3)


# In[310]:


#change momochrome column to False for rows without color data
df.loc[df[color_cols].isna().sum(axis=1)==3,'monochrome'] = False


# In[311]:


#How many animals are monochrome
print(f"{df.monochrome.sum()} are monochrome.")


# ## How many dogs are in each borough? Plot it in a graph.

# In[313]:


#How many dogs are in each borough?
df.borough.value_counts()


# In[314]:


#graph
df.borough.value_counts().sort_values().plot(kind="barh")
plt.title("The number of dogs in each borough")
plt.show()


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[323]:


#population data
boro_population = pd.read_csv('boro_population.csv')
boro_population = boro_population.set_index('borough')


# In[324]:


#add dog counts
boro_population['dogs'] = df.borough.value_counts()


# In[330]:


#calculate per capita dogs
boro_population['per_capita_dogs'] = boro_population.dogs / boro_population.population


# In[349]:


#sort values
boro_population = boro_population.sort_values(by='per_capita_dogs', ascending=False)


# In[350]:


boro_population


# In[353]:


print(f"{boro_population.index[0]} is borough with the highest number of dogs per-capita.")


# In[339]:


#check with the whole data set
#Manhattan is still the borough with the highest number
df_all = pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx')
df_all = df_all.merge(zipcode, left_on='Owner Zip Code', right_on='zip')
(df_all.borough.value_counts() / boro_population.population).sort_values(ascending= False)


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[357]:


df['dogs_count'] = 1


# In[362]:


#count number of dogs of each breed for each borough
borough_df = df.groupby(['borough','Primary Breed']).sum()[['dogs_count']]


# In[365]:


#rank
borough_df['dogs_rank'] = borough_df.groupby(level=0).dogs_count.rank(ascending=False, method="min")


# In[366]:


#top5 table
borough_df[borough_df.dogs_rank<=5]


# In[368]:


#data
#top5 breeds of each boroughs 
source = borough_df[borough_df.dogs_rank<=5]

fig = plt.figure(figsize=(10,5))
fig.suptitle('The top 5 dog breeds in the boroughs of NYC', fontsize=16)

xlim = source.dogs_count.max() +10

i = 1
for borough in df.borough.unique():
    ax = fig.add_subplot(3, 2, i)
    ax = source.loc[borough,'dogs_count'].rename_axis('').sort_values().plot(kind="barh")
    ax.set_xlim(0, xlim)
    ax.set_title(f"{borough}")
    i+=1

fig.tight_layout()
plt.show()


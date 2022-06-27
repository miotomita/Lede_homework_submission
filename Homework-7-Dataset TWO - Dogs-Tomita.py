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


df = pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx', nrows=30000, dtype={'Owner Zip Code':str})


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


# In[7]:


#modify column names
df.columns = df.columns.str.lower().str.replace(' ','_')


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# ----
# <font color="blue"><b>**my answer**</b>:</font><br>
# Each row is a registered pet in New York City.<br><br>
# `Owner Zip Code` is a zip code of the owner's address.<br>
# `Vaccinated` is whether the pet is vaccinated or not. Shown as <YES/NO><br>
# ----

# In[8]:


#check column names
df.columns


# In[9]:


#check data in Vaccinated column
df.vaccinated.unique()


# In[10]:


#check data in Owner Zip Code
df['owner_zip_code'].unique()


# In[11]:


#add '0' if zip code is only 4 digits
df.owner_zip_code = df.owner_zip_code.apply(lambda x: '0'+ str(x) if len(x)==4 else x)


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

# In[12]:


#top 10 breed
df.primary_breed.value_counts().head(10)


# In[13]:


#replace 'Unknown'
df.primary_breed = df.primary_breed.replace('Unknown', np.nan)


# In[14]:


#top 10 breed excluding unknown
df.primary_breed.value_counts().head(10)


# In[15]:


#top 10 graph
df.primary_breed.value_counts().head(10).sort_values().plot(kind='barh')
plt.title('The most popular primary breeds of dogs')
plt.show()


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown
# 
# * *Tip: Maybe you want to go back to your `.read_csv` and use `na_values=`? Maybe not? Up to you!*

# In[16]:


#I have done it with 3.1


# ## What are the most popular dog names?

# In[17]:


#popular names
df.animal_name.value_counts().head(10)


# In[18]:


#replace names "Unknown" with np.nan
df.loc[df.animal_name.str.contains('unknown',case=False, na=False),'animal_name'] = np.nan


# In[19]:


#popular names excluding unknown
df.animal_name.value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[20]:


# Do any dogs have your name?----> No
df[df.animal_name.str.contains('mio', case=False, na=False)]


# In[21]:


#cleaning data
#strip
df.animal_name = df.animal_name.str.strip()


# In[22]:


#How many dogs are named "Max?
#check Max names
df[df.animal_name.str.contains('Max', case=False, na=False)].animal_name.unique()


# In[23]:


#How many dogs are named "Max"
#count dogs with all names with "max" in it
df.animal_name.str.contains('Max', case=False, na=False).sum()


# In[24]:


#Only "Max (with either upper/lowercase)"
df.animal_name.str.contains('^max$', case=False, na=False).sum()


# In[25]:


#all the Maxwell names
df.animal_name.str.contains('maxwell', case=False, na=False).sum()


# In[26]:


#Only "Maxwell(with either upper/lowercase)"
df.animal_name.str.contains('^maxwell$', case=False, na=False).sum()


# ## What percentage of dogs are guard dogs?

# In[27]:


#check data
df.guard_or_trained.unique()


# In[28]:


#percentage of guard dogs/non-guard dogs
df.guard_or_trained.value_counts(normalize=True)


# In[29]:


percentage = df.guard_or_trained.value_counts(normalize=True)['Yes'] *100
print(f"{percentage:.2f}% of dogs with training data are guard dogs.")


# In[30]:


# percentage including na values
df.guard_or_trained.value_counts(dropna=False, normalize=True) *100


# In[31]:


percentage = df.guard_or_trained.value_counts(normalize=True, dropna=False)['Yes'] *100
print(f"{percentage:.2f}% of all dogs are guard dogs.")


# ## What are the actual numbers?

# In[32]:


df.guard_or_trained.value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`. Think about missing data!

# In[33]:


# if you add that up, is it the same as your number of rows?
#add numbers up
#It's NOT the same as the number of all the rows (30000)
df.guard_or_trained.value_counts().sum()


# In[34]:


#Where are the other dogs????
#How can we find them??????
#---->by filtering na data
df[df.guard_or_trained.isna()].head()


# ## Maybe fill in all of those empty "Guard or Trained" columns with "No"? Or as `NaN`? 
# 
# Can we make an assumption either way? Then check your result with another `.value_counts()`

# In[35]:


#counting NaN as "No"
df.guard_or_trained.fillna('No').value_counts(normalize=True)


# ## What are the top dog breeds for guard dogs? 

# In[36]:


#the top dog breeds for guard dogs
df.query("guard_or_trained=='Yes'").primary_breed.value_counts().head(5)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[37]:


df['year'] = df.animal_birth.dt.year


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[38]:


#calculate age and assign it as a new column
df['age'] = 2022 - df.year


# In[39]:


#average age of dogs
print(f"Dogs are {df.age.median():.1f} years old on average.")


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[40]:


#read zipcode data
zipcode = pd.read_csv('zipcodes-neighborhoods.csv', dtype=str)


# In[41]:


#check data
zipcode.head()


# In[42]:


#check data types
zipcode.dtypes


# In[43]:


zipcode.zip = zipcode.zip.apply(lambda x: '0' + x if len(x)==4 else x)


# In[44]:


#check data in borough column
zipcode.borough.unique()


# In[45]:


#check data in neighborhood column
zipcode.neighborhood.unique()


# In[46]:


#merge data
df = df.merge(zipcode, left_on='owner_zip_code', right_on='zip')


# In[47]:


#check merged data
df.head()


# In[48]:


#Which neighborhood does each dog live in?

df.neighborhood.value_counts()


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?
# 
# You'll want to do these separately, and filter for each.

# In[49]:


#What is the most popular dog name in all parts of the Bronx?
df.query("borough=='Bronx'").animal_name.value_counts().head(1)


# In[50]:


#How about Brooklyn? 
df.query("borough=='Brooklyn'").animal_name.value_counts().head(1)


# In[51]:


#The Upper East Side?
df.query("neighborhood=='Upper East Side'").animal_name.value_counts().head(1)


# ## What is the most common dog breed in each of the neighborhoods of NYC?
# 
# * *Tip: There are a few ways to do this, and some are awful (see the "top 5 breeds in each borough" question below).*

# In[52]:


breed_by_area = pd.crosstab(df.primary_breed, df.neighborhood).rank(method='min', ascending=False)


# In[53]:


for neighborhood in breed_by_area.columns:
    dog_breed = breed_by_area[breed_by_area[neighborhood]==1].index[0]
    print(neighborhood, ": ", dog_breed)


# ## What breed of dogs are the least likely to be spayed? Male or female?
# 
# * *Tip: This has a handful of interpretations, and some are easier than others. Feel free to skip it if you can't figure it out to your satisfaction.*

# In[54]:


#check how data looks like
df.spayed_or_neut.unique()


# In[76]:


#What breed of dogs are the least likely to be spayed?
spayed_by_breed = df.groupby('primary_breed').spayed_or_neut.value_counts(normalize=True).unstack()


# In[77]:


spayed_by_breed.sort_values(by='Yes').head(5)


# In[94]:


#Male or Female?
spayed_by_gender = pd.crosstab(df.animal_gender, df.spayed_or_neut)
spayed_by_gender_pct = spayed_by_gender.div(spayed_by_gender.sum(axis=1), axis=0).sort_values(by='Yes')

#-->Male dogs have lower percentage of getting spayed
spayed_by_gender_pct


# ## Make a new column called `monochrome` that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[201]:


#columns with data for colors 
color_col = df.columns[df.columns.str.contains('color')]


# In[202]:


#change color names to lower case
df[color_col] = df[color_col].applymap(lambda x: x.lower() if type(x)==str else x)


# In[203]:


#list of colors to include
monocolors = ['black','white','gray', np.nan]


# In[204]:


#assign a monochrome column
df['monochrome'] = df[color_col].isin(monocolors).sum(axis=1)==3


# In[205]:


#change momochrome column to False for rows without color data
df.loc[df[color_col].isnull().sum(axis=1)==3, 'monochrome'] = False


# In[206]:


#How many animals are monochrome
print(f"{df.monochrome.sum()} are monochrome.")


# ## How many dogs are in each borough? Plot it in a graph.

# In[207]:


#How many dogs are in each borough?
df.borough.value_counts()


# In[208]:


#graph
df.borough.value_counts().sort_values().plot(kind="barh")
plt.title("The number of dogs in each borough")
plt.show()


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[209]:


#population data
boro_population = pd.read_csv('boro_population.csv')
boro_population = boro_population.set_index('borough')


# In[210]:


#add dog counts
boro_population['dogs'] = df.borough.value_counts()


# In[211]:


#calculate per capita dogs
boro_population['per_capita_dogs'] = boro_population.dogs / boro_population.population


# In[212]:


#sort values
boro_population = boro_population.sort_values(by='per_capita_dogs', ascending=False)


# In[213]:


boro_population


# In[216]:


print(f"{boro_population.index[0]} is borough with the highest number of dogs per capita.")


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[245]:


breed_by_borough = pd.crosstab(df.primary_breed, df.borough)


# In[265]:


fig = plt.figure(figsize=(10,5))
fig.suptitle('The top 5 dog breeds in the boroughs of NYC', fontsize=16)

xlim = breed_by_borough.max().max() +10

i = 1
for borough in breed_by_borough.columns:
    source = breed_by_borough.nlargest(5, borough)[borough]

    ax = fig.add_subplot(3, 2, i)
    ax = source.rename_axis('').sort_values().plot(kind="barh")
    ax.set_xlim(0, xlim)
    ax.set_title(f"{borough}")
    i+=1

fig.tight_layout()
plt.show()


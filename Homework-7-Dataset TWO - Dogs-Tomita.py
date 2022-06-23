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


df.shape[0]


# In[6]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# <font color="blue">**my answer**:</font><br>
# Each row is a registered pet<br><br>
# `Owner Zip Code` is a zip code of the owner of the pet<br>
# `Vaccinated` is whether the pet is vaccinated or not <YES/NO><br>

# In[7]:


df.Vaccinated.unique()


# In[8]:


df.head()


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# <font color="blue">**my answer**:</font><br>
# <li>What percentage of the pets are vaccinated?</li>
# <li>What percentage of the pets are guard or trained?</li>
# <li>What percentage of the pets are spayed or neut?</li>
# <li>What are the popular breeds?</li>
# <li>Is license issued without delay for all the owners?</li>
# <li>If there are pets with shorter duration of licence, why is it? Are there any difference by vaccination status or training status etc?</li>

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[9]:


df['Primary Breed'].unique()


# In[10]:


df.loc[df['Primary Breed'].str.contains('know',na=False),'Primary Breed'].unique()


# In[11]:


df['Primary Breed'] = df['Primary Breed'].replace('Unknown', np.nan)


# In[12]:


df['Primary Breed'].value_counts().head(10)


# In[13]:


df['Primary Breed'].value_counts().head(10).sort_values().plot(kind='barh')
plt.title('The most popular primary breeds of dogs')
plt.show()


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown
# 
# * *Tip: Maybe you want to go back to your `.read_csv` and use `na_values=`? Maybe not? Up to you!*

# In[14]:


#I have done it with 3.1


# ## What are the most popular dog names?

# In[15]:


df['Animal Name'].value_counts()


# In[16]:


#replace names "Unknown" with np.nan
df.loc[df['Animal Name'].str.contains('unknown', case=False, na=False),'Animal Name'] =np.nan


# In[17]:


df['Animal Name'].value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[18]:


df['Animal Name'] = df['Animal Name'].apply(lambda x: str(x).strip())


# In[19]:


df['Animal Name'] = df['Animal Name'].replace('nan', np.nan)


# In[20]:


df.loc[df['Animal Name'].str.contains('Max', case=False, na=False),'Animal Name'].unique()


# In[21]:


#All the names that includes "max"
df[df['Animal Name'].str.contains('Max', case=False, na=False)].shape[0]


# In[22]:


#"Max"
#but there could be other Max such as 'MAX', 'max'
df[df['Animal Name']=='Max'].shape[0]


# In[23]:


#"max"
#but there could still be other Max such as'max'
df[df['Animal Name']=='max'].shape[0]


# In[24]:


#"Max","MAX", "max", etc.
df[df['Animal Name'].str.contains('^Max$', regex=True, case=False, na=False)].shape[0]


# In[25]:


#"Maxwell","MAXWELL" etc.
df[df['Animal Name'].str.contains('^Maxwell$',case=False,na=False)].shape[0]


# ## What percentage of dogs are guard dogs?

# In[26]:


df['Guard or Trained'].unique()


# In[27]:


df['Guard or Trained'].value_counts(normalize=True) *100


# In[28]:


df['Guard or Trained'].value_counts(dropna=False, normalize=True) *100


# ## What are the actual numbers?

# In[29]:


df['Guard or Trained'].value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`. Think about missing data!

# In[30]:


df['Guard or Trained'].value_counts().sum()


# ## Maybe fill in all of those empty "Guard or Trained" columns with "No"? Or as `NaN`? 
# 
# Can we make an assumption either way? Then check your result with another `.value_counts()`

# In[31]:


df['Guard or Trained'].value_counts(dropna=False, normalize=True) *100


# ## What are the top dog breeds for guard dogs? 

# In[32]:


df.loc[df['Guard or Trained']=='Yes','Primary Breed'].value_counts()


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[33]:


df['year'] = df['Animal Birth'].apply(lambda x: x.year)


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[34]:


df['age'] = 2022 - df.year


# In[35]:


#average age of dogs
df.age.mean()


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[36]:


zipcode = pd.read_csv('zipcodes-neighborhoods.csv')


# In[37]:


zipcode.head()


# In[38]:


zipcode.dtypes


# In[39]:


zipcode.borough.unique()


# In[40]:


zipcode.neighborhood.unique()


# In[41]:


df = df.merge(zipcode, left_on='Owner Zip Code', right_on='zip')


# In[42]:


df.head()


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?
# 
# You'll want to do these separately, and filter for each.

# In[43]:


df[df.borough=='Bronx']['Animal Name'].value_counts().head()


# In[44]:


df[df.borough=='Brooklyn']['Animal Name'].value_counts().head()


# In[45]:


df[df.neighborhood=='Upper East Side']['Animal Name'].value_counts().head()


# ## What is the most common dog breed in each of the neighborhoods of NYC?
# 
# * *Tip: There are a few ways to do this, and some are awful (see the "top 5 breeds in each borough" question below).*

# In[46]:


df.neighborhood.unique()


# In[72]:


#count numbers of dogs of each breed in each neighborhood
breed_by_location = df.groupby(['neighborhood','Primary Breed']).count()[['borough']]
breed_by_location = breed_by_location.rename(columns={'borough':'number_of_dogs'})


# In[73]:


#rank
breed_by_location['local_rank'] = breed_by_location.groupby(level=[0]).rank(method="min",ascending=False)


# In[77]:


#show as a table
breed_by_location = breed_by_location.local_rank.unstack()


# In[93]:


#sort & filter top5
sort_order = breed_by_location.mean().sort_values().index.to_list()
top5_breed_by_location = breed_by_location[sort_order].where(breed_by_location<=5).dropna(how="all").dropna(how="all",axis=1)


# In[94]:


top5_breed_by_location.fillna('')


# ## What breed of dogs are the least likely to be spayed? Male or female?
# 
# * *Tip: This has a handful of interpretations, and some are easier than others. Feel free to skip it if you can't figure it out to your satisfaction.*

# In[95]:


df['Spayed or Neut'].unique()


# In[96]:


df['spayed_or_neut'] = df['Spayed or Neut'].replace({'Yes': True, 'No': False})


# In[117]:


#What breed of dogs are the least likely to be spayed?
df.groupby(['Primary Breed'])['spayed_or_neut'].mean().sort_values().head(15)


# In[114]:


#Male or female?
df.groupby(['Primary Breed','Animal Gender']).mean().spayed_or_neut.sort_values().head(25)


# In[118]:


df.groupby(['Animal Gender']).mean().spayed_or_neut.sort_values()


# ## Make a new column called `monochrome` that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[223]:


#columns
color_cols = [col for col in df.columns if 'Color' in col]


# In[224]:


#check how color columns look like
df[color_cols].head()


# In[164]:


#names of colors
colors = set(df['Animal Dominant Color'])|set(df['Animal Secondary Color'])|set(df['Animal Third Color'])


# In[175]:


#names of monochrome colors
mono_colors = [color for color in colors if any(mono in str(color).lower() for mono in ['black','white','gray'])]
mono_colors


# In[245]:


#drop rows with na for all the 3 color columns
#fillna with "Black" so that it will be counted as True
color_df = df[color_cols].dropna(how="all").fillna('Black')

#filter rows only with mono_colors or na
color_df = color_df[color_df.isin(mono_colors).sum(axis=1)==3]


# In[254]:


#create new column
#"True" for rows that are monochrome
df.loc[color_df.index, 'monochrome'] = True

#"False" for rows that are not monochrome
df.monochrome = df.monochrome.fillna(False)


# In[267]:


df[df.monochrome].head(10)


# In[270]:


#How many animals are monochrome
df.monochrome.value_counts()


# ## How many dogs are in each borough? Plot it in a graph.

# In[273]:


df.borough.value_counts()


# In[278]:


df.borough.value_counts().sort_values().plot(kind="barh")
plt.title("The number of dogs in each borough")
plt.show()


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[281]:


population = pd.read_csv('boro_population.csv')
population


# In[294]:


borough_df = pd.DataFrame(df.borough.value_counts().rename('dogs'))


# In[301]:


#number of dogs per-capita
(borough_df.dogs / population.set_index('borough').population).sort_values(ascending=False)


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[306]:


df['dogs_count'] = 1


# In[345]:


borough_df


# In[343]:


#count number of dogs of each breed for each borough
borough_df = df.groupby(['borough','Primary Breed']).sum()[['dogs_count']]


# In[451]:


#rank
borough_df['dogs_rank'] = borough_df.groupby(level=0).dogs_count.rank(ascending=False, method="min")


# In[452]:


#top5 table
borough_df[borough_df.dogs_rank<=5]


# In[449]:


#data
#top5 breeds of each boroughs 
data = borough_df[borough_df.dogs_rank<=5]

fig = plt.figure(figsize=(10,5))
fig.suptitle('The top 5 dog breeds in the boroughs of NYC', fontsize=16)

xlim = data.dogs_count.max() +10

i = 1
for borough in df.borough.unique():
    ax = fig.add_subplot(3, 2, i)
    ax = data.loc[borough,'dogs_count'].rename_axis('').sort_values().plot(kind="barh")
    ax.set_xlim(0, xlim)
    ax.set_title(f"{borough}")
    i+=1

fig.tight_layout()
plt.show()


#!/usr/bin/env python
# coding: utf-8

# Name: Mio Tomita<br>
# First Submission Date: June 25, 2022<br>
# Second Submission Date: June 27, 2022

# # Homework 7, Part One: Lots and lots of questions about beer

# ### Do your importing and your setup

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")


# ## Read in the file `craftcans.csv`, and look at the first first rows

# In[12]:


#retrieve raw data
df = pd.read_csv('craftcans.csv')


# In[18]:


df.head(10)


# ## How many rows do you have in the data? What are the column types?

# In[19]:


#number of rows in the data
df.shape[0]


# In[20]:


#data types of each columns
df.dtypes


# # Checking out our alcohol

# ## What are the top 10 producers of cans of beer?

# In[21]:


#top 10 producers
df.Brewery.value_counts().head(10)


# ## What is the most common ABV? (alcohol by volume)

# In[26]:


#clean data and cast it as float
df.ABV = df.ABV.str.replace('%','').astype(float)


# In[27]:


#mean
df.ABV.mean()


# In[30]:


#median
df.ABV.median()


# In[28]:


#mode
df.ABV.mode().values[0]


# ## Oh, weird, ABV isn't a number. Convert it to a number for me, please.
# 
# It's going to take a few steps!
# 
# ### First, let's just look at the ABV column by itself

# In[31]:


#show ABV column
df.ABV


# ### Hm, `%` isn't part of  a number. Let's remove it.
# 
# When you're confident you got it right, save the results back into the `ABV` column.
# 
# - *Tip: In programming the easiest way to remove something is to *replacing it with nothing*.
# - *Tip: "nothing" might seem like `NaN` sinc we talked about it a lot in class, but in this case it isn't! It's just an empty string, like ""*
# - *Tip: `.replace` is usually used for replacing ENTIRE cells, while `.str.replace` is useful for replacing PARTS of cells*

# In[32]:


#I've done this in 2.2
#df.ABV = df.ABV.str.replace('%','')


# ### Now let's turn `ABV` into a numeric data type
# 
# Save the results back into the `ABV` column (again), and then check `df.dtypes` to make sure it worked.
# 
# - *Tip: We used `.astype(int)` during class, but this has a decimal in it...*

# In[12]:


#I've done this in 2.2
#but in case I need to remove it here:

#df.ABV = df.ABV.astype(float)


# ## What's the ABV of the average beer look like?
# 
# ### Show me in two different ways: one command to show the `median`/`mean`/etc, and secondly show me a chart

# In[33]:


# show the median/mean/etc
df.ABV.describe()


# In[34]:


#chart of ABV distribution
df.ABV.hist(ec="k")
plt.title(f"The average ABV is {df.ABV.mean():.2f}%")
plt.xlabel('ABV(%)')
plt.ylabel('number of beer')
plt.show()


# ### We don't have ABV for all of the beers, how many are we missing them from?
# 
# - *Tip: You can use `isna()` or `notna()` to see where a column is missing/not missing data.*
# - *Tip: You just want to count how many `True`s and `False`s there are.*
# - *Tip: It's a weird trick involving something we usually use to count things in a column*

# In[35]:


#the number of missing beers
df.ABV.isna().sum()


# # Looking at location
# 
# Brooklyn used to produce 80% of the country's beer! Let's see if it's still true.

# ## What are the top 10 cities in the US for canned craft beer?

# In[36]:


#top 10 cities for the canned craft beer 1
df.Location.value_counts().head(10)


# In[45]:


print(df.Location.value_counts().head(10).index.to_list())


# ## List all of the beer from Brooklyn, NY

# In[55]:


#check location names
[location for location in df.Location.unique() if "Brooklyn" in str(location)]


# In[60]:


#list for all the beers from Brooklyn, NY
df.query("Location=='Brooklyn, NY'").Beer.to_list()


# ## What brewery in Brooklyn puts out the most types of canned beer?

# In[74]:


#Brewery in Brooklyn that puts put the most beer
df.query("Location=='Brooklyn, NY'").Brewery.value_counts().head(1)


# In[85]:


#Brooklyn beers
brooklyn = df.query("Location=='Brooklyn, NY'")


# In[105]:


#number of styles each breweries in Brooklyn puts out
brooklyn.groupby('Brewery').Style.count().sort_values().plot(kind='barh')


# ## What are the five styles of beer that Sixpoint produces the most cans of?

# In[89]:


#the five styles of beer that Sixpoint produces the most cans of
df.query("Brewery=='Sixpoint Craft Ales'").Style.value_counts().head(5)


# ## List all of the breweries in New York state.
# 
# - *Tip: We want to match **part** of the `Location` column, but not all of it.*
# - *Tip: Watch out for `NaN` values! You might be close, but you'll need to pass an extra parameter to make it work without an error.*

# In[123]:


#create a new column "state"
df['state'] = df.Location.str.extract('.*,\s(.*)')


# In[128]:


#Breweries in New York state
df.query("state=='NY'").Brewery.unique()


# ### Now *count* all of the breweries in New York state

# In[130]:


#number of all breweries in New York state
df.query("state=='NY'").Brewery.nunique()


# In[131]:


#numbers of beers each breweries in New York State are producing
df.query("state=='NY'").Brewery.value_counts()


# # Measuring International Bitterness Units
# 
# ## Display all of the IPAs
# 
# Include American IPAs, Imperial IPAs, and anything else with "IPA in it."
# 
# IPA stands for [India Pale Ale](https://www.bonappetit.com/story/ipa-beer-styles), and is probably the most popular kind of beer in the US for people who are drinking [craft beer](https://www.craftbeer.com/beer/what-is-craft-beer).

# In[132]:


#Display IPAs
df[df.Style.str.contains('IPA', na=False)]


# IPAs are usually pretty hoppy and bitter (although I guess hazy IPAs and session IPAs are changing that since I first made this homework!). IBU stands for [International Bitterness Unit](http://www.thebrewenthusiast.com/ibus/), and while a lot of places like to brag about having the most bitter beer (it's an American thing!), IBUs don't necessary *mean anything*.
# 
# Let's look at how different beers have different IBU measurements.

# ## Try to get the average IBU measurement across all beers

# In[137]:


#IBU median 
pd.to_numeric(df.IBUs, errors='coerce').median()


# In[140]:


#IBU mean
pd.to_numeric(df.IBUs, errors='coerce').mean()


# ### Oh no, it doesn't work!
# 
# It looks like some of those values *aren't numbers*. There are two ways to fix this:
# 
# 1. Do the `.replace` and `np.nan` thing we did in class. Then convert the column to a number. This is boring.
# 2. When you're reading in your csv, there [is an option called `na_values`](http://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.read_csv.html). You can give it a list of **numbers or strings to count as `NaN`**. It's a lot easier than doing the `np.nan` thing, although you'll need to go add it up top and run all of your cells again.
# 
# - *Tip: Make sure you're giving `na_values` a LIST, not just a string*
# 
# ### Now try to get the average IBUs again

# In[146]:


#check what kinds of non-numeric data are mixed in
df[~df.IBUs.str.isnumeric().replace(np.nan, False)].IBUs.unique()


# In[147]:


#replace "Does not apply" manually
#cast as float
df.IBUs = df.IBUs.replace('Does not apply',np.nan).astype(float)


# In[150]:


#average IBUs
df.IBUs.mean()


# ## Draw the distribution of IBU measurements, but with *twenty* bins instead of the default of 10
# 
# - *Tip: Every time I ask for a distribution, I'm looking for a histogram*
# - *Tip: Use the `?` to get all of the options for building a histogram*

# In[151]:


#the distribution of IBU measurements
df.IBUs.hist(ec="k",bins=20)
plt.title('the distribution of IBU measurements with 20 bins')
plt.xlabel('IBUs')
plt.ylabel('number of cans')
plt.show()


# ## Hm, Interesting distribution. List all of the beers with IBUs above the 75th percentile
# 
# - *Tip: There's a single that gives you the 25/50/75th percentile*
# - *Tip: You can just manually type the number when you list those beers*

# In[152]:


#75th percentile
df.IBUs.quantile(0.75)


# In[153]:


#summary statistics
df.IBUs.describe()


# In[154]:


#all the beers with IBUs above the 75th percentile
#filter
high_ibu= df[df.IBUs>df.IBUs.quantile(0.75)]
high_ibu


# In[155]:


#show all the names of high IBU beer
high_ibu.Beer.to_list()


# ## List all of the beers with IBUs below the 25th percentile

# In[156]:


#all the beers with IBUs above the 75th percentile
filter
low_ibu = df[df.IBUs<df.IBUs.quantile(0.25)]
low_ibu


# In[157]:


#show all the names of low IBU beer
low_ibu.Beer.to_list()


# ## List the median IBUs of each type of beer. Graph it.
# 
# Put the highest at the top, and the missing ones at the bottom.
# 
# - Tip: Look at the options for `sort_values` to figure out the `NaN` thing. The `?` probably won't help you here.

# In[180]:


pd.options.display.max_rows = None


# In[181]:


#List the median IBUs of each type of beer
ibu_by_type = df.groupby('Style').IBUs.median().sort_values(na_position='first').sort_values()
ibu_by_type


# In[185]:


#graph
ibu_by_type.sort_values(na_position='first')\
    .plot(title='Median IBUs of Each Type of Beer', kind='barh', figsize=(5,20))
plt.show()


# ## Hmmmm, it looks like they are generally different styles. What are the most common 5 styles of high-IBU beer vs. low-IBU beer?
# 
# - *Tip: You'll want to think about it in three pieces - filtering to only find the specific beers beers, then finding out what the most common styles are, then getting the top 5.*
# - *Tip: You CANNOT do this in one command. It's going to be one command for the high and one for the low.*
# - *Tip: "High IBU" means higher than 75th percentile, "Low IBU" is under 25th percentile*

# In[187]:


#the most common 5 styles of high-IBU beer
high_ibu.Style.value_counts().head(5)


# In[188]:


#the most common 5 styles of low-IBU beer
low_ibu.Style.value_counts().head(5)


# ## Get the average IBU of "Witbier", "Hefeweizen" and "American Pale Wheat Ale" styles
# 
# I'm counting these as wheat beers. If you see any other wheat beer categories, feel free to include them. I want ONE measurement and ONE graph, not three separate ones. And 20 to 30 bins in the histogram, please.
# 
# - *Tip: I hope that `isin` is in your toolbox*

# In[189]:


#look up for wheaty styles
df[df.Style.str.contains('Wheat', na=False, case=False)].Style.unique()


# In[190]:


#list of wheat beers
wheaty_list = [
    'Witbier', 
    'Hefeweizen',
    'American Pale Wheat Ale',
    'American Dark Wheat Ale',
    'Wheat Ale',    
]


# In[191]:


#filtered data
wheat_beer = df[df.Style.isin(wheaty_list)]


# In[192]:


#the average IBU of wheat beers
wheat_beer.IBUs.mean()


# ## Draw a histogram of the IBUs of those beers

# In[193]:


#histogram
wheat_beer.IBUs.hist(ec="k", bins=20)
plt.title('The distribution of IBUs of wheat beers')
plt.xlabel('IBUs')
plt.ylabel('number of beer')
plt.show()


# ## Get the average IBU of any style with "IPA" in it (also draw a histogram)

# In[194]:


#filter
ipa_beer = df[df.Style.str.contains('IPA', na=False)]


# In[195]:


#average
ipa_beer.IBUs.mean()


# In[196]:


#histogram
ipa_beer.IBUs.hist(ec="k", bins=20)
plt.title('The distribution of IBUs of IPA beer')
plt.xlabel('IBUs')
plt.ylabel('number of beer')
plt.show()


# ## Plot those two histograms on top of one another
# 
# To plot two plots on top of one another, you *might* just be able to plot twice in the same cell. It depends on your version of pandas/matplotlib! If it doesn't work, you'll need do two steps.
# 
# 1. First, you make a plot using `plot` or `hist`, and you save it into a variable called `ax`.
# 2. You draw your second graph using `plot` or `hist`, and send `ax=ax` to it as a parameter.
# 
# It would look something like this:
# 
# ```python
# ax = df.plot(....)
# df.plot(ax=ax, ....)
# ``` 
# 
# And then youull get two plots on top of each other. They won't be perfect because the bins won't line up without extra work, but it's fine!

# In[197]:


#Compare IBUs distribution of wheat beers and IPAs
fig = plt.figure(figsize=(5,7))
bins = range(0,140,5)

#chart1: wheat beer
ax1 = fig.add_subplot(2, 1, 1)
ax1 = wheat_beer.IBUs.hist(ec="k", bins=bins)
ax1.set_title('The distribution of IBUs of wheat beers')

#chart2: IPAs
ax2 = fig.add_subplot(2, 1, 2, sharex=ax1, sharey=ax1)
ax2 = ipa_beer.IBUs.hist(ec="k", bins=bins)
ax2.set_title('The distribution of IBUs of IPA beer')

fig.tight_layout()


plt.show()


# ## Compare the ABV of wheat beers vs. IPAs : their IBUs were really different, but how about their alcohol percentage?
# 
# Wheat beers might include witbier, hefeweizen, American Pale Wheat Ale, and anything else you think is wheaty. IPAs probably have "IPA" in their name.

# In[198]:


#Compare ABV distribution of wheat beers and IPAs
fig = plt.figure(figsize=(5,7))

bins = np.arange(2.0, 11.0, 0.25)

#chart1: wheat beer
ax1 = fig.add_subplot(2, 1, 1)
ax1 = wheat_beer.ABV.hist(ec="k", bins=bins)
ax1.set_title('The distribution of ABV of wheat beers')

#chart2: IPAs
ax2 = fig.add_subplot(2, 1, 2, sharex=ax1, sharey=ax1)
ax2 = ipa_beer.ABV.hist(ec="k", bins=bins)
ax2.set_title('The distribution of ABV of IPA beer')


fig.tight_layout()
plt.show()


# ## Good work!
# 
# For making it this far, your reward is my recommendation for Athletic Brewing Co.'s products as the best non-alcoholic beer on the market. Their Run Wild IPA and Upside Dawn are both very solid.

# In[199]:


#check if there is any data for the non-alcoholic beer
#Either way, I'll definitly try that one!
df[df.Brewery.str.contains('Athletic', na=False)]


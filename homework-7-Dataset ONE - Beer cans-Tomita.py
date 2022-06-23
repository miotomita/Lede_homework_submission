#!/usr/bin/env python
# coding: utf-8

# # Homework 7, Part One: Lots and lots of questions about beer

# ### Do your importing and your setup

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")


# ## Read in the file `craftcans.csv`, and look at the first first rows

# In[2]:


df = pd.read_csv('craftcans.csv')


# In[3]:


df.head()


# ## How many rows do you have in the data? What are the column types?

# In[4]:


df.shape[0]


# In[5]:


df.dtypes


# # Checking out our alcohol

# ## What are the top 10 producers of cans of beer?

# In[6]:


df.Brewery.value_counts().head(10)


# ## What is the most common ABV? (alcohol by volume)

# In[7]:


#df.ABV = df.ABV.apply(lambda x: str(x).replace('%','')).astype(float)


# In[8]:


#mean
#df.ABV.mean()


# In[9]:


#mode
#df.ABV.mode()


# ## Oh, weird, ABV isn't a number. Convert it to a number for me, please.
# 
# It's going to take a few steps!
# 
# ### First, let's just look at the ABV column by itself

# In[10]:


df.ABV


# ### Hm, `%` isn't part of  a number. Let's remove it.
# 
# When you're confident you got it right, save the results back into the `ABV` column.
# 
# - *Tip: In programming the easiest way to remove something is to *replacing it with nothing*.
# - *Tip: "nothing" might seem like `NaN` sinc we talked about it a lot in class, but in this case it isn't! It's just an empty string, like ""*
# - *Tip: `.replace` is usually used for replacing ENTIRE cells, while `.str.replace` is useful for replacing PARTS of cells*

# In[11]:


df.ABV = df.ABV.str.replace('%','')


# ### Now let's turn `ABV` into a numeric data type
# 
# Save the results back into the `ABV` column (again), and then check `df.dtypes` to make sure it worked.
# 
# - *Tip: We used `.astype(int)` during class, but this has a decimal in it...*

# In[12]:


df.ABV = df.ABV.astype(float)


# ## What's the ABV of the average beer look like?
# 
# ### Show me in two different ways: one command to show the `median`/`mean`/etc, and secondly show me a chart

# In[13]:


df.ABV.mean()


# In[14]:


df.ABV.hist(ec="k")
plt.title("The average ABV is 6%")
plt.xlabel('ABV(%)')
plt.ylabel('number of beer')


# ### We don't have ABV for all of the beers, how many are we missing them from?
# 
# - *Tip: You can use `isna()` or `notna()` to see where a column is missing/not missing data.*
# - *Tip: You just want to count how many `True`s and `False`s there are.*
# - *Tip: It's a weird trick involving something we usually use to count things in a column*

# In[15]:


df.ABV.isna().sum()


# # Looking at location
# 
# Brooklyn used to produce 80% of the country's beer! Let's see if it's still true.

# ## What are the top 10 cities in the US for canned craft beer?

# In[16]:


df.Location.value_counts().head(10)


# ## List all of the beer from Brooklyn, NY

# In[17]:


[location for location in df.Location.unique() if "Brooklyn" in str(location)]


# In[18]:


df[df.Location=='Brooklyn, NY']


# ## What brewery in Brooklyn puts out the most types of canned beer?

# In[19]:


df[df.Location=='Brooklyn, NY'].Brewery.value_counts()


# ## What are the five styles of beer that Sixpoint produces the most cans of?

# In[20]:


df[df.Brewery=='Sixpoint Craft Ales'].Style.value_counts()


# In[21]:


df[df.Brewery=='Sixpoint Craft Ales'].Style.value_counts().head(5)


# ## List all of the breweries in New York state.
# 
# - *Tip: We want to match **part** of the `Location` column, but not all of it.*
# - *Tip: Watch out for `NaN` values! You might be close, but you'll need to pass an extra parameter to make it work without an error.*

# In[22]:


df['state'] = df.Location.str.replace('.*, ','', regex=True)


# In[23]:


df[df.state=='NY'].Brewery.unique()


# ### Now *count* all of the breweries in New York state

# In[24]:


df[df.state=='NY'].Brewery.value_counts()


# # Measuring International Bitterness Units
# 
# ## Display all of the IPAs
# 
# Include American IPAs, Imperial IPAs, and anything else with "IPA in it."
# 
# IPA stands for [India Pale Ale](https://www.bonappetit.com/story/ipa-beer-styles), and is probably the most popular kind of beer in the US for people who are drinking [craft beer](https://www.craftbeer.com/beer/what-is-craft-beer).

# In[25]:


df[df.Style.str.contains('IPA', na=False)]


# IPAs are usually pretty hoppy and bitter (although I guess hazy IPAs and session IPAs are changing that since I first made this homework!). IBU stands for [International Bitterness Unit](http://www.thebrewenthusiast.com/ibus/), and while a lot of places like to brag about having the most bitter beer (it's an American thing!), IBUs don't necessary *mean anything*.
# 
# Let's look at how different beers have different IBU measurements.

# ## Try to get the average IBU measurement across all beers

# In[26]:


df.IBUs.apply(lambda x: pd.to_numeric(x, errors='coerce')).mean()


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

# In[27]:


df[~df.IBUs.str.isnumeric().replace(np.nan, False)].IBUs.unique()


# In[28]:


df.IBUs = df.IBUs.replace('Does not apply',np.nan).astype(float)


# In[29]:


df.IBUs.mean()


# ## Draw the distribution of IBU measurements, but with *twenty* bins instead of the default of 10
# 
# - *Tip: Every time I ask for a distribution, I'm looking for a histogram*
# - *Tip: Use the `?` to get all of the options for building a histogram*

# In[30]:


df.IBUs.hist(ec="k")
plt.title('the distribution of IBU measurements with the default of 10 bins')
plt.xlabel('IBUs')
plt.ylabel('number of cans')
plt.show()


# In[31]:


df.IBUs.hist(ec="k",bins=20)
plt.title('the distribution of IBU measurements with 20 bins')
plt.xlabel('IBUs')
plt.ylabel('number of cans')
plt.show()


# ## Hm, Interesting distribution. List all of the beers with IBUs above the 75th percentile
# 
# - *Tip: There's a single that gives you the 25/50/75th percentile*
# - *Tip: You can just manually type the number when you list those beers*

# In[32]:


df.IBUs.describe()


# In[33]:


df.IBUs.quantile([0, 0.25, 0.5, 0.75, 1.0])


# In[34]:


df.IBUs.quantile(0.75)


# In[35]:


df[df.IBUs>=df.IBUs.quantile(0.75)]


# ## List all of the beers with IBUs below the 25th percentile

# In[36]:


df[df.IBUs<df.IBUs.quantile(0.25)]


# ## List the median IBUs of each type of beer. Graph it.
# 
# Put the highest at the top, and the missing ones at the bottom.
# 
# - Tip: Look at the options for `sort_values` to figure out the `NaN` thing. The `?` probably won't help you here.

# In[37]:


ibu_by_type = df.groupby('Style').median().IBUs.sort_values(ascending=False)


# In[38]:


ibu_by_type.dropna()


# In[39]:


ibu_by_type[ibu_by_type.isna()]


# In[40]:


ibu_by_type.dropna().sort_values().plot(kind="barh", figsize=(5,18))
plt.show()


# ## Hmmmm, it looks like they are generally different styles. What are the most common 5 styles of high-IBU beer vs. low-IBU beer?
# 
# - *Tip: You'll want to think about it in three pieces - filtering to only find the specific beers beers, then finding out what the most common styles are, then getting the top 5.*
# - *Tip: You CANNOT do this in one command. It's going to be one command for the high and one for the low.*
# - *Tip: "High IBU" means higher than 75th percentile, "Low IBU" is under 25th percentile*

# In[41]:


df[df.IBUs>df.IBUs.quantile(0.75)].Style.value_counts().head(5)


# In[42]:


df[df.IBUs<df.IBUs.quantile(0.25)].Style.value_counts().head(5)


# ## Get the average IBU of "Witbier", "Hefeweizen" and "American Pale Wheat Ale" styles
# 
# I'm counting these as wheat beers. If you see any other wheat beer categories, feel free to include them. I want ONE measurement and ONE graph, not three separate ones. And 20 to 30 bins in the histogram, please.
# 
# - *Tip: I hope that `isin` is in your toolbox*

# In[43]:


wheat_beer = df[df.Style.isin(["Witbier", "Hefeweizen","American Pale Wheat Ale"])]


# In[44]:


wheat_beer.IBUs.mean()


# ## Draw a histogram of the IBUs of those beers

# In[45]:


wheat_beer.IBUs.hist(ec="k", bins=20)
plt.title('The distribution of IBUs of wheat beers')
plt.xlabel('IBUs')
plt.ylabel('number of beer')
plt.show()


# ## Get the average IBU of any style with "IPA" in it (also draw a histogram)

# In[46]:


#filter
ipa_beer = df[df.Style.str.contains('IPA', na=False)]


# In[48]:


#average
ipa_beer.IBUs.mean()


# In[49]:


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

# In[114]:


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

# In[145]:


fig = plt.figure(figsize=(5,7))

#bins = range(2,11,1)
bins = np.arange(2.0, 11.0, 0.25)

ax1 = fig.add_subplot(2, 1, 1)
ax1 = wheat_beer.ABV.hist(ec="k", bins=bins)
ax1.set_title('The distribution of ABV of wheat beers')

ax2 = fig.add_subplot(2, 1, 2, sharex=ax1, sharey=ax1)
ax2 = ipa_beer.ABV.hist(ec="k", bins=bins)
ax2.set_title('The distribution of ABV of IPA beer')


fig.tight_layout()
plt.show()


# ## Good work!
# 
# For making it this far, your reward is my recommendation for Athletic Brewing Co.'s products as the best non-alcoholic beer on the market. Their Run Wild IPA and Upside Dawn are both very solid.

# In[149]:


df[df.Brewery.str.contains('Athletic', na=False)]


# In[ ]:


#They don't have its data in the file 
#probably because it's non-alcoholic?
#But I'll definitly try that one!


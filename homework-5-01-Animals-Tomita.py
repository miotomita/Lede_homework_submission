#!/usr/bin/env python
# coding: utf-8

# # Homework 5, Part 1: Building a pandas cheat sheet
# 
# **Use `animals.csv` to answer the following questions.** The data is small and the questions are pretty simple, so hopefully you can use this for pandas reference in the future.

# ## First: things we didn't cover in class
# 
# ### Counting things
# 
# If during class we had wanted to know how many countries were on each continent, I would use `df.continent.value_counts()`.
# 
# Lots of people like to try `groupby` when you're counting things, but in pandas there is only one rule: **every time you want to count things and think you should use groupby.... don't use `groupby`!** Instead use `value_counts()`.
# 
# ### Filtering your dataset
# 
# We also spent the whole time working with the entire dataset! Oftentimes you only want a subset of it.
# 
# We might have wanted to do something like "I only want to see countries in Africa." In the same way we can do math to every single row at the same time, we can also do comparisons for every single row. We could have asked, "is your `continent` column equal to `"Africa"`?"
# 
# ```python
# df.continent == 'Africa'
# ```
# 
# This only gives me a list of Trues and Falses, which isn't very useful by itself (...technically it's a Series since it has an index). What *is* very useful is being able to say, **I want to see all of the rows where the continent is Africa:**
# 
# ```python
# df[df.continent == 'Africa']
# ```
# 
# There we have it! I could also save this as another variable if I wanted to spend time working with it later:
# 
# ```python
# df_africa = df[df.continent == 'Africa']
# df_africa.head()
# ```
# 
# Hope that's helpful.
# 
# ### Graphing things
# 
# Just put `.plot()` on the end of whatever you're looking at. It works like 75% of the time!
# 
# ```python
# df.groupby('continent').population.sum().plot(kind='barh')
# ```
# 
# The code above will give me a horizontal bar graph of the sum of each continent's population. Technically speaking it works because it's a Series and it plots the index vs the values. 
# 
# If you have a full dataframe, though, you usually need to give it the `x` and `y`.
# 
# ```python
# df.plot(x='life_expectancy', y='per_capita_gdp', kind='scatter')
# ```
# 
# This will give you a scatterplot of each country's life expectancy vs. its per-capita GDP.

# ## 0) Setup
# 
# Import pandas **with the correct name**.

# In[1]:


import pandas as pd


# In[2]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# ## 1) Reading in a csv file
# 
# Use pandas to read in the animals CSV file, saving it as a variable with the normal name for a dataframe

# In[3]:


df = pd.read_csv('animals.csv')


# ## 2) Checking your data
# 
# Display the number of rows and columns in your data. Also display the names and data types of each column.

# In[4]:


df


# In[5]:


df.shape


# In[6]:


df.dtypes


# ## 3) Display the first 3 animals
# 
# Hmmm, we know how to take the first 5, but maybe the first 3. Maybe there is an option to change how many you get? Use `?` to check the documentation on the command.

# In[7]:


df.head(3)


# ## 4) Sort the animals to show me the 3 longest animals
# 
# > **TIP:** You can use `.head()` after you sort things!

# In[8]:


df.sort_values(by='length', ascending=False).head(3)


# ## 5) Get the mean and standard deviation of animal lengths
# 
# You can do this with separate commands or with a single command.
# 
# > **Tip:** You don't know how to do standard deviation, but remember when we did `df.so` and hit tab and it suggested some options for sorting? I'm assuming the standard deviation method starts with `s`....

# In[9]:


df.describe()


# ## 6) How many cats do we have and how many dogs?

# In[10]:


#cats
(df.animal=='cat').sum()


# In[11]:


#dogs
(df.animal=='dog').sum()


# In[12]:


#or if we are allowed to use "groupby"...
df.groupby('animal').count()['name']


# ## 7) Only display the dogs
# 
# > **TIP:** It's probably easiest to make it display the list of `True`/`False` first, then wrap the `df[]` around it.

# In[13]:


df.loc[df.animal=='dog']


# ## 8) Only display the animals that are longer than 40cm

# In[14]:


df.loc[df.length>40]


# ## 9) `length` is the animal's length in centimeters. Create a new column called `inches` that is the length in inches.

# In[15]:


#1 cm = 0.393701 inches

df['inches'] = df.length * 0.39371


# In[16]:


df


# ## 10) Save the cats to a separate variable called `cats`. Save the dogs to a separate variable called `dogs`.
# 
# This is the same as listing them, but you just save the result to a variable instead of looking at it. Be sure to use `.head()` to make sure your data looks right.
# 
# Once you do this, every time you use `cats` you'll only be talking about the cats, and same for the dogs.

# In[17]:


cats = df.loc[df.animal=='cat'].reset_index(drop=True)


# In[18]:


dogs = df.loc[df.animal=='dog'].reset_index(drop=True)


# In[19]:


cats


# In[20]:


dogs


# ## 11) Display all of the animals that are cats and above 12 inches long.
# 
# First do it using the `cats` variable, then also do it using your `df` dataframe.
# 
# > **TIP:** For multiple conditions, you use `df[(one condition) & (another condition)]`

# In[21]:


cats.loc[cats.inches>=12]


# In[22]:


df.loc[(df.animal=='cat')&(df.inches>=12)]


# ## 12) What's the mean length of a cat? What's the mean length of a dog?

# In[23]:


cats.length.mean()


# In[24]:


dogs.length.mean()


# ## 13) If you didn't already, use `groupby` to do #12 all at once

# In[25]:


df.groupby('animal').mean()


# ## 14) Make a histogram of the length of dogs.
# 
# We didn't talk about how to make a histogram in class! It **does not** use `plot()`. Imagine you're a programmer who doesn't want to type out `histogram` - what do you think you'd type instead?
# 
# > **TIP:** The method is four letters long
# >
# > **TIP:** First you'll say "I want the length column," then you'll say "make a histogram"
# >
# > **TIP:** This is the worst histogram ever

# In[26]:


dogs.length.plot(kind='hist')


# ## 15) Make a horizontal bar graph of the length of the animals, with the animal's name as the label
# 
# > **TIP:** It isn't `df['length'].plot()`, because it needs *both* columns. Think about how we did the scatterplot in class.
# >
# > **TIP:** Which is the `x` axis and which is the `y` axis? You'll notice pandas is kind of weird and wrong.
# >
# > **TIP:** Make sure you specify the `kind` of graph or else it will be a weird line thing
# >
# > **TIP:** If you want, you can set a custom size for your plot by sending it something like `figsize=(15,2)`

# In[102]:


df.plot(x='name', y='length', kind='barh', title='The length of animals', width=0.8)


# In[97]:


plt.barh(df.name, df.length, color='green', label='length(cm)')
plt.ylabel('name')
plt.title('The length of animals')
plt.legend(loc='upper right')
plt.show()


# ## 16) Make a sorted horizontal bar graph of the cats, with the larger cats on top
# 
# > **TIP:** Think in steps, even though it's all on one line - first make sure you can sort it, then try to graph it.

# In[ ]:


cats = cats.sort_values(by='length')


# In[112]:


cats.plot(x='name', y='length', kind='barh', title='the length of cats')
plt.show()


# In[110]:


x = cats.name
y = cats.length

plt.barh(x, y, color="blue", label='length(cm)')
plt.ylabel('name')
plt.title('the length of cats')
plt.legend(loc='lower right')
plt.show()


# ## 17) As a reward for getting down here: run the following code, then plot the number of dogs vs. the number of cats
# 
# > **TIP:** Counting the number of dogs and number of cats does NOT use `.groupby`! That's only for calculations.
# >
# > **TIP:** You can set a title with `title="Number of animals"`

# In[54]:


import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# In[113]:


df.animal.value_counts().plot(kind='barh', title='Number of animals')
plt.show()


#!/usr/bin/env python
# coding: utf-8

# # Homework 5, Part 2: Answer questions with pandas
# 
# **Use the Excel file to answer the following questions.** This is a little more typical of what your data exploration will look like with pandas.

# ## 0) Setup
# 
# Import pandas **with the correct name** .

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# ## 1) Reading in an Excel file
# 
# Use pandas to read in the `richpeople.xlsx` Excel file, saving it as a variable with the name we'll always use for a dataframe.
# 
# > **TIP:** You will use `read_excel` instead of `read_csv`. Trying `read_excel` the first time will probably not work, you'll get an error message. Be sure to read the error carefully: *you probably need to install a new library before it will work, and the error tells you what the library is named*.

# In[2]:


df = pd.read_excel('richpeople.xlsx')


# ## 2) Checking your data
# 
# Display the number of rows and columns in your data. Also display the names and data types of each column.

# In[3]:


df.head()


# In[4]:


df.dtypes


# In[5]:


df.shape


# ## 3) Who are the top 10 richest billionaires? Use the `networthusbillion` column.

# In[6]:


df.sort_values(by='networthusbillion').head(10)


# ## 4) How many male billionaires are there compared to the number of female billionares? What percent is that? Do they have a different average wealth?
# 
# > **TIP:** The last part uses `groupby`, but the count/percent part does not.
# > **TIP:** When I say "average," you can pick what kind of average you use.

# In[7]:


#How many male billionaires are there compared to the number of female billionares? 
df.gender.value_counts()


# In[8]:


#What percent is that?
round(df.gender.value_counts()['male'] / df.gender.count() *100, 1)


# In[9]:


df.groupby('gender').networthusbillion.mean()


# In[10]:


df.groupby('gender').networthusbillion.sum() / df.gender.value_counts()


# ## 5) What is the most common source/type of wealth? Is it different between males and females?
# 
# > **TIP:** You know how to `groupby` and you know how to count how many times a value is in a column. Can you put them together???
# > **TIP:** Use percentages for this, it makes it a lot more readable.

# In[11]:


df.columns


# In[12]:


#the most common type of wealth for males is "founder non-finance"
df_type = df.groupby(['gender','typeofwealth']).name.count().unstack().T
df_type = df_type.sort_values(by='male', ascending=False)
df_type


# In[13]:


#whereas for females, it's "inherited"
df_type.sort_values(by='female', ascending=False)


# ## 6) What companies have the most billionaires? Graph the top 5 as a horizontal bar graph.
# 
# > **TIP:** First find the answer to the question, then just try to throw `.plot()` on the end
# >
# > **TIP:** You can use `.head()` on *anything*, not just your basic `df`
# >
# > **TIP:** You might feel like you should use `groupby`, but don't! There's an easier way to count.
# >
# > **TIP:** Make the largest bar be at the top of the graph
# >
# > **TIP:** If your chart seems... weird, think about where in the process you're sorting vs using `head`

# In[14]:


df.company.unique()


# In[15]:


#I felt like.....
#df.groupby('company').name.count().sort_values(ascending=False).head(5)


# In[16]:


df.company.value_counts().head(5)


# In[17]:


df.company.value_counts().head(5).sort_values().plot(kind='barh')
plt.show()


# ## 7) How much money do these billionaires have in total?

# In[18]:


top5_companies = df.company.value_counts().index[:5].to_list()

df.loc[df.company.isin(top5_companies)].networthusbillion.sum()


# ## 8) What are the top 10 countries with the most money held by billionaires?
# 
# I am **not** asking which country has the most billionaires - this is **total amount of money per country.**
# 
# > **TIP:** Think about it in steps - "I want them organized by country," "I want their net worth," "I want to add it all up," and "I want 10 of them." Just chain it all together.

# In[19]:


df.columns


# In[20]:


df.groupby('citizenship').sum().sort_values(by='networthusbillion', ascending=False).head(10)


# ## 9) How old is an average billionaire? How old are self-made billionaires  vs. non self-made billionaires? 

# In[21]:


df.selfmade.unique()


# In[22]:


df.age.mean()


# In[23]:


df.groupby('selfmade').age.mean().round(1)


# ## 10) Who are the youngest billionaires? Who are the oldest? Make a graph of the distribution of ages.
# 
# > **TIP:** You use `.plot()` to graph values in a column independently, but `.hist()` to draw a [histogram](https://www.mathsisfun.com/data/histograms.html) of the distribution of their values

# In[24]:


#Who are the youngest billionaires?
df.loc[df.age==df.age.min()]


# In[25]:


#Who are the oldest?
df.loc[df.age==df.age.max()]


# In[26]:


#Make a graph of the distribution of ages
df.age.hist(ec='black')
plt.xlabel('age')
plt.ylabel('number of billionaires')
plt.title('How old are billionaires?')
plt.show()


# ## 11) Make a scatterplot of net worth compared to age

# In[29]:


df.plot(x='age', y='networthusbillion',kind='scatter')


# In[33]:


x = df.age
y = df.networthusbillion

plt.scatter(x,y)
plt.title('age and wealth')
plt.ylabel('net worth in bil$')
plt.xlabel('age')
plt.show()


# ## 13) Make a bar graph of the wealth of the top 10 richest billionaires
# 
# > **TIP:** When you make your plot, you'll need to set the `x` and `y` or else your chart will look _crazy_
# >
# > **TIP:** x and y might be the opposite of what you expect them to be

# In[49]:


df_top10 = df.sort_values(by='networthusbillion').tail(10)
x = df_top10.name
y = df_top10.networthusbillion

plt.barh(x,y, label='net worth in bil USD')
plt.title('TOP 10 richest billionaires')
plt.ylabel('name')
plt.legend(loc='lower right')
plt.show()


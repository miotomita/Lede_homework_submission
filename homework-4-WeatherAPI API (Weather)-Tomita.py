#!/usr/bin/env python
# coding: utf-8

# # WeatherAPI (Weather)
# 
# Answer the following questions using [WeatherAPI](http://www.weatherapi.com/). I've added three cells for most questions but you're free to use more or less! Hold `Shift` and hit `Enter` to run a cell, and use the `+` on the top left to add a new cell to a notebook.
# 
# Be sure to take advantage of both the documentation and the API Explorer!
# 
# ## 0) Import any libraries you might need
# 
# - *Tip: We're going to be downloading things from the internet, so we probably need `requests`.*
# - *Tip: Remember you only need to import requests once!*

# In[1]:


import requests
from datetime import datetime, date, timedelta


# ## 1) Make a request to the Weather API for where you were born (or lived, or want to visit!).
# 
# - *Tip: The URL we used in class was for a place near San Francisco. What was the format of the endpoint that made this happen?*
# - *Tip: Save the URL as a separate variable, and be sure to not have `[` and `]` inside.*
# - *Tip: How is north vs. south and east vs. west latitude/longitude represented? Is it the normal North/South/East/West?*
# - *Tip: You know it's JSON, but Python doesn't! Make sure you aren't trying to deal with plain text.* 
# - *Tip: Once you've imported the JSON into a variable, check the timezone's name to make sure it seems like it got the right part of the world!*

# In[2]:


#Weather API
#You can change locations here:
location = 'Tokyo'

url = f"http://api.weatherapi.com/v1/current.json?key=42febc308e914aaf9ed193214221306&q={location}&aqi=yes"


# In[3]:


#retrieve raw data
response = requests.get(url)
data = response.json()


# In[4]:


#check keys-1
data['location'].keys()


# In[5]:


#check keys-2
data['current'].keys()


# In[6]:


#check latitude/longitude
print(data['location']['lat'])
print(data['location']['lon'])


# In[7]:


#check the local time
print(data['location']['localtime'])


# In[8]:


#current weather
condition = data['current']['condition']['text']

text = f"Current weather in {location} is {condition.lower()}."
print(text)


# ## 2) What's the current wind speed? How much warmer does it feel than it actually is?
# 
# - *Tip: You can do this by browsing through the dictionaries, but it might be easier to read the documentation*
# - *Tip: For the second half: it **is** one temperature, and it **feels** a different temperature. Calculate the difference.*

# In[9]:


#wind speed
windspeed_m = data['current']['wind_mph']
windspeed_k = data['current']['wind_kph']

text = f"The current wind speed is {windspeed_m} miles per hour / {windspeed_k} km per hour."
print(text)


# In[10]:


#temperature in Celcius/Fahrenheit degrees
scales = {'c':'°C', 'f':'°F'}

#compare the actual/feels-like temperatures
for key, val in scales.items():
    temp_actual = data['current'][f"temp_{key}"]
    temp_feels = data['current'][f"feelslike_{key}"]
    temp_dif = temp_feels - temp_actual
    if temp_dif == 0:
        text = 'The feels the same as the actual temperature.'
    elif temp_dif > 0:
        text = f"It feels {temp_dif}{val} warmer than the actual temperature."
    else:
        text = f"It feels {temp_dif}{val} colder than the actual temperature."
    print(text)


# ## 3) What is the API endpoint for moon-related information? For the place you decided on above, how much of the moon will be visible tomorrow?
# 
# - *Tip: Check the documentation!*
# - *Tip: If you aren't sure what something means, ask in Slack*

# There are 2 different ways to look up for moon-related info.
# 
# 1: **astronomy API**<br>
# endpoint:  *~/astronomy.json?key={<font color ="blue">API KEY</font>}&q={<font color ="blue">location</font>}*
# 
# 2: **forecast API**<br>
# endpoint:  *~forecast.json?key={<font color ="blue">API KEY</font>}&q={<font color ="blue">location</font>}&dt={<font color ="blue">yyyy-MM-dd</font>}*

# In[11]:


#forecast API
#I have ignored timezone difference here
#But if you want to do it precisely, use timedelta(hours=9+24) for Tokyo
target_date = datetime.now() + timedelta(days=1)
target_date = target_date.strftime('%Y-%m-%d')

url = f"http://api.weatherapi.com/v1/forecast.json?key=42febc308e914aaf9ed193214221306&q={location}&dt={target_date}&aqi=yes"


# In[12]:


#retrieve data
response = requests.get(url)
data2 = response.json()


# In[13]:


data2['forecast'].keys()


# In[14]:


data2['forecast']['forecastday'][0]['date']


# In[15]:


data2['forecast']['forecastday'][0]['astro']


# In[16]:


#moon phase
moon_phase = data2['forecast']['forecastday'][0]['astro']['moon_phase']
text = f"{moon_phase.capitalize()} is visible in {location} tomorrow."
print(text)


# ## 4) What's the difference between the high and low temperatures for today?
# 
# - *Tip: When you requested moon data, you probably overwrote your variables! If so, you'll need to make a new request.*

# In[17]:


target_date = datetime.now()
target_date = target_date.strftime('%Y-%m-%d')

url = f"http://api.weatherapi.com/v1/forecast.json?key=42febc308e914aaf9ed193214221306&q={location}&dt={target_date}&aqi=yes"


# In[18]:


#retrieve data
response = requests.get(url)
data3 = response.json()


# In[19]:


#I ignored the time difference again, because it was too confusing(It's already tomorrow)
data3['forecast']['forecastday'][0]

#scales = {'c':'°C', 'f':'°F'}
#compare the high/low temperatures
for key, val in scales.items():
    #temperatures
    temp_high = data3['forecast']['forecastday'][0]['day'][f"maxtemp_{key}"]
    temp_low = data3['forecast']['forecastday'][0]['day'][f"mintemp_{key}"]
    #calculate
    temp_dif = temp_high - temp_low
    #texts
    if temp_dif == 0:
        text = f"The high and low temperatures are the same for today. Both are {temp_high}{val}."
    else:
        text = f"The difference between the high and low temperatures are {temp_dif:.2f}{val} for today."
    #print
    print(text)


# ## 4.5) How can you avoid the "oh no I don't have the data any more because I made another request" problem in the future?
# 
# What variable(s) do you have to rename, and what would you rename them?

# In[20]:


#I used different URLs for each questions...so I don't have variables that I would wish to avoid overwriting...

#But I could have done better with naming data-sets, as data, data2...is not readable enough
#However, it's tiresome to go over the long names for variables again and again especially when you are writing long codes
#So I'd rather use data1,2,3...But should I change it?

#data
#data2
#data3


# ## 5) Go through the daily forecasts, printing out the next three days' worth of predictions.
# 
# I'd like to know the **high temperature** for each day, and whether it's **hot, warm, or cold** (based on what temperatures you think are hot, warm or cold).
# 
# - *Tip: You'll need to use an `if` statement to say whether it is hot, warm or cold.*

# In[21]:


#3 days forecasts
days =3
url = f"http://api.weatherapi.com/v1/forecast.json?key=42febc308e914aaf9ed193214221306&q={location}&days={days}"


# In[22]:


#retrieve data
response = requests.get(url)
data4 = response.json()


# In[23]:


for i in range(len(data4['forecast']['forecastday'])):
    #date
    forecast_date = data4['forecast']['forecastday'][i]['date']
    forecast_date = datetime.strptime(forecast_date, '%Y-%m-%d').strftime('%B %d')
    #highest temp
    temp_highest = data4['forecast']['forecastday'][i]['day']['maxtemp_c']
    #text
    text = f"The highest temperature on {forecast_date} will be {temp_highest}°C."
    if temp_highest >=25:
        text = text + " " + "It's going to be a hot day."
    elif temp_highest >=15:
        text = text + " " + "You can enjoy a warm day."
    else:
        text = text + " " + "It's going to be a cold day. Don't forget to bring your jacket."
    print(text)


# ## 5b) The question above used to be an entire week, but not any more. Try to re-use the code above to print out seven days.
# 
# What happens? Can you figure out why it doesn't work?
# 
# * *Tip: it has to do with the reason you're using an API key - maybe take a look at the "Air Quality Data" introduction for a hint? If you can't figure it out right now, no worries.*

# In[24]:


#1st Try (did not work)
#Forecast API
#As they provide the data for air quality only for 3 days in the forecast API, the data for other parts do not show up either
days =7
url = f"http://api.weatherapi.com/v1/forecast.json?key=42febc308e914aaf9ed193214221306&q={location}&days={days}"

#retrieve data
response = requests.get(url)
data5 = response.json()

print("The length of the data is", len(data5), "....")


# In[25]:


#2nd Try (did not work)
#Forecast API WITH "aqi=no"
#As they provide the data for air quality only for 3 days in the forecast API, the data for other parts do not show up either
days =7
url = f"http://api.weatherapi.com/v1/forecast.json?key=42febc308e914aaf9ed193214221306&q={location}&days={days}&aqi=no"

#retrieve data
response = requests.get(url)
data5 = response.json()

print("The length of the data is", len(data5), "....")


# In[26]:


#3rd Try (did not work)
#FUTURE API WITH "aqi=no"
days =7
url = f"http://api.weatherapi.com/v1/future.json?key=42febc308e914aaf9ed193214221306&q={location}&days={days}&aqi=no"

#retrieve data
response = requests.get(url)
data5 = response.json()

print("The length of the data is", len(data5), "....")
#Maybe you have to pay for that....?
print(data5)


# In[27]:


#4th Try (Successful!!!...I hope.)
#Forecast API WITH dt={yyyy-MM-dd}
print('--------')
for i in range(1,8):
    #target date
    target_date = datetime.now() + timedelta(days=i)
    target_date = target_date.strftime('%Y-%m-%d')
    print(target_date)
    
    #API
    url = f"http://api.weatherapi.com/v1/forecast.json?key=42febc308e914aaf9ed193214221306&q={location}&dt={target_date}&aqi=yes"
    print(url)    
    
    #retrieve data
    response = requests.get(url)
    daily_data = response.json()

    #temperatures
    text = daily_data['forecast']['forecastday'][0]['day']['condition']['text']
    print(text)
    print('--------')
    


# ## 6) What will be the hottest day in the next three days? What is the high temperature on that day?

# In[54]:


#data4: Forecast data for the next 3 days

#dic
temp_dic_c = {}
temp_dic_f = {}

#data
for i in range(len(data4['forecast']['forecastday'])):
    forecast_date = data4['forecast']['forecastday'][i]['date']
    maxtemp_c = data4['forecast']['forecastday'][i]['day']['maxtemp_c']
    maxtemp_f = data4['forecast']['forecastday'][i]['day']['maxtemp_f']
    temp_dic_c[forecast_date] = maxtemp_c
    temp_dic_f[forecast_date] = maxtemp_f

#hottest day
hottest_day_temp_c = max(temp_dic_c.values())
hottest_day_temp_f = max(temp_dic_f.values())
hottest_day_list = [key for key, val in temp_dic_c.items() if val == hottest_day_temp_c]

#text
#Just in case there are more than 1 day with the same highest temperature
if len(hottest_day_list)>1:
    text = ", ".join(hottest_day_list) + " are the hottest days in the next 3 days."
    text = text + " " + f"It will be {hottest_day_temp_c}°C /{hottest_day_temp_f}°F."
else:
    text = hottest_day_list[0] + " is the hottest day in the next 3 days."
    text = text + " " + f"It will be {hottest_day_temp_c}°C /{hottest_day_temp_f}°F."
print(text) 


# ## 7) What's the weather looking like for the next 24+ hours in Miami, Florida?
# 
# I'd like to know the temperature for every hour, and if it's going to have cloud cover of more than 50% say "{temperature} and cloudy" instead of just the temperature. 
# 
# - *Tip: You'll only need one day of forecast*

# In[108]:


#URL
location = 'Miami'
target_date = datetime.now() + timedelta(days=1)
target_date = target_date.strftime('%Y-%m-%d')

url = f"http://api.weatherapi.com/v1/forecast.json?key=42febc308e914aaf9ed193214221306&q={location}&dt={target_date}"
print(url)


# In[109]:


#retrieve data
response = requests.get(url)
data6 = response.json()


# In[122]:


hourly_dic = {}

for hourly_data in data6['forecast']['forecastday'][0]['hour']:
    hour = hourly_data['time']
    #This is for the next question
    hourly_dic[hour] = hourly_data['temp_f']
    
    #text
    text = "The temperature is " + str(hourly_data['temp_c']) + '°C' + '/' + str(hourly_data['temp_f']) + '°F'
    text = text + " and cloudy." if hourly_data['cloud'] > 50 else text + "."
    
    print(hour, ": ", text)


# ## 8) For the next 24-ish hours in Miami, what percent of the time is the temperature above 85 degrees?
# 
# - *Tip: You might want to read up on [looping patterns](http://jonathansoma.com/lede/foundations-2017/classes/data%20structures/looping-patterns/)*

# In[130]:


hours_above85 = len([val for val in hourly_dic.values() if val > 85]) 
hours_total =  len(hourly_dic.values()) 
pct_above85 = hours_above85 / hours_total * 100

print(f"{pct_above85}% of the time is the temperature above 85 degrees.")


# ## 9) How much will it cost if you need to use 1,500,000 API calls?
# 
# You are only allowed 1,000,000 API calls each month. If you were really bad at this homework or made some awful loops, WeatherAPI might shut down your free access. 
# 
# * *Tip: this involves looking somewhere that isn't the normal documentation.*

# In[132]:


#Source: https://www.weatherapi.com/pricing.aspx
print("$4 for 2,000,000 Calls per month.")


# ## 10) You're too poor to spend more money! What else could you do instead of give them money?
# 
# * *Tip: I'm not endorsing being sneaky, but newsrooms and students are both generally poverty-stricken.*

# In[134]:


print("Sign up with another email account. If you don't have one, create a new one on google (or other free accounts).")


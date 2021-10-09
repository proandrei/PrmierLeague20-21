#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[2]:


#Upload the data into Python for players and results

path = 'C:/Users/Andrei/Desktop/Python/Fotbal/players_21.csv'
player_data = pd.read_csv(path)

path = 'C:/Users/Andrei/Desktop/Python/Fotbal/results.csv'
results = pd.read_csv(path)

print(results)


# In[3]:


#Extract the relevant data from both dataframes 
player_data = player_data[player_data['league_name']
                                       == 'English Premier League']

player_data = player_data[['short_name', 'overall', 'value_eur', 
                           'wage_eur', 'age', 'height_cm','league_name', 'club_name',
                           'club_position', 'pace', 'passing', 'dribbling',
                           'defending', 'physic']]

results = results[['Date', 'Time', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]


# In[4]:


#Veirfy that both datasets hold the same number of teams
#and the same names for them

print(len(results['HomeTeam'].unique()))
print(len(player_data['club_name'][player_data['league_name']  == 'English Premier League'].unique()))

print(sorted(results['HomeTeam'].unique()))
print(sorted(player_data['club_name'][player_data['league_name'] == 'English Premier League'].unique()))


# In[5]:


#Replace the team names in the players dataset
#to match the ones from results

names_players = sorted(player_data['club_name'][player_data['league_name'] 
                                                == 'English Premier League'].unique())
names_results = sorted(results['HomeTeam'].unique())


counter = 0

for name in names_players:
    player_data['club_name'] = player_data['club_name'].replace(
        name, names_results[counter])
    counter += 1


# In[6]:


#Create aggregate statistcis for each club regarding the studied variables

aggregate = pd.DataFrame(player_data.groupby(['club_name']).mean())
print(aggregate)


# In[7]:


#Recreate the standing at the end of the league using the results dataset

#Start by adding points for the home and away team on each match

ht_points = []
aw_points = []

for counter in range(len(results.index)):
    if results.iloc[counter]['FTHG'] > results.iloc[counter]['FTAG']:
        ht_points.append(3)
        aw_points.append(0)
    elif results.iloc[counter]['FTHG'] == results.iloc[counter]['FTAG']:
        ht_points.append(1)
        aw_points.append(1)
    else:
        ht_points.append(0)
        aw_points.append(3)
    
results['HPoints'] = ht_points
results['APoints'] = aw_points

#Aggregate the results 

standings = pd.DataFrame(results.groupby(['HomeTeam']).sum('HPoints'))
print(standings)


# In[8]:


#Add the team names to the dataframe, the group by function will order alphabetically if not instructed otherwise
standing = pd.DataFrame()
standing['Team'] = results.groupby(['AwayTeam']).sum('APoints').index

#Add Away Points, Home Point, Goals scored away and at home, goals conceded away and at home

standing['AP'] = list(results.groupby(['AwayTeam']).sum('APoints')['APoints']) # Away points
standing['HP'] = list(results.groupby(['HomeTeam']).sum('HPoints')['HPoints']) #Home Points

standing['AG'] = list(results.groupby(['HomeTeam']).sum('FTHG')['FTHG']) #Away goals scored
standing['HG'] = list(results.groupby(['AwayTeam']).sum('FTAG')['FTAG']) #Home goals conceded

standing['AC'] = list(results.groupby(['HomeTeam']).sum('FTAG')['FTAG']) #Away goals conceded
standing['HC'] = list(results.groupby(['AwayTeam']).sum('FTHG')['FTHG']) #Home goals conceded

standing['Points'] = standing['AP'] + standing['HP'] # Total points
standing['Goals_Scored'] = standing['AG'] + standing['HG'] #Total goals scored
standing['Goals_Conceded'] = standing['AC'] + standing['HC'] #Total goals conceded
standing['Difference'] = standing['Goals_Scored'] - standing['Goals_Conceded'] #Difference bwteen goals scored and conceded

standing.sort_values(['Points', 'Difference' ], ascending = False, inplace = True) #Sort teeams as in final standing


#Recreate the official standing of the 20/21 season

official_standing = standing[['Team','Points', 'Goals_Scored', 'Goals_Conceded', 'Difference']]
print(official_standing.reset_index(drop = True))


# In[9]:


#Merge the results data with the team aggregate player information data
standing.set_index('Team', drop = True, inplace = True) # Make the team names index - as in the other dataset
dataset = standing.merge(aggregate, left_index = True, right_index = True)


# In[10]:


for team in dataset.index:
    if team in dataset.head(10).index:
           ay =  plt.scatter(dataset['wage_eur'][dataset.index == team],
                dataset['Points'][dataset.index == team], label = team)

plt.ylabel('Points')
plt.xlabel('Wage per week in "0£')
plt.title('Comparison of points won on salary cost')
plt.legend(loc='best', ncol = 2)
plt.show()


# In[11]:


for team in dataset.index:
    if team in dataset.head(10).index:
           ax =  plt.scatter(dataset['overall'][dataset.index == team],
                dataset['Points'][dataset.index == team], label = team)

plt.ylabel('Points')
plt.xlabel('Overall')
plt.title('Comparison of points won on salary cost')
plt.legend(loc='best', ncol = 2)
plt.show()


# In[12]:


for team in dataset.index:
    if team in dataset.head(10).index:
           ax =  plt.scatter(dataset['wage_eur'][dataset.index == team],
                dataset['overall'][dataset.index == team], label = team)

plt.ylabel('Overall')
plt.xlabel('Wage')
plt.title('Comparison of points won on salary cost')
plt.legend(loc='best', ncol = 2)
plt.show()


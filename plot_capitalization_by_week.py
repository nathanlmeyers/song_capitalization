import pandas as pd
from matplotlib import pyplot as plt

# Read in the data from https://data.world/kcmillersean/billboard-hot-100-1958-2017
dat = pd.read_csv('hot_stuff.csv')

# Create new columns for plotting
weeks_songs = dat[['WeekID','Song']]
weeks_songs['Just Letters Length'] = weeks_songs['Song'].apply(lambda x: sum(1 for l in x if l.isalpha()))
weeks_songs['Capitalized Letters'] = weeks_songs['Song'].apply(lambda x: sum(1 for l in x if l.isalpha() and l.isupper()))
weeks_songs['Lower Case Letters'] = weeks_songs['Song'].apply(lambda x: sum(1 for l in x if l.isalpha() and l.islower()))
weeks_songs['All Caps'] = (weeks_songs['Just Letters Length'] == weeks_songs['Capitalized Letters']) & (weeks_songs['Just Letters Length'] > 0)
weeks_songs['All Lower Case'] = (weeks_songs['Just Letters Length'] == weeks_songs['Lower Case Letters']) & (weeks_songs['Just Letters Length'] > 0)
date_list = weeks_songs['WeekID'].values.tolist()
weeks_songs['Week'] = [pd.to_datetime(x.split('/')[2]+'-'+x.split('/')[0].zfill(2)+'-'+x.split('/')[1].zfill(2)) for x in date_list]

# Aggregate columns
weeks_songs_summary = weeks_songs[['Week','All Caps','All Lower Case']].groupby('Week').aggregate('sum').sort_values(by=['Week'])

# Grab the last 1000 weeks for plotting
w10 = weeks_songs_summary[-1000:]

# Make a line plot with matplotlib
ax = w10.plot(kind='line')
plt.title('Song Capitalization by Week')
plt.ylabel('Number of Songs')
fig = ax.get_figure()
fig.set_size_inches(18.5, 10.5)
fig.savefig('capitalization_plot.png')

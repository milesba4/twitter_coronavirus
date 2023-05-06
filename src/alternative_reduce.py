#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
#parser.add_argument('--input_paths',nargs='+',required=False)
parser. add_argument('--hashtags', nargs='+', required = True)
parser.add_argument('--output_path',required=False)
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#Reduce
hashtags = args.hashtags
print("hashtags=", hashtags)
directory = 'outputs'
total = defaultdict(lambda: Counter())

#create list of days
days = ['20-' + filename[13:19] for filename in sorted(os.listdir(directory)) if '.lang' in filename]
df_dict={'days': days}
#print("df_dict=", df_dict)
for filename in sorted(os.listdir(directory)):
    if '.lang' in filename:
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f) as j:
                #load the dictionary of that day
                tmp = json.load(j)
                day= '20-' + filename[13:19]
                #for each hashtag
                for hashtag in hashtags:
                    #only if hashtag in day of tweets
                    if hashtag in tmp:
                        #print("day:", day, "hashtag:", hashtag)
                        #extract  day[hashtag] values and sum them up
                        total[day][hashtag] = sum(list(tmp[str(hashtag)].values()))

#Visualize
#Creating dictionary for data frame 
for hashtag in hashtags:
    df_dict[hashtag[1:]]= [total[day][hashtag] for day in days]
print("df_dict=", df_dict)

df_dict['days'] = [day.replace('.','') for day in df_dict['days']]
print("df_dict=", df_dict)
#Creating DataFrame from df_dict
df = pd.DataFrame(df_dict)
print("df=", df)
#converting days column to datetime
df["days"] = pd.to_datetime(df["days"], format = '%y-%m-%d')
#print("df=", df)
#plotting df
fig, ax = plt.subplots()
plt.plot(df['days'], df['coronavirus'], label = 'coronavirus')
plt.plot(df['days'], df['covid19'], label = 'covid19')
#Creating labels
plt.xlabel('Days')
plt.ylabel('Number of Tweets')
plt.legend(loc='upper left')
plt.tight_layout()
xlabels = [label.get_text() for label in ax.get_xticklabels()]
xlabels[-1]=''
ax.set_xticklabels(xlabels)
print("xlabels2=", xlabels)
plt.subplots_adjust(bottom=0.3)
#plt.xticks(range(len(days)),days,  rotation=90)
#plt.yticks([0, 10, 50, 100, 500, 1000, 5000, 10000], rotation=45)
plt.title('Number of tweets per hashtag per day')
plt.savefig('final_alt_reduce.png')



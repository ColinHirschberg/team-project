# Initiated by Kelsey Kraus
#
# Contributors: <UPDATE ME!> 
#
# Description: <UPDATE ME!> This file currently contains the instructions for replicating the data cleaning method implemented by CTK 2016.

# NOTE: the suggested approaches below are NOT the only way to complete this task! It is merely given as a starting point. You can choose to do this in a different way if you want, but be sure to comment on your process along the way.

# !!! You may need to run in your Shell: pip install pandas !!!
# This line is written by Max

import os
import pandas
import re

allTweets = []
with open('pro-who-tweets.csv') as file:
  allTweets = file.read()
  print(allTweets)


# -- Preprocessing: -- We don't care about the other data in our .csv. We want to only get the tweet text data in 'content' column.
# -- Suggested approach: -- create a list variable and save the 'content' column of the pro-who-tweets.csv file as your list. Print the length of the list. See here for more: https://www.geeksforgeeks.org/python-read-csv-columns-into-list/



# === Part 1: Filtering ===

# -- First filter: -- Remove duplicates. 
# -- Suggested approach: -- using your list, convert the list into a dictionary, which will automatically remove duplicates. Then convert your dictionary back into a list. Print the length of the list. https://www.w3schools.com/python/python_howto_remove_duplicates.asp

#A dictionary is an assemblage of key-value pairs.

#Dictionary comprehension: {expression(s):s for s in list} or {s: expression(s)for s in list}  ----- key:value

#allTweetsContent_dict = {index(s)+1:s for s in content_list} #Conversion of a list to dictionary will eliminate duplicates because a dictionary's entries are unique.
#allTweetsContent = list(content_list_dict.values()) #Extraction of a list of values from the dictionary

print(len(allTweetsContent))

allTweetsContent_dict = {allTweetsContent.index(s)+1: s for s in allTweetsContent}

allTweetsContent = []

allTweetsContent = list(allTweetsContent_dict.values())

print(len(allTweetsContent))



# -- Second filter: -- Remove tweets where the last non-whitespace character before the word 'who' is not a letter or a comma. See Lecture 3 slides for more explanation of this!
# -- Suggested approach: -- Use the list you created as a result of the previous filter. Save the 10 possible pronouns in a list. Create a loop to run through each entry in your list. Use a conditional statement to construct a regular expression match, and save the list elements matching your condition. Print the length of the list.

pronouns = ["you", "she", "her", "he", "him", "we", "us", "they", "them", "those"]

#Seek out a PRO who sequence in which the last whitespace character is anything other than a letter or a comma, and apply remove() list method

for i in range(len(pronouns)):
  for j in range(len(allTweetsContent)):
    #The jth item of the list allTweetsContent is the reference string on which we perform the matching operation.
    pronoun = pronouns[i]
    m = re.search(pronoun+r'\s*[^abcdefghijklmnopqrstuvwxyz,]\s+(W|w)ho',allTweetsContent[j])
    if type(m) == re.Match:
      allTweetsContent.remove(allTweetsContent[j]) #Lists are mutable unlike strings and tuples.
    else:
      continue
      
print(len(allTweetsContent))


# -- Third filter: -- Remove the pattern 'of PRO who'
# -- Suggested approach: -- Create another loop, and another conditional statement using a regular expression from the list you got from the previous filter. This time, save only those that DO NOT match the conditional statement. Print the length of the list.





# -- Fourth filter: -- Remove tweets where the pronoun 'it' preceeds the word 'who' by 2-4 words
# -- Suggested approach: -- Write a regular expression that picks out this pattern. Using the list you generated from the previous filter, use create a loop with a conditional statement that removes this pattern. Print the length of the list.





# -- Fifth filter: -- Remove tweets where 'PRO who' is preceded by the verbs 'ask', 'tell', 'wonder', 'inform', and 'show'.
# -- Suggested approach: --  Save the verbs above into a list. Create a loop that iterates through your pronoun list from above, and removes examples that contain the pattern '[element-from-verb-list] [element-from-PRO-list]'. Print the length of the list.





# === Part 2: Uniqueness ===

# -- Instruction: -- You now need to find out whether the tweets you have left are "literary" or "non-literary", according to CTK's classification. I've written a bit of this for you. Modify the block of code below so that it runs with your variable names. You should replace 'tweetList' in the 'for' block with your variable name that holds the final filtered list of 'PRO who' tweets.

# Test variable: contains a short list of test utterances for the pattern "who <word1> <word2>"
tweetList = ['this is a quote: he who shall not be named', 'who among us really', 'jeff is wondering who sings', 'he who shall not be named again', 'but who among us is perfect']

# This evaluates each tweet in TweetList for whether it contains the specified regex search, and whether that regex pattern in a tweet matches exactly to any other tweet in the list. If it does, it is assigned a value True. If it doesn't, it's assigned a value False.
for tweet in tweetList:
  whoPhrase = re.search("who \w+ \w+", tweet)
  try:
    trueFalseList = [whoPhrase.group() in tweet for tweet in tweetList]
  except AttributeError:
    trueFalseList = False
print(trueFalseList)

# The following takes our two lists, tweetList and trueFalseList, and zips them together. It then creates a dataframe out of this list, that can then be converted to a .csv file

annotatedTweetList = list(zip(tweetList, trueFalseList))
tweetDataframe = pandas.DataFrame(annotatedTweetList)
tweetDataframe.to_csv('literary-annotated-tweets.csv', header=["Tweets", "isLiterary"], index=False)


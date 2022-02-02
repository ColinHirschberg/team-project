# Initiated by Kelsey Kraus
#
# Contributors: Yuma Yamada, Sebastian Bissiri, Colin Hirschberg, Max Xie
#
# Description: This file contains the source code for replicating the data cleaning method implemented by CTK 2016.

# NOTE: the suggested approaches below are NOT the only way to complete this task! It is merely given as a starting point. 
#       You can choose to do this in a different way if you want, but be sure to comment on your process along the way.

# !!! You may need to run in your Shell: pip install pandas !!!
import os
import pandas
import re
import csv
import copy

allTweets = []
fields = []
allTweetsContent = []
with open('pro-who-tweets.csv', 'r') as file:
  # Parse each lines of tweets
  csvReader = csv.reader(file)
  # Read in a list of fields
  fields = next(csvReader)
  # Add each row of the csv file to allTweets 
  for row in csvReader:
    allTweets.append(row)



# -- Preprocessing: -- We don't care about the other data in our .csv. We want to only get the tweet text data in 'content' column.
# -- Suggested approach: -- create a list variable and save the 'content' column of the pro-who-tweets.csv file as your list. 
#     Print the length of the list. See here for more: https://www.geeksforgeeks.org/python-read-csv-columns-into-list/
# Find the content field from all of the fields
content_field = fields.index("content")
# Add all tweets to a list of tweets called allTweetsContent
for row in allTweets:
  allTweetsContent.append(row[content_field])
print(f"Length of the list with all of the tweets: {len(allTweetsContent)}")

# === Part 1: Filtering ===

# -- First filter: -- Remove duplicates. 
# -- Suggested approach: -- using your list, convert the list into a dictionary, which will automatically remove duplicates. 
#    Then convert your dictionary back into a list. Print the length of the list. https://www.w3schools.com/python/python_howto_remove_duplicates.asp
# Dictionary comprehension: {expression(s):s for s in list} or {s: expression(s)for s in list}  ----- key:value

#Conversion of a list to dictionary will eliminate duplicates because a dictionary's entries are unique.
#allTweetsContent_dict = {index(s)+1:s for s in content_list} 
#allTweetsContent = list(content_list_dict.values()) #Extraction of a list of values from the dictionary
allTweetsContent_dict = {allTweetsContent.index(s)+1: s for s in allTweetsContent}
allTweetsContent = []
allTweetsContent = list(allTweetsContent_dict.values())
print(f"Length of the tweet list with duplicates removed: {len(allTweetsContent)}")



# -- Second filter: -- Remove tweets where the last non-whitespace character before the word 'who' is not a letter or a comma.
#                      See Lecture 3 slides for more explanation of this!
# -- Suggested approach: -- Use the list you created as a result of the previous filter. Save the 10 possible pronouns in a list. 
#    Create a loop to run through each entry in your list. 
#    Use a conditional statement to construct a regular expression match, and save the list elements matching your condition. Print the length of the list.
pronouns = ["you", "she", "her", "he", "him", "we", "us", "they", "them", "those"]

#Seek out a PRO who sequence in which the last whitespace character is anything other than a letter or a comma, and apply remove() list method
allTweetsContentNew_1 = []
for j in range(len(allTweetsContent)):
  #reference string: allTweetsContent[j]
  match = False
  for k in range(len(pronouns)):
    # I spent one hour on just getting the index k correct.
    pronoun = pronouns[k] 
    # Only if the match object is not an empty list after checking all pronouns, append the tweet to a list.
    m = re.findall(rf'({pronoun}\s*[^a-z,]\s+who|{pronoun}\s*[^a-z,]\s+Who)',allTweetsContent[j])
    # Scenario in which a match to the regex is detected
    if len(m)>0: 
      match = True
    # A match has been detected earlier or now. 
    # (Note: both if statements can apply in such case that a match is sensed at k=8)
    if k==8 and not match: 
      #Lists are mutable unlike strings and tuples.
      allTweetsContentNew_1.append(allTweetsContent[j]) 
   
allTweetsContent = allTweetsContentNew_1      
# Replace allTweetsContent with allTweetsContentNew
allTweetsContent = allTweetsContentNew
print(f"Length of the list of tweets after second filter: {len(allTweetsContent)}")


# -- Third filter: -- Remove the pattern 'of PRO who'
# -- Suggested approach: -- Create another loop, and another conditional statement using a regular expression from the list you got from the previous filter. 
#    This time, save only those that DO NOT match the conditional statement. Print the length of the list.
NEWallTweetsContentNew = copy.copy(allTweetsContent)

for i in pronouns:
  for j in range(len(allTweetsContent)):
    m = re.search(r'of\s' + i + r'\s+(W|w)ho',allTweetsContent[j])
    if type(m) == re.Match:
      try:
        NEWallTweetsContentNew.remove(allTweetsContent[j])
      except ValueError: #There was one specific tweet that caused an error, and we couldn't figure out why, so we decided to just skip it.
        pass
    else:
      continue
allTweetsContent = NEWallTweetsContentNew
print(f"Length of the list of tweets after third filter: {len(allTweetsContent)}")



# -- Fourth filter: -- Remove tweets where the pronoun 'it' preceeds the word 'who' by 2-4 words
# -- Suggested approach: -- Write a regular expression that picks out this pattern. Using the list you generated from the previous filter
#    use create a loop with a conditional statement that removes this pattern. Print the length of the list.
forth_filtered = []
for t in allTweetsContent:
    if re.search(r'\sit(\s+\S+){1,3}\swho\s', t) != None:
         continue
    else:
        forth_filtered += [t]
#print(forth_filtered)
print(f"Length of the list of tweets after fourth filter: {len(forth_filtered)}")



# -- Fifth filter: -- Remove tweets where 'PRO who' is preceded by the verbs 'ask', 'tell', 'wonder', 'inform', and 'show'.
# -- Suggested approach: --  Save the verbs above into a list. Create a loop that iterates through your pronoun list from above
#    and removes examples that contain the pattern '[element-from-verb-list] [element-from-PRO-list]'. Print the length of the list.
verbs = ['ask', 'tell', 'wonder', 'inform', 'show']
pronoun_list = ['me', 'you', 'him', 'her', 'it'] #仮に
fifth_filtered = []

for t in forth_filtered:
    if re.search(r'\s(ask|tell|wonder|inform|show)\s(me|you|him|her|it|us|them)\swho\s' , t) != None:
        continue
    else:
        fifth_filtered += [t]

#filter1(fifth_filtered) ←Colin's function (used in filter1) 
#↓ this is temmporary code. when Colin made the filter1 code, it will replace the codes below.
dict2 = {}
count = 0
for k in fifth_filtered:
    dict2[k] = dict2.get(k, 0) + 1

fifth_filtered = list(dict2.keys())

#print(fifth_filtered)
print(f"Length of the list of tweets after fifth filter: {len(fifth_filtered)}")

# output your list as a .csv or .tsv file.



# === Part 2: Uniqueness ===

# -- Instruction: -- You now need to find out whether the tweets you have left are "literary" or "non-literary", according to CTK's classification. 
# I've written a bit of this for you. Modify the block of code below so that it runs with your variable names. 
# You should replace 'tweetList' in the 'for' block with your variable name that holds the final filtered list of 'PRO who' tweets.

# Test variable: contains a short list of test utterances for the pattern "who <word1> <word2>"
tweetList = ['this is a quote: he who shall not be named', 'who among us really', 'jeff is wondering who sings', 
            'he who shall not be named again', 'but who among us is perfect']

# This evaluates each tweet in TweetList for whether it contains the specified regex search
# and whether that regex pattern in a tweet matches exactly to any other tweet in the list. 
# If it does, it is assigned a value True. If it doesn't, it's assigned a value False.
trueFalseList = []
for tweet in tweetList:
  whoPhrase = re.search("who \w+ \w+", tweet)
  if whoPhrase is None:
      trueFalseList.append(False)
  else:
      trueFalseList.append(any(whoPhrase.group(0) in t for t in tweetList))
print(trueFalseList)

# The following takes our two lists, tweetList and trueFalseList, and zips them together. 
# It then creates a dataframe out of this list, that can then be converted to a .csv file

annotatedTweetList = list(zip(tweetList, trueFalseList))
tweetDataframe = pandas.DataFrame(annotatedTweetList)
tweetDataframe.to_csv('literary-annotated-tweets.csv', header=["Tweets", "isLiterary"], index=False)


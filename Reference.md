'''
Temporary reference file for handy notes and tricks that I learn while developing
'''
#Use Pandas MultiIndex
http://pandas.pydata.org/pandas-docs/stable/advanced.html

#Level Indexing
Use df.xs(index_name, level) to index dataframe

#Updating dataframe with new values
Use Dataframe.update to update in place. Works with multiindex which is handy. Overwrites by default
import sys, ast
from datetime import datetime
import numpy
import matplotlib.pylab as plt
import calendar
plt.style.use('classic')

############################################################################################
#introduction information
############################################################################################
if sys.argv[1]: #can define which questions to answer
    question = sys.argv[1]
else:
    question = None

fname = "Posts.xml" #input('What is the file name? ')#sys.argv[1]


############################################################################################
#defined functions 
############################################################################################

##################Setup functions##################

#this function output all the possible keys of the data. It could be run once and the output could be dumped to a file. 
def get_keys(input_file_name): #get the unique keys from your file. some lines have different keys than others, but we want the full list.
    file = open('%s'%input_file_name, encoding = "utf-8")   
    #head = [next(file) for x in range(3)]
    keys = []
    for line in file:
        dic = string_to_dictionary(line)
        keys =  numpy.unique( numpy.append( keys, numpy.array( list( dic.keys() ) ) ) ) #saves unique keys only
    print(keys)
    return keys

#This function will need to change dependin on the format of the incoming data.
def string_to_dictionary(input_str):
    raw_dic = input_str.split('<')[1].split('>')[0].replace('=', '').replace(' ', '').split('"')#massage the data by cutting the end <> off and the = signs through. then splitting the string by " divides it into all entries
    dic = dict(zip(raw_dic[::2], raw_dic[1::2]))#group the odd and even entries into dictionaries.
    return dic

##################set functions##################

#This function converts Date parameters from strings to datetime.
def set_datetime(par):
    dtime = datetime.strptime(par, "%Y-%m-%d %H:%M:%S.%f")
    return dtime

def set_type(key, objects):
    if "Date" in key:
        for idx, i in enumerate(objects):
            objects[idx] = set_datetime(i)
    elif ("Id" or "Count" or "Score") in key:
        for idx, i in enumerate(objects):
            objects[idx] = int(i)
    else:
        print('none')
    return objects

##################conditions##################

#Condtition of parameter between values.
def condition_between(dic, count, key, constraints):
    if (dic.get(key) > constraints[0]) and (dic.get(key) < constraints[1]):
        count += 1
    return count

#Condtition of parameter equal to value.
def condition_equal(dic, count, key, constraints):
    if dic.get(key) == constraints[0]:
        count += 1
    return count

#Condtition of parameter less than value.
def condition_lessthan(dic, count, key, constraints):
    if dic.get(key) < constraints[0]:
        count += 1
    return count

#Condtition of parameter greater then value.
def condition_greaterthan(dic, count, key, constraints):
    if dic.get(key) > constraints[0]:
        count += 1
    return count

#Condtition of values within a parameter.
def condition_contained(dic, count, key, constraints ):
    if constraints[0] in dic.get(key):
        count += 1
    return count

#Condtition of values within a parameter, excluding a value.
def condition_contained_exluding(dic, count, key, constraints ):
    if constraints[0] in dic.get(key) and constraints[1] not in dic.get(key):
        count += 1
    return count

##################run functions##################

def get_counts(input_file_name, key=None, condition=None, constraints = None): 
    file = open('%s'%input_file_name, encoding = "utf-8")#FIXME Could make 'encoding' a parameter also.
    count = 0
    head = [next(file) for x in range(350)] #for testing purposes.
    contraints = set_type(key, constraints)
    for line in file:
        dic = string_to_dictionary(line)#convert the string of the line to a dictionary.

        #only if key exists.
        if dic.get(key):

            #If the key has date in the name, convert to datetime. If it is an Id, Count or Score, set as integer. Otherwise leave as string.
            if "Date" in key:
                dic[key] = set_datetime(dic.get(key).replace('T', ' '))
            elif ("Id" or "Count" or "Score") in key:
                dic[key] = int(dic[key])

            #conditions.
            if condition == "between":
                count = condition_between(dic, count, key, constraints)
            elif condition == "contained":
                count = condition_contained(dic, count, key, constraints)
            elif condition == "contained excluding":
                count = condition_contained_exluding(dic, count, key, constraints)
            else:
                count += 1 # with no conditions, count all lines.
                
    return count


def get_hists(input_file_name, key = None, constraints = None, key2 = None):
    file = open('%s'%input_file_name, encoding = "utf-8")#FIXME Could make 'encoding' a parameter also.
    count = 0
    head = [next(file) for x in range(10000)] #for testing purposes.
    hist = []
    for line in file:
        dic = string_to_dictionary(line)#convert the string of the line to a dictionary.
        #only if key exists.
        if dic.get(key):
            #If the key has date in the name, convert to datetime. If it is an Id, Count or Score, set as integer. Otherwise leave as string.
            if "Date" in key:
                dic[key] = set_datetime(dic.get(key).replace('T', ' '))
            elif ("Id" or "Count" or "Score") in key:
                dic[key] = int(dic[key])
            #If the key has date in the name, convert to datetime. If it is an Id, Count or Score, set as integer. Otherwise leave as string.
            if "Date" in key2:
                dic[key2] = set_datetime(dic.get(key2).replace('T', ' '))
            elif ("Id" or "Count" or "Score") in key2:
                dic[key2] = int(dic[key2])

            #Append the month
            if constraints[0] in dic.get(key):
                hist.append(dic[key2].month)
    return hist

def get_time_series(input_file_name, key = None, constraints = None):
    file = open('%s'%input_file_name, encoding = "utf-8")#FIXME Could make 'encoding' a parameter also.
    count = 0
    dat = []
    t = []
    head = [next(file) for x in range(100000)] #for testing purposes.
    for line in file:
        dic = string_to_dictionary(line)#convert the string of the line to a dictionary.
        #only if key exists.
        if dic.get(key):
            #If the key has date in the name, convert to datetime. If it is an Id, Count or Score, set as integer. Otherwise leave as string.
            if "Date" in key:
                dic[key] = set_datetime(dic.get(key).replace('T', ' '))
            elif ("Id" or "Count" or "Score") in key:
                dic[key] = int(dic[key])

            #The other key always needed is CreationDate    
            dic['CreationDate'] = set_datetime(dic.get('CreationDate').replace('T', ' '))

            if constraints[0] in dic.get(key):
                t.append(dic.get('CreationDate'))
                count += 1
                dat.append(count)
            else:
                t.append(dic.get('CreationDate'))
                dat.append(count)
    tseries = numpy.vstack([t, dat])
    return tseries


############################################################################################
#run commands
############################################################################################

if question == "1":
    count = get_counts(fname, key = "CreationDate", condition = "between", constraints = ["2016-06-01 00:00:00.00", "2016-07-01 00:00:00.00"] ) 
    print("The number of posts made in June 2016 was", count)
    
if question == "2":
    count = get_counts(fname, key = "Tags", condition = "contained", constraints = ["combinatorics"])
    print("The number of posts containing the tag 'cominatorics' is", count)

if question == "2a":
    count = get_counts(fname, key = "Tags", condition = "contained excluding", constraints = ["combinatorics", "fibonacci-numbers"])
    print("The number of posts containing the tag 'combinatorics' exluding 'fibonacci-numbers'", count) 

if question == "3":
    hist = get_hists(fname, key = "Tags", constraints = ["graph-theory"], key2 = "CreationDate")
    mybins = list(numpy.arange(0.5, 13.5, 1))
    arr = plt.hist(hist, bins = mybins, align='mid', rwidth = 1)
    for i in range(12):
        plt.text(arr[1][i],arr[0][i],str(int(arr[0][i])))
    plt.xlim([0.5,12.5])
    plt.xticks(numpy.arange(1, 13, 1), ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec') )
    plt.savefig('graphtheory_hist.pdf')
    print("The month which was the most popular for posts tagged 'graph-theory' was", calendar.month_name[numpy.argmax(arr[0])+1] )

if question == "4":
    tdata = get_time_series(fname, key = "Tags", constraints = ["graph-theory"])
    plt.plot(numpy.sort(tdata[0]), tdata[1])
    plt.savefig('graphtheory_timeseries.pdf')
    
#keys = get_keys(fname)


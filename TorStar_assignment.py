import sys, ast
from datetime import datetime
from datetime import timedelta
import numpy
from matplotlib import rc
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import calendar
#some formatting for matplotlib
plt.style.use('classic')
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']}, size = 15)
rc('text', usetex=True)

############################################################################################
#introduction information
############################################################################################
if len(sys.argv) > 1: #can define which questions to answer
    question = sys.argv[1]
else:
    question = None

fname = "Posts.xml" #input('What is the file name? ')#sys.argv[1]


############################################################################################
#defined functions 
############################################################################################

####################################Setup functions####################################

#This function outputs all the possible keys of the data. It could be run once and the output could be dumped to a file. 
def get_keys(input_file_name): #get the unique keys from your file. some lines have different keys than others, but we want the full list.
    file = open('%s'%input_file_name, encoding = "utf-8")   
    #head = [next(file) for x in range(3)]
    keys = []
    for line in file:
        dic = string_to_dictionary(line)
        keys =  numpy.unique( numpy.append( keys, numpy.array( list( dic.keys() ) ) ) ) #saves unique keys only
    print(keys)
    return keys

#This function will need to change depending on the format of the incoming data.
def string_to_dictionary(input_str):
    raw_dic = input_str.split('<')[1].split('>')[0].replace('=', '').replace(' ', '').split('"')#massage the data by cutting the end <> off and the = signs through. then splitting the string by " divides it into all entries
    dic = dict(zip(raw_dic[::2], raw_dic[1::2]))#group the odd and even entries into dictionaries.
    return dic

####################################set functions####################################

#This function converts Date parameters from to datetime.
def set_datetime(par):
    dtime = datetime.strptime(par, "%Y-%m-%d %H:%M:%S.%f")
    return dtime

#This function assigns a type to each parameter based on the key.
def set_constraint_type(key, var):
    if "Date" in key: #if it is a Date, convert to datetime
        for idx, i in enumerate(var):
            var[idx] = set_datetime(i)
    elif ("Id" or "Count" or "Score") in key:#if it is any of these, convert to integer
        for idx, i in enumerate(var):
            var[idx] = int(i)
    else: #else leave as string
        for idx, i in enumerate(var):
            var[idx] = i 
    return var

####################################conditions functions####################################

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

####################################functions####################################

def get_counts(input_file_name, key=None, condition=None, constraints = None, test = False): 
    file = open('%s'%input_file_name, encoding = "utf-8") #FIXME Could make 'encoding' a parameter also.
    count = 0
    if test: #for testing purposes.
        print('THIS IS TEST MODE')
        file = [next(file) for x in range(10000)]
    contraints = set_constraint_type(key, constraints) #the constraints come in a string. this will convert them appropriately.
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
            if condition == "between":#the condition is an input to this function
                count = condition_between(dic, count, key, constraints)
            elif condition == "contained":
                count = condition_contained(dic, count, key, constraints)
            elif condition == "contained excluding":
                count = condition_contained_exluding(dic, count, key, constraints)
            else:
                count += 1 # with no conditions, count all lines.
                
    return count


def get_hists(input_file_name, key = None, constraints = None, key2 = None, test = False):
    file = open('%s'%input_file_name, encoding = "utf-8") #FIXME Could make 'encoding' a parameter also.
    count = 0
    hist = []
    if test:#for testing purposes.
        print('THIS IS TEST MODE')
        file = [next(file) for x in range(100000)] 
    for line in file:
        dic = string_to_dictionary(line)#convert the string of the line to a dictionary.
        
        #only if key exists. Always have to check this because not all lines in the file contain all keys.
        if dic.get(key):
            #If the key has date in the name, convert to datetime. If it is an Id, Count or Score, set as integer. Otherwise leave as string.
            if "Date" in key:
                dic[key] = set_datetime(dic.get(key).replace('T', ' '))
            elif ("Id" or "Count" or "Score") in key:
                dic[key] = int(dic[key])
            if "Date" in key2:
                dic[key2] = set_datetime(dic.get(key2).replace('T', ' '))
            elif ("Id" or "Count" or "Score") in key2:
                dic[key2] = int(dic[key2])

            #Append the month to the histogram
            if constraints[0] in dic.get(key):
                hist.append(dic[key2].month)
    return hist #returns a list of all months.

def get_time_series(input_file_name, key = None, constraints = None, test = False):
    file = open('%s'%input_file_name, encoding = "utf-8") #FIXME Could make 'encoding' a parameter also.
    count = 0
    dat = []
    t = []
    if test: #for testing purposes.
        print('THIS IS TEST MODE')
        file = [next(file) for x in range(100000)] 
    for line in file:
        dic = string_to_dictionary(line) #convert the string of the line to a dictionary.
        
        #only if key exists.
        if dic.get(key):
            #If the key has date in the name, convert to datetime. If it is an Id, Count or Score, set as integer. Otherwise leave as string.
            if "Date" in key:
                dic[key] = set_datetime(dic.get(key).replace('T', ' '))
            elif ("Id" or "Count" or "Score") in key:
                dic[key] = int(dic[key])

            #The other key always needed is CreationDate for this time series.   
            dic['CreationDate'] = set_datetime(dic.get('CreationDate').replace('T', ' '))

            if constraints[0] in dic.get(key): 
                t.append(dic.get('CreationDate'))
                count += 1
                dat.append(count)
            else:
                t.append(dic.get('CreationDate'))
                dat.append(count)
    tseries = numpy.vstack([t, dat])  
    return tseries #returns an array containing the time and the accumulated count 


############################################################################################
#run commands
############################################################################################

#keys = get_keys(fname) #this is not needed for anything other than to look at the available keys in the file.

test = False # make this true to test code. It will only go through a portion of the file, not the entire thing.


if question == "1": #runs get_counts with input parameters.
    count = get_counts(fname, key = "CreationDate", condition = "between", constraints = ["2016-06-01 00:00:00.00", "2016-07-01 00:00:00.00"], test = test ) #returns the count according to the conditions.
    print("The number of posts made in June 2016 was", count)
    
if question == "2":#runs get_counts with input parameters.
    count = get_counts(fname, key = "Tags", condition = "contained", constraints = ["combinatorics"], test = test )#returns the count according to the conditions.
    print("The number of posts containing the tag 'cominatorics' is", count)

if question == "2a":#runs get_counts with input parameters.
    count = get_counts(fname, key = "Tags", condition = "contained excluding", constraints = ["combinatorics", "fibonacci-numbers"], test = test )#returns the count according to the conditions.
    print("The number of posts containing the tag 'combinatorics' exluding 'fibonacci-numbers'", count) 

if question == "3": #runs get_hists with input parameters.
    hist = get_hists(fname, key = "Tags", constraints = ["graph-theory"], key2 = "CreationDate", test = test )#gets just a list
    mybins = list(numpy.arange(0.5, 13.5, 1)) #define bins centered on numbers of the months.
    arr = plt.hist(hist, bins = mybins, align='mid', rwidth = 1) #creates the histogram with my bins and the list `hist'. aligns them in the middle with width 1
    for i in range(12):#plotting the number above each bar
        plt.text(arr[1][i]+0.15,arr[0][i]+0.2,str(int(arr[0][i])))
    plt.title(r'Posts with Tags containing ``graph-theory" sorted by Month')
    plt.ylabel(r'Number of posts')
    plt.xlabel(r'Month') 
    plt.xlim([0.5,12.5])
    plt.xticks(numpy.arange(1, 13, 1), ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec') ) #labels each bin by the month. I made the hist with month number instead of datetime, becasue it would not be in the correct calendar order otherwise.
    plt.savefig('graphtheory_hist.pdf') #save figure
    print("The month which was the most popular for posts tagged 'graph-theory' was", calendar.month_name[numpy.argmax(arr[0])+1] )
    print("See the histogram 'graphtheory_hist.pdf' ")
          
if question == "4":#runs get_time_series with input parameters.
    tdata = get_time_series(fname, key = "Tags", constraints = ["graph-theory"], test = test )#returns a numpy array of time and the accumulated count given conditions.
    plt.figure(figsize=(10, 5))#set custom figurre size. Width is 2 times the height.
    plt.plot(numpy.sort(tdata[0]), tdata[1]) #plots time, and the dat
    minyear = tdata[0][0].year
    maxyear = tdata[0][-1].year
    for i in numpy.arange(minyear, maxyear+1, 1):
        plt.axvline(set_datetime(str(i)+"-01-01 00:00:00.00"), color='grey', alpha = 0.5, linestyle='--', label = '%s'%i)
    plt.title(r'Posts with Tags containing ``graph-theory"')
    plt.xlabel(r'Time')
    plt.ylabel(r'Number of Posts')
    dt = (tdata[0][-1] - tdata[0][0])/5 #defines the distance between times on the x axis.
    plt.xticks([tdata[0][0], tdata[0][0] + dt, tdata[0][0] +2*dt, tdata[0][0] +3*dt, tdata[0][0] +4*dt, tdata[0][0] +5*dt])#Sets the times for x axis.
    plt.savefig('graphtheory_timeseries.pdf')#save figure
    print("See the plot 'graphtheory_timeseries.pdf' ")

if not question:
    print('Please type "1", "2", "2a", "3" or "4" after "TorStar_assignment.py" to choose the question you would like answered.')


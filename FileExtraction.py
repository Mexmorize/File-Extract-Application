# time      - import package to be able to track run times
# os        - import package to help with file path management
# csv       - import package to act on csv files
# json      - import package to act on json files
# pprint    - import package for dictionary printing
# math      - import package for math methods
# datetime  - import package for date and time handling
import time, os, csv, json, pprint, math, collections, datetime

# Create extraction function
def FileExtraction(fileName):
    
    # Start the timer and store it in a variable
    startTime = time.time()
    
    # Get file path of the file parameter
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    
    # Find and store the file path/name in variable, userFile
    userFile = os.path.join(THIS_FOLDER, fileName)
    
    # Gets the file type, to distinguish .csv versus .json
    fileType = os.path.splitext(fileName)[1]
    
    # Create the empty dictionary to store all persons (row) information in
    dictList = []
    
    # Create an ordered dictionary to store the months of a year
    monthDict = collections.OrderedDict({'January':0, 'February':0, 'March':0, 
                                         'April':0, 'May':0, 'June':0, 'July':0, 
                                         'August':0, 'September':0, 'October':0, 
                                         'November':0, 'December':0})
    
    # Initiates the variable to hold the total number of siblings
    totalSiblings = 0
    
    # Initiates the variable to count all the favourite foods
    favFoods = collections.Counter()
    
    if fileType == '.csv':
        # Opens .csv file and uses the reader along with the delimiter for data
        data = csv.DictReader(open(userFile), delimiter=',')
            
    elif fileType == '.json':
        # Opens .json file and loads the data
        data = json.load(open(userFile))
        
    # Iterates through each row in the data
    for row in data:
        
        # used for debugging and testing
        # pprint.pprint(row)
        
        # ///////////////////////// SIBLINGS //////////////////////////////////
        # Appends the information into the dictionary for use
        dictList.append(row)
        
        # Adds each person's (row) sibling count to the total count
        totalSiblings += int(row['siblings'])
        
        # ///////////////////////// FAVOURITE FOODS ///////////////////////////
        # Formats the name of the favourite_food and stores it in foodItem
        foodItem = row['favourite_food'].strip().capitalize()
        
        # Adds the unique food item to the counter and adds 1 to value
        favFoods[foodItem] += 1
        
        # ///////////////////////// BIRTH MONTHS //////////////////////////////
        # Stores the time stamp integer value in a variable
        timeStamp = int(row['birth_timestamp'])/1000

        # Store the birth_timezone as a HH:MM variable
        timeZone = datetime.datetime.strptime(row['birth_timezone'], '%z')
        
        # Create a datetime.timezone class and store it
        timeA = datetime.timezone(datetime.datetime.utcoffset(timeZone))
        
        # Store the final (adjusted) datetime
        finalTime = datetime.datetime.fromtimestamp(timeStamp, timeA)
        
        # Formats out the month from the final calendar datetime
        birthMonth = finalTime.strftime('%B')

        # Add a count for the found birth month
        monthDict[birthMonth] += 1
    
    # Store the top 3 food items
    topFoods = favFoods.most_common(3)
        
    # Divides the total person count by the number of siblings to get average
    # Uses the math.ceil() to force the decimal number to round up
    averageSiblings = math.ceil(totalSiblings / len(dictList))
    
    # ////////////////////////// FINAL RESULTS ////////////////////////////////
    
    # Prints the header line for the results
    print('------------------------------------')
    
    # Prints the average number of siblings to the user
    print('Average siblings: %i \n' % averageSiblings)
    
    # For each food item in the list of most common foods, print new line
    for food in topFoods:
        
        # Prints the information from food in topFoods
        print('- {:<10} {:>6}'.format(food[0], food[1]))
        
    # Prints the header for the Birth Months
    print('\nBirths per month:\n')
    
    # Iterate through each month in the dictionary that had at leasy 1 birth
    for birthMonth in monthDict:
        
        # Print the month and the number of births in that month
        print('- {:<10} {:>6}'.format(birthMonth, monthDict[birthMonth]))
    
    # ///////////////////////////// TESTING ///////////////////////////////////
        
    # Prints the runtime for the program
    print("\n--- %s seconds ---" % (time.time() - startTime))
   
# Stores all the test file names as veriables for quick testing
x = 'population_sample.csv'
y = 'population_sample.json'
z = 'population.csv'
u = 'population.json'

# Calls the function with the file name as the parameter (.csv or .json)
FileExtraction(x)
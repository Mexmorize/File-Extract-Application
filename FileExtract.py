# sys           - import package to get system input as arguments
# time          - import package to be able to track run times
# os            - import package to help with file path management
# csv           - import package to act on csv files
# json          - import package to act on json files
# pprint        - import package for dictionary printing
# math          - import package for math methods
# collections   - import package to use counter
# datetime      - import package for date and time handling
# concurrent    - import package for threading
import sys, time, os, csv, json, pprint, math, collections, datetime, concurrent.futures, pathlib

'''
Functionality: 
    Extract data from a file into a list
Parameters:
    file - A String name of a file
Returns:
    dataList - A List of the data contained in the file
'''    
def get_data(userFile):
    
    # Create the empty dictionary to store all persons (row) information in
    dataList = []

    theFile = pathlib.Path.cwd() / userFile

    # Gets the file type, to distinguish .csv versus .json
    fileType = os.path.splitext(theFile)[1]
    
    if fileType == '.csv':
        # Opens .csv file and uses the reader along with the delimiter for data
        data = csv.DictReader(open(theFile), delimiter=',')
                
    elif fileType == '.json':
        # Opens .json file and loads the data
        data = json.load(open(theFile))
        
    else:
        raise UnboundLocalError('Error: Improper file type')
        
    for row in data:
        
        # used for debugging and testing
        # pprint.pprint(row)

        # Appends the information into the dictionary for use
        dataList.append(row)
        
    return dataList

'''
Functionality: 
    Get the average number of siblings from the file data
Parameters:
    allData - A List of the data contained in the file
Returns:
    averageSiblings - An Integer of the average number of siblings from the data
'''   
def get_siblings(allData):
    
    # Initiates the variable to hold the total number of siblings
    totalSiblings = 0
    
    # Iterates through each row in the data
    for row in allData:
        
        # Converts the string of the number of siblings into an integer
        numOfSiblings = int(row['siblings'])
        
        # If the number of siblings isn't negative ...
        # Adds each person's (row) sibling count to the total count
        if numOfSiblings >= 0:
            totalSiblings += numOfSiblings
        
    # Divides the total person count by the number of siblings to get average
    # Uses the math.ceil() to force the decimal number to round up
    averageSiblings = math.ceil(totalSiblings / len(allData))
        
    return averageSiblings

'''
Functionality: 
    Get the top three favourite foods from the data
Parameters:
    allData - A List of the data contained in the file
Returns:
    topFoods - A List of the top three most common favourite foods in the data
'''   
def get_fav_foods(allData):
    
    # Initiates the variable to count all the favourite foods
    favFoods = collections.Counter()
        
    for row in allData:
    
        # Formats the name of the favourite_food and stores it in foodItem
        foodItem = row['favourite_food'].strip().capitalize()
        
        # Adds the unique food item to the counter and adds 1 to value
        favFoods[foodItem] += 1
        
     # Store the top 3 food items
    topFoods = favFoods.most_common(3)
    
    return topFoods

'''
Functionality: 
    Tabulates all the birth months from the timestamps in the data, taking into
    account the timezone differences
Parameters:
    allData - A List of the data contained in the file
Returns:
    monthDict - A Dictionary of each month along with their respective birth counts
'''   
def get_birth_months(allData):
    
    # Create an ordered dictionary to store the months of a year
    monthDict = collections.OrderedDict({'January':0, 'February':0, 'March':0, 
                                     'April':0, 'May':0, 'June':0, 'July':0, 
                                     'August':0, 'September':0, 'October':0, 
                                     'November':0, 'December':0})
    
    for row in allData:
        
        # Stores the time stamp integer value in a variable
        timeStamp = int(row['birth_timestamp'])/1000

        # Store the birth_timezone as a HH:MM variable
        timeZone = datetime.datetime.strptime(row['birth_timezone'].replace(':',''), '%z')
        
        # Create a datetime.timezone class and store it
        timeA = datetime.timezone(datetime.datetime.utcoffset(timeZone))
        
        # Store the final (adjusted) datetime
        finalTime = datetime.datetime.fromtimestamp(timeStamp, timeA)
        
        # Formats out the month from the final calendar datetime
        birthMonth = finalTime.strftime('%B')

        # Add a count for the found birth month
        monthDict[birthMonth] += 1
        
    return monthDict

''' //////////////////////////// FINAL RESULTS /////////////////////////////'''

# Executes this file if requested by the terminal
if __name__ == '__main__':
    
    # Start the timer and store it in a variable
    startTime = time.time()

    #fileData = get_data(dataFolder / sys.argv[1])
    fileData = get_data(sys.argv[1])

    # Utilize threading through the concurrent.futures module
    with concurrent.futures.ThreadPoolExecutor() as executor:
        
        # The threading for getting the average siblings
        futureAvgSiblings = executor.submit(get_siblings, fileData)
        avgSiblings = futureAvgSiblings.result()
        
        # The threading for getting the most popular foods
        futurePopularFoods = executor.submit(get_fav_foods, fileData)
        popularFoods = futurePopularFoods.result()
        
        # The threading for getting the months of birth
        futureBirthMonths = executor.submit(get_birth_months, fileData)
        birthMonths = futureBirthMonths.result()
    
    # Prints the header line for the results
    print('------------------------------------')
    
    # Prints the average number of siblings to the user
    print('Average siblings: %i \n' % avgSiblings)
    
    # Prints the header for the favourite foods list
    print('Favourite foods:\n')
    
    # For each food item in the list of most common foods, print new line
    for food in popularFoods:
        
        # Prints the information from food in topFoods
        print('- {:<10} {:>6}'.format(food[0], food[1]))
        
    # Prints the header for the Birth Months
    print('\nBirths per month:\n')
    
    # Iterate through each month in the dictionary
    for month in birthMonths:
        
        # Print the month and the number of births in that month
        print('- {:<10} {:>6}'.format(month, birthMonths[month]))
    
    # Prints the runtime for the program
    # The estimated runtime for the program is O(logN)
    print("\n--- %s seconds ---" % (time.time() - startTime))
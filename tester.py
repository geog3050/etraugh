
import assignment2
import os
import csv


# Tests the functions of assignment2 using the data given in a csv
# Prints results to console
def testFile(csv_file):
    # These will change depending on testing and be displayed in the end.
    import_test = "Passed"
    fight_test = "Passed"
    tournament_test = "Passed"

    # WIll contain list of all participants from the csv file
    participants = []
    
    try:
        participants = assignment2.import_data(csv_file) # Run import data on csv
    except:
        import_test = "Failed" # If execution fails, update import_test string
   
    try:
        assignment2.fight(participants[0], participants[1], 1) # Runs fight using first 2 participants
    except:
        fight_test = "Failed" # If execution fails, update fight_test string
     
    try:
        assignment2.tournament(participants) # Runs tournmanet function
    except:
        tournament_test = "Failed" # If execution fails, update tournament_test string

    # Print successes and failures to console
    print("For CSV File: " + csv_file)
    print("import_data: " + import_test)
    print("fight: "+ fight_test)
    print("tournament: " + tournament_test)


# Runs testFile on every csv file in a given folder
def testFolder(folder):
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        # checking if it is a file
        if os.path.isfile(f):
            testFile(f) # Run test using current csv

def testAccuracy(solution_file):
    with open(solution_file, 'r') as csvfile:
    # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # Getting participants from csv into correct format
        raw_participants = ",".join(next(csvreader))
        participants = eval(raw_participants)
        
        # Getting solution from csv into correct format
        raw_solution = ",".join(next(csvreader))
        solution = eval(raw_solution)

        # If the assignment2 tournament function returns the same results as the solution, print passed
        if(assignment2.tournament(participants) == solution):
            print("Accuracy Test: Passed")
        else:
            print("Accuracy Test: Failed")
    
# Given a directory of pokemon csv files, and a solution rubric, test the execution
# and accuracy of assignment2 code
def testAssignment(dir, solution):
    testFolder(dir) # See if every function executes for given csv files
    testAccuracy(solution) # See if function 


#folder = "C:/Users/Ethan/Documents/GeospatialProgramming/Quiz5/testdata_assignment2"
#file = "C:/Users/Ethan/Documents/GeospatialProgramming/Quiz5/testdata_assignment2/test1.txt"
#solution = "C:/Users/Ethan/Documents/GeospatialProgramming/Quiz5/solution_test1.txt"
# testFolder(folder)
# testAccuracy(solution)
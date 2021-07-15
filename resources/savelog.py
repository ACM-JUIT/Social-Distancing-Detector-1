# importing libraries and required files
import csv
from datetime import datetime,date
from os import path

#Function adds to log in csv file
#Takes in argument as number of violates violates
def addtolog(violations):
    #If files already exists it appends to the csv
    if path.exists('violationlog.csv') :
        with open('violationlog.csv', mode='a') as csv_file:
            fieldnames = ['Date', 'Time', 'Voilations']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            #Gets current Date and Time
            time = datetime.now()
            current_time = time.strftime("%H:%M:%S")
            today = date.today()
            dates = today.strftime("%B %d, %Y")

            #Writes Date Time and number of violates to file
            writer.writerow({'Date': dates, 'Time': current_time, 'Voilations': violations})
    #If file doesnt exist create and add headings and first data
    else:
        with open('violationlog.csv', mode='w') as csv_file:
            fieldnames = ['Date', 'Time', 'Voilations']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            #Gets current Date and Time
            time = datetime.now()
            current_time = time.strftime("%H:%M:%S")
            today = date.today()
            dates = today.strftime("%B %d, %Y")

            #Creates headings for each coloumn
            writer.writeheader()

            #Writes first data
            writer.writerow({'Date': dates, 'Time': current_time, 'Voilations': violations})

"""
 ============================================================================
 Name: Ryan Russell
 UVicID: V00873387
 Created: Nov. 12th, 2017
 Last Updated: Nov. 16th, 2017
 Assignment: SENG 265 Assignment 3 Part B
 File name: ferry_delays.py
 Description: This interactive program calculates ferry delays from CSV
 files containing BC ferries schedule data, prompts user input and 
 displays the desired data about ferry delays for a specific month. 
 ============================================================================
 """

import csv
import sys
import os

# NOTE: I understand the complications that can occur by using global variables and 
# would normally never use any. In this case, I was (before changing it for this version) making
# assumptions about the file name and needed to get the month from one of the columns of the 
# csv file, but couldn't return two values from the delay_calculator function, so I believe that
# using global variable was required to avoid completely changing my implementation.
month = ""  

# The delay_calculator function takes an input file and the name of the terminal for which the user
# wants delay statistics, then reads specific columns of the csv file that pertain to the scheduled
# and actual departure time. It then calculates the delay for a specific ship, sums all of the delays
# and divides that delay by the total number of ships that departed from the specified terminal,
# rounding and returning the average delay 
def delay_calculator(file, terminal):

	global month   # Initializing the global variable month for the delay_calculator function

	# These are float variables that are used to calculate the average delay below
	scheduled_time = 0.0
	actual_time = 0.0
	delay = 0.0
	delay_sum = 0.0
	ships_sailed = 0.0
	average_delay = 0.0

	reader = csv.DictReader(file)
	for row in reader:
		month = row["scheduled_departure_month"]
		if row["departure_terminal"] == terminal:
			scheduled_time = ((float(row["scheduled_departure_hour"]) * 60.0) + float(row["scheduled_departure_minute"]))
			actual_time = ((float(row["actual_departure_hour"]) * 60.0) + float(row["actual_departure_minute"]))
			delay = actual_time - scheduled_time
			delay_sum += delay
			ships_sailed = ships_sailed + 1.0

	average_delay = delay_sum / ships_sailed
	average_delay = '{0:.2f}'.format(average_delay)
	return average_delay
	

def main():

	global month         # Initializing the global variable month for the main function
	terminal = ""        # A string to hold the name of the terminal
	data = []            # A list to contain the months for which we have accumulated data
	avg_printed = False  # A boolean value declaring whether or not the avg has been printed for the given input

	# A list of 3-letter abbreviations and integer values representing the months of the year
	months = ["June", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "July"] 
	int_months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

	# Lets the user know about the option to quit at any point
	print("\nThis program will calculate the average ferry delay from Tsawwassen and Swartz Bay.")
	print("You may enter \"q\" at any time to quit the program.\n")

	# An infinite loop until "q" is inputted by the user
	while True:

		# Prompts user input for the terminal which the average delay should be calculated for
		terminal_input = input("Would you like to calculate delay statistics for Tsawwassen (t) or Swartz Bay (s): ")
		
		if terminal_input == "t":
			print("Delay statistics for the Tsawwassen terminal will be calculated.\n")
			terminal = "Tsawwassen"

		elif terminal_input == "s":
			print("Delay statistics for the Swartz Bay terminal will be calculated.\n")
			terminal = "Swartz Bay"

		elif terminal_input == "q":
			print("Quit has been selected. The program will now end.")
			break

		else:
			print("Input is invalid. Please enter your selection again.\n")
			continue

		while True:

			# Prompts user input for the month which the average delay should be calculated for
			month_input = input("For which month would you like to calculate average delay statistics (enter a number from 1 to 12): ")

			if month_input == "q":
				print("Quit has been selected. The program will now end.")
				break

			# If the input for the month is valid, open the csv files, calculate the average delay, and check
			# the month located within the file. If that month matches the user inputted month: print the 
			# average delay in formatted output. If there is no data: tell the user there is no data 
			elif month_input in int_months:
					for argument in sys.argv:
						if '.csv' in argument:
								if os.path.exists(argument):
									with open(argument, "r") as csv_file:
										avg_delay = delay_calculator(csv_file, terminal)
										if int(month) == int(month_input):
											print("\nRESULTS")
											print(terminal + ":")
											print("    Average delay for " + months[int(month_input)] + ": " + str(avg_delay))
											print("END\n")
											avg_printed = True
					if avg_printed == False:
						print("\nRESULTS")
						print(terminal + ":")
						print("    No delay data for " + months[int(month_input)])
						print("END\n")
					avg_printed = False

			else:
				print("Input is invalid. Please enter your selection again.\n")
				continue   # Reprompt the month question

			break   # Return to the first prompt

		if month_input == "q":
			break   # Completely exit the program


if __name__ == "__main__":
	main()
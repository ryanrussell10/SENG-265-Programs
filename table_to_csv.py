"""
 ============================================================================
 Name: Ryan Russell
 UVicID: V00873387
 Created: Nov. 20th, 2017
 Last Updated: Nov. 27th, 2017
 Assignment: SENG 265 Assignment 4
 File name: table_to_csv.py
 Description: This program reads HTML tables from standard input and 
 outputs a CSV representation of each table in the input.
 ============================================================================
 """

import sys
import re

def main():

		if sys.stdin.isatty():
			print("There is no input.")
			return

		html_input = sys.stdin.read()               # Read from stdin and store in a string
		html_input = html_input.replace("\n", " ")  # Replace newlines with spaces

		csv_row = []        # A list to store each row that will be output to csv format
		max_row_length = 0  # An int to to store the max. row length
		num_commas = 0      # An int to store the number of commas that need to be printed

		# This regex matches all table tags in the html input
		table_regex = "<table[\s]*[^><]*>([\W\w]*?)</table[\s]*>"
		all_tables = re.findall(table_regex, html_input, re.IGNORECASE)

		# This regex matches all row tags in the html input
		row_regex = "<tr[\s]*[^><]*>([\W\w]*?)</tr[\s]*>"

		# These regexes match all header and data tags in the html input
		header_regex = "<th[\s]*[^><]*>([\W\w]*?)</th[\s]*>"
		data_regex = "<td[\s]*[^><]*>([\W\w]*?)</td[\s]*>"

		# Look through every table in the html input and print the TABLE number
		for index, table in enumerate(all_tables):

			print("TABLE " + str(index + 1) + ":")

			# Find every row in the table and look through each row for the data (or header data) 
			# in each column. If there are headers, add them to a list of the row contents and
			# check if additional commas need to be added. If there are no headers, perform the
			# same process with the data cells. Finally, print the formatted csv output.
			rows = re.findall(row_regex, table, re.IGNORECASE)
			for row in rows:

				# Finds all the occurences of header and data tags in the row
				headers = re.findall(header_regex, row, re.IGNORECASE)
				cells = re.findall(data_regex, row, re.IGNORECASE)

				if len(headers) > 0:
					for header in headers:
						csv_row.append(" ".join(header.split()))
					if len(headers) < max_row_length:
						num_commas = max_row_length - len(headers)

				elif len(cells) > 0:
					for cell in cells:
						csv_row.append(" ".join(cell.split()))
					if len(cells) < max_row_length:
						num_commas = max_row_length - len(cells)

				else:
					# No data in this row, only print the commas
					print("," * (max_row_length - 1))

				# Print the formatted csv output
				print(",".join(csv_row) + ("," * num_commas))

				# Checks to see if the current row has the greatest length in the table
				if len(csv_row) > max_row_length:
					max_row_length = len(csv_row)

				csv_row = []    # Clears the csv_row list
				num_commas = 0  # Clears the num_commas int

			print()  # Prints a newline character so there is a line between each table
			max_row_length = 0  # Clears the max_row_length int for a new table


if __name__ == "__main__":
	main() 
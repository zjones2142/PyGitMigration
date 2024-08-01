import csv
"""This file can be useful to organize the csv output files in case of clutter.

Note: This code does NOT remove the old csv file.
You will need to delete it manually if desired
"""
def filter_csv(input_csv, output_csv, allowed_list):
  """
  Filters a CSV file, keeping only rows where the first column value is in the allowed_items list.

  Args:
    input_csv: The path to the input CSV file.
    output_csv: The path to the output CSV file.
    allowed_items: A list of strings representing allowed items (case-insensitive).
  """

  allowed_items = [item.lower() for item in allowed_list]

  with open(input_csv, 'r', newline='') as infile, open(output_csv, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write the header row to the output file
    header = next(reader)
    writer.writerow(header)

    readerList = []
    for row in reader:
      readerList.extend(str(row))

    for item in readerList:
      if item.lower() in allowed_items:
        writer.writerow(item)

if __name__ == "__main__":
  input_file = "FILEPATH"
  output_file = "FILEPATH"
  allowedString = ""
  allowed_list = allowedString.split(',')
  filter_csv(input_file, output_file, allowed_list)
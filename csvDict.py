import csv

header = ['TYPE', 'TOTAL', 'OUT', 'AVL', 'RATE']
values = [['hourly', '50', '0', '50', '5'],
          ['daily', '70', '0', '70', '20'],
          ['weekly', '40', '0', '40', '60']]

filename = "inventory.csv"

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(values)
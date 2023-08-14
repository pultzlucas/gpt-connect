import pandas as pd
import glob
import sys

all_csvs_arr = []
path = sys.argv[1]
for file in glob.glob(f'{path}/*.csv'):
    with open(file, 'r', encoding='utf8') as csv:
        csv_arr = [line.split('@') for line in csv.read().split('\n')]
        all_csvs_arr.extend(csv_arr)
with open('result.csv', 'w', encoding='utf8') as result:
    result.write('\n'.join(['@'.join(line) for line in all_csvs_arr]))
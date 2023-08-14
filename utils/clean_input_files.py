import os

path = '../data/input'

for file in os.listdir(path):
    filename = file.replace('_processing_', '')
    os.rename(f'{path}/{file}', f'{path}/{filename}')
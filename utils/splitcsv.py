import os

def split_csv_file(path, n):
    with open(path, 'r', encoding='utf-8') as f:
        input_lines = f.read().split('\n')
    count_files = 0
    for i in range(len(input_lines)):
        if i % n == 0:
            content = '\n'.join(input_lines[i:i+n]).strip()
            if content != "":
                open(f'{os.path.splitext(path)[0]}_chunk_{count_files + 1}.csv', 'w', encoding='utf-8').write(content)
                count_files += 1
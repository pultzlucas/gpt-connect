import os

class CsvController():
    def __init__(self):
        self.input_files = self.get_files_to_process()

    def get_files_to_process(self):
        files = []
        for f in os.listdir('data/input'):
            if os.path.isfile(os.path.join('data/input', f)):
                if not '_processing' in f:
                    files.append(f)
        return files

    def extract_input_file(self):
        if len(self.input_files) == 0:
            return None
        first_file = self.input_files[0]
        self.input_files.remove(first_file)
        return first_file

    def get_csv(self, uid):
        self.input_files = self.get_files_to_process()
        filename = self.extract_input_file()
        input_dir = 'data/input/'
        
        if not filename:
            return {
                'filename': None,
                'data': None
            }
        
        filerename = filename.replace('.csv', f'_processing_{uid}.csv')
        os.rename(f'{input_dir}{filename}', f'{input_dir}{filerename}')

        with open(f'{input_dir}{filerename}', 'r', encoding='utf-8') as f:
            csv = f.read()

        return {
            'filename': filename,
            'data': csv
        }

    def receive_csv(self, csv, params):
        filename = params['filename']
        uid = params['uid']

        if filename is None:
            return {
                'stored': False,
                'error': 'filename must be informed'
            }
        
        if csv.decode('utf-8') == '':
            return {
                'stored': False,
                'error': 'csv data cannot be empty'
            }
        
        filerename = filename.replace('.csv', f'_processing_{uid}.csv')
        if os.path.exists(f'data/input/{filerename}'): 
            os.remove(f'data/input/{filerename}')
            
        with open(f'data/output/result_{filename}', 'wb') as w:
            writed = w.write(csv)
            return {
                'stored': bool(writed)
            }
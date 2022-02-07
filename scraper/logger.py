from datetime import datetime


class AutoRiaScrapLogger:
    def __init__(self, folder, ):
        self.file_path = f"{folder}/log.txt"
        self.f = open(self.file_path, "a+")

    def add_header(self, search_url):
        time = datetime.now()
        self.f.write(f'*****{time.strftime("%m/%d/%YT%H:%M:%S")} - SEARCH_URI:{search_url};\n')

    def add_page_read_log(self, page, item_count):
        time = datetime.now()
        self.f.write(f'    {time.strftime("%m/%d/%YT%H:%M:%S")} - PAGE:{page};COUNT:{item_count};\n')

    def add_file_save_log(self, file, item_count):
        time = datetime.now()
        self.f.write(f'    {time.strftime("%m/%d/%YT%H:%M:%S")} - FILENAME:{file};COUNT:{item_count};\n')

    def close(self):
        self.f.close()

import os
from datetime import datetime
from shutil import copyfile
import logging

output_dir = 'scrapers/output/'

FILE_SYSTEM_AVAILABLE = True

def save_response_body(response_body, name='unknown', folder='unknown', status=None):
    if FILE_SYSTEM_AVAILABLE:
        file_path = 'scrapers/html_responses/' + folder + '/' + name
        if status:
            file_path += "(" + str(status) + ")"
        file_path += '.html'

        if not os.path.exists(file_path):  # todo: this should actually be checked before starting request
            with open(file_path, 'wb') as f:
                f.write(response_body)

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_problematic_page(response):
    url_final_part = response.url.split('/')[-1]
    url_final_part_without_params = url_final_part.split('?')[0]
    logging.info(f'Saving {response.url} as {url_final_part_without_params}')
    save_response_body(response.body, url_final_part_without_params, 'errors', status=response.status)


def delete_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


def allocate_output_path(spider_name):
    today = datetime.now().strftime('%m-%d %Hh%M')
    path = f'{output_dir}{spider_name} {today}.json'
    return path


def overwrite_main_file(spider_name, current_output_file):
    copyfile(current_output_file, f'{output_dir}{spider_name}.json')


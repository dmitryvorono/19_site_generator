import os
import sys
import json
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader


def load_config(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def render_index_page(templates_folder, templates_filename, config):
    env = Environment(loader=FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    index_template = env.get_template(templates_filename)
    index_template.render(topics=config['topics'], articles=config['articles'])
    with open(templates_filename, 'w') as file_handler:
        file_handler.write(index_template.render(topics=config['topics'], articles=config['articles']))


if __name__ == '__main__':
    config = load_config('config.json')
    render_index_page('templates', 'index.html', config)

import os
import sys
import json
import errno
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from markdown import markdown
import urllib


def load_config_json(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return file_handler.read()


def get_jinja_template(templates_folder, templates_filename):
    jinja_env = Environment(loader=FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    return jinja_env.get_template(templates_filename)


def render_index_page(jinja_template, config, output='index.html'):
    with open(output, 'w') as file_handler:
        file_handler.write(jinja_template.render(topics=config['topics'], articles=config['articles']))


def convert_markdown_to_html(markdown_filepath):
    markdown_text = load_data(markdown_filepath)
    return markdown(markdown_text)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def render_article_page(jinja_template, article, content, output):
    mkdir_p(os.path.dirname(output))
    print(output)
    with open(output, 'w') as file_handler:
        file_handler.write(jinja_template.render(article=article, content=content))


def encode_to_url(string):
    return urllib.parse.quote(string)


def render_articles(jinja_template, articles, articles_folder):
    for article in articles:
        path_to_article = ''.join([articles_folder, '/', article['source']])
        html = convert_markdown_to_html(path_to_article)
        output = ''.join([article['source'][0:-2], 'html'])
        render_article_page(jinja_template, article, html, output)
        article['html'] = encode_to_url(output)


if __name__ == '__main__':
    templates_folder = 'templates'
    config = load_config_json('config.json')
    index_template = get_jinja_template(templates_folder, 'index.html')
    article_template = get_jinja_template(templates_folder, 'article.html')
    render_articles(article_template, config['articles'], 'articles')
    render_index_page(index_template, config)

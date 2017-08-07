import os
import json
import errno
from jinja2 import Environment, FileSystemLoader
from markdown import markdown
import urllib
from livereload import Server


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


def load_jinja_templates(templates_folder):
    jinja_env = Environment(loader=FileSystemLoader(templates_folder),
                            trim_blocks=True,
                            lstrip_blocks=True)
    jinja_env
    with os.scandir(templates_folder) as folder_iterator:
        return {entry.name: jinja_env.get_template(entry.name)
                for entry in folder_iterator if entry.is_file()}


def render_index_page(jinja_template, config, output='index.html'):
    with open(output, 'w') as file_handler:
        file_handler.write(jinja_template.render(topics=config['topics'],
                                                 articles=config['articles']))


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
    with open(output, 'w') as file_handler:
        file_handler.write(jinja_template.render(article=article,
                                                 content=content))




def render_articles(jinja_template, articles, articles_folder):
    for article in articles:
        path_to_article = ''.join([articles_folder, '/', article['source']])
        html = convert_markdown_to_html(path_to_article)
        output = ''.join([article['source'][:-2], 'html'])
        render_article_page(jinja_template, article, html, output)
        article['url'] = output


def make_site():
    templates_folder = 'templates'
    articles_folder = 'articles'
    config = load_config_json('config.json')
    jinja_templates = load_jinja_templates(templates_folder)
    render_articles(jinja_templates['article.html'],
                    config['articles'],
                    articles_folder)
    render_index_page(jinja_templates['index.html'], config)


if __name__ == '__main__':
    server = Server()
    server.watch('templates/*.html', make_site)
    server.watch('articles/**/*.md', make_site)
    server.serve(root='.')

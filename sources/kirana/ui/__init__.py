# All Python Built-in Imports Here.
import os

# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.
IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'images').replace('\\', '/')
STYLESHEETS_PATH = os.path.join(os.path.dirname(__file__), 'stylesheets').replace('\\', '/')


def get_stylesheet(stylesheet_name):
    if not stylesheet_name.endswith('.css'):
        stylesheet_name = f'{stylesheet_name}.css'

    full_path = os.path.join(STYLESHEETS_PATH, stylesheet_name)
    with open(full_path, 'r') as stream:
        css = stream.read()
        return css.replace('<image_dir>/', f'{IMAGES_PATH}/')


if __name__ == '__main__':
    pass

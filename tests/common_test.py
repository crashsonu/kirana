import os
from kirana.ui import IMAGES_PATH

icon_file = os.path.join(IMAGES_PATH, 'add.png')
print(icon_file)
print(os.path.exists(icon_file))

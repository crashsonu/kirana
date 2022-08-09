import os
from kirana.ui import IMAGES_PATH

icon_file = os.path.join(IMAGES_PATH, 'add.png')
print(icon_file)
print(os.path.exists(icon_file))

# def del_check_items_lw(self, lw_name, items_indexes):
#     items_to_remove = list()
#     for i in items_indexes:
#         item = self.cat_lw.item(i)
#         if item:
#             items_to_remove.append(item)

# print(items_to_remove)
# for i in range(lw_name.count()):
#     list_item = lw_name.item(i)
#     print(list_item)
#     if list_item in items_to_remove:
#         print(list_item)
#         item_row = lw_name.row(list_item)
#         print(item_row)
#         lw_name.takeItem(item_row)
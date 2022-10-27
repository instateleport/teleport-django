# import sqlite3
# from .models import CustomUser
#
#
# db = sqlite3.connect('db.sqlite3')
# a = db.execute('SELECT * FROM `users_customuser`').fetchall()
# keys = ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'email', 'verification_uuid', 'avatar', 'promocode_id']
# for x in a:
#     dict_ = {}
#     for v, k in zip(x, keys):
#         if v == 0:
#             v = False
#         elif v == 1 and k != 'id':
#             v = True
#         if k == 'id':
#             try:
#                 us = CustomUser.objects.get(id=v)
#                 us.delete()
#                 continue
#             except CustomUser.DoesNotExist:
#                 continue
#         dict_[k] = v
#     user = CustomUser(**dict_)
#     try:
#         user.save()
#     except Exception as e:
#         print(e)
#     print(user)
from django.db.models import Q

from apps.users.models import CustomUser
from apps.subscribe_pages.models import BGColor


default_bg_color = BGColor.get_default_bg_color()


for user in CustomUser.objects.all():
    # page_list = user.subscribe_pages.all().filter(Q(is_active=False) | Q(bg_color=None))
    # for page in page_list:
    #     update_fields = []
    #     print(page)
    #     if user.pocket.balance > 0:
    #         if not page.is_active:
    #             print('page is not active ', user.pocket.balance, ' R.')
    #             page.is_active = True
    #             update_fields.append('is_active')
    #
    #     if not page.bg_color:
    #         print('page HAS NOT BG_COLOR')
    #         page.bg_color = default_bg_color
    #         update_fields.append('bg_color')
    #     print(update_fields)
    #
    #     page.save(update_fields=update_fields)

    group_list = user.group_of_pages.filter(name__contains='/')
    for group in group_list:
        group.name = group.name.replace('/', ' ')
        group.save(update_fields=['name'])

    # group_list = user.group_of_pages.all()
    # print(group_list)
    # group_length = len(group_list)
    # accum = 0
    # print(group_length)
    # for group in group_list:
    #     if accum == group_length:
    #         continue
    #     group.delete()
    #     accum += 1

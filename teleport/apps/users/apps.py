from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = 'Пользователи'

    # def ready(self):
    #     from .models import CustomUser, GroupOfSubscribePage
    #
    #     for user in CustomUser.objects.filter(group_of_pages__isnull=True):
    #
    #
    #         try:
    #             GroupOfSubscribePage.objects.get_or_create(
    #                user=user,
    #                name='Неотсортированные',
    #                can_delete=False
    #             )
    #         except GroupOfSubscribePage.MultipleObjectsReturned:
    #             pass

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

# local imports
from . import views

app_name = 'subscribe_pages'

router = routers.DefaultRouter()
router.register(r'vk-subscribe-pages', views.VKSubscribePageViewSet)
router.register(r'vk-subscribers', views.VKSubscriberViewSet)

urlpatterns = [
    # API
    path('api/v1/', include(router.urls)),
    path('api/v1/vk-subscribe-pages-statistic/',
         views.VKStatisticAPIView.as_view()),

    # domains
    path('domains/', views.DomainCreateListView.as_view(), name='domain-list'),
    path('domains/delete/', views.DomainDeleteAjaxView.as_view(),
         name='domain-delete'),
    path('domains/insctuctions/',
         views.DomainInstructionTemplateView.as_view(),
         name='domain-instruction'),

    # ig folders
    path('folders/create/', views.FolderCreateView.as_view(),
         name='folder-create'),
    path('folders/delete/', views.FolderDeleteAjaxView.as_view(),
         name='folder-delete'),
    path('folders/rename/', views.FolderRenameView.as_view(),
         name='folder-rename'),
    path('folder/append/', views.AddToFolderView.as_view(),
         name='add-to-folder'),

    path('tg-subscribe-pages/', views.TGSubscribePageListView.as_view(),
         name='tg-page-list'),
    path('tg-subscribe-pages/<str:name>/', views.TGSubscribePageListView.as_view(),
         name='tg-page-list'),
    path('tg-folders/create/', views.TGFolderCreateView.as_view(),
         name='tg-folder-create'),

    # ig instagram pages - crud
    path('subscribe-pages/', views.InstagramSubscribePageListView.as_view(),
         name='page-list'),
    path('subscribe-pages/<str:name>/', views.InstagramSubscribePageListView.as_view(),
         name='page-list'),

    path('subscribe-page/create/', views.SubscribePageCreateView.as_view(),
         name='page-create'),
    path('subscribe-page/create/slug-check/',
         views.SubscribePageCreateSlugCheckAjaxView.as_view(),
         name='page-create-slug_check'),

    path('subscribe-page/delete/', views.SubscribePageDeleteView.as_view(),
         name='page-delete'),

    path('subscribe-page/<slug:slug>/',
         views.SubscribePageDetailView.as_view(), name='page-detail'),
    path('subscribe-page/<slug:slug>/slug-check/',
         views.SubscribePageDetailSlugCheckAjaxView.as_view(),
         name='page-detail-slug_check'),

    path('subscribe-page/<slug:slug>/duplicate/',
         views.SubscribePageDuplicateView.as_view(), name='page-duplicate'),
    path('subscribe-page/<slug:slug>/statistic/',
         views.StatisticSubscribePageDetailView.as_view(),
         name='page-statistic'),
    path('subscribe-page/<slug:slug>/statistic/get-statistic/',
         views.StatisticAjaxView.as_view(),
         name='ajax-page-statistic'),
    path('subscribe-page/<slug:slug>/statistic/download-subscribers/',
         views.StatisticSubscribePageDownloadSubscribers.as_view(),
         name='page-statistic-download-subscribers'),
    path('subscribe-page/<slug:slug>/statistic/search-subscribers/',
         views.SearchSubscribersAjaxView.as_view(),
         name='page-statistic-search-subscribers'),

    # ig subscribe pages
    path('page/<slug:slug>/', views.SubscribePageOpenView.as_view(),
         name='page-open'),
    path('page/<slug:slug>/subscribe/',
         views.SubscribePageGetMaterials.as_view(), name='page-get_material'),
    path('page/<slug:slug>/subscribe/check-subscribe/',
         views.SubscribePageAjaxCheckUsername.as_view(),
         name='ajax-check'),
    path('page/<slug:slug>/success/', views.SubscribePageSuccessView.as_view(),
         name='success'),

    # vk folders
    path('vk-folders/create/', views.VKFolderCreateView.as_view(),
         name='vk-folder-create'),
    path('vk-folders/delete/', views.VKFolderDeleteAjaxView.as_view(),
         name='vk-folder-delete'),
    path('vk-folders/rename/', views.VKFolderRenameView.as_view(),
         name='vk-folder-rename'),
    path('vk-folder/append/', views.AddToVKFolderView.as_view(),
         name='vk-add-to-folder'),

    # vk subscribe pages - crud
    path('vk-subscribe-pages/', views.VKSubscribePageListView.as_view(),
         name='vk-page-list'),
    path('vk-subscribe-pages/<str:name>/',
         views.VKSubscribePageListView.as_view(),
         name='vk-page-list'),

    path('vk-subscribe-page/create/',
         views.VKSubscribePageCreateView.as_view(),
         name='vk-page-create'),
    path('vk-subscribe-page/create/slug-check/',
         views.VKSubscribePageCreateSlugCheckAjaxView.as_view(),
         name='vk-page-create-slug_check'),

    path('vk-subscribe-page/delete/',
         views.VKSubscribePageDeleteView.as_view(),
         name='vk-page-delete'),

    path('vk-subscribe-page/<slug:slug>/',
         views.VKSubscribePageDetailView.as_view(), name='vk-page-detail'),
    path('vk-subscribe-page/<slug:slug>/slug-check/',
         views.VKSubscribePageDetailSlugCheckAjaxView.as_view(),
         name='vk-page-detail-slug_check'),

    path('vk-subscribe-page/<slug:slug>/duplicate/',
         views.VKSubscribePageDuplicateView.as_view(),
         name='vk-page-duplicate'),
    path('vk-subscribe-page/<slug:slug>/statistic/',
         views.VKStatisticSubscribePageDetailView.as_view(),
         name='vk-page-statistic'),
    path('vk-subscribe-page/<slug:slug>/statistic/get-statistic/',
         views.VKStatisticAjaxView.as_view(),
         name='vk-ajax-page-statistic'),
    path('vk-subscribe-page/<slug:slug>/statistic/download-subscribers/',
         views.VKStatisticSubscribePageDownloadSubscribers.as_view(),
         name='vk-page-statistic-download-subscribers'),
    path('vk-subscribe-page/<slug:slug>/statistic/search-subscribers/',
         views.VKSearchSubscribersAjaxView.as_view(),
         name='vk-page-statistic-search-subscribers'),


    #telegram bot
    path('api/v1/telegram-page/present/<str:channel_id>/',
         views.GetPresentFromTelegramPageView.as_view()),
    path('api/v1/telegram-page/subscriber/',
         views.AddTelegramUserToChannelSubscribers.as_view())
]

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path(
        'tg-subscribe-pages/',
        views.TGSubscribePageListView.as_view(),
        name='tg-page-list'
    ),
    path(
        'tg-subscribe-pages/<str:name>/',
        views.TGSubscribePageListView.as_view(),
        name='tg-page-list'
    ),
    path(
        'tg-folders/create/',
        views.TGFolderCreateView.as_view(),
        name='tg-folder-create'
    ),
    path(
        'tg-folders/delete/',
        views.TGFolderDeleteAjaxView.as_view(),
        name='tg-folder-delete'
    ),
    path(
        'tg-folders/rename/',
        views.TGFolderRenameView.as_view(),
        name='tg-folder-rename'
    ),
    path(
        'tg-folder/append/',
        views.TGAddToFolderView.as_view(),
        name='add-to-folder'
    ),

    path(
        'tg-subscribe-page/create/',
        views.TGSubscribePageCreateView.as_view(),
        name='tg-page-create'
    ),
    path(
        'tg-subscribe-page/delete/',
        views.TGSubscribePageDeleteView.as_view(),
        name='page-delete'
    ),
    path(
        'tg-subscribe-page/<slug:slug>/duplicate/',
        views.TGSubscribePageDuplicateView.as_view(), 
        name='tg-page-duplicate'
    ),
    path(
        'tg-subscribe-page/<slug:slug>/',
        views.TGSubscribePageDetailView.as_view(),
        name='tg-page-detail'
    ),
    path(
        'tg-subscribe-page/<slug:slug>/statistic/',
        views.TGStatisticSubscribePageDetailView.as_view(),
        name='tg-page-statistic'
    ),
    path(
        'tg-subscribe-page/<slug:slug>/statistic/get-tg-statistic/',
        views.TGStatisticAjaxView.as_view(),
        name='tg-ajax-page-statistic'
    ),
    path(
        'tg-subscribe-page/<slug:slug>/statistic/download-tg-subscribers/',
        views.TGStatisticSubscribePageDownloadSubscribers.as_view(),
        name='tg-page-statistic-download-subscribers'
    ),
    path(
        'tg-page/<slug:slug>/',
        views.TGSubscribePageOpenView.as_view(),
        name='tg-page-open'
    ),
]

if settings.DEBUG:
     if settings.MEDIA_ROOT:
          urlpatterns += static(
               settings.MEDIA_URL,
               document_root=settings.MEDIA_ROOT
          )
          urlpatterns += static(
               settings.STATIC_URL,
               document_root=settings.STATIC_ROOT
          )

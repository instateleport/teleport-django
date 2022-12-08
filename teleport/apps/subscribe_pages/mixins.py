from django.shortcuts import render
from django.views.generic import DeleteView
from django.http import Http404
from django.http.response import HttpResponse

import json


class IsSubscribePageActive:
    def dispatch(self, request, *args, **kwargs):

        self.object = self.get_object()

        if not self.object.is_active:
            if self.object.user == request.user or self.object.user.is_staff:
                return render(request,
                              'subscribe_pages/page-out_of_balance.html')
            raise Http404('Активная страница не найдена')
        return super().dispatch(request, *args, **kwargs)


class IsSubscribePageOwner:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            page = self.get_object(
                self.model.objects.filter(user=request.user))
            if not page:
                raise Http404
        return super().dispatch(request, *args, **kwargs)


class AjaxMixin:
    response = {}

    def get_ajax_response(self, **kwargs) -> dict:
        self.response.update({**kwargs})
        return self.response.copy()

    def ajax_response(self, data: dict, **kwargs):
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", **kwargs)


class DeleteAjaxMixin(DeleteView, AjaxMixin):
    model = None
    http_method_names = ['post']
    id_field_name = 'objectID'
    is_owner = False

    def get_object(self, object_id: int):
        query_kwargs = {'id': object_id}

        if self.is_owner:
            query_kwargs['user'] = self.request.user

        try:
            obj = self.model.objects.get(**query_kwargs)
        except self.model.DoesNotExist:
            obj = None
        return obj

    def delete(self, request, *args, **kwargs):
        response = self.get_ajax_response()
        data = request.POST
        object_id = int(data.get(self.id_field_name, 0))

        self.object = self.get_object(object_id)

        if self.object:
            self.object.delete()
            response['status'] = 'SUCCESS'
        else:
            response['status'] = 'ERROR'
            response['reason'] = 'OBJECT_NOT_FOUND'
        return self.ajax_response(response)

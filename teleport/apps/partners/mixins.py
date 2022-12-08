from django.http import Http404


class IsChannelOwner:
    def dispatch(self, request, *args, **kwargs):
        channel = self.get_object(self.model.objects.filter(partner__referrer=request.user))
        if not channel:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

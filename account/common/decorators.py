from django.http import HttpResponseBadRequest

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not requet.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **args)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

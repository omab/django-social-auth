from django.http import HttpResponseRedirect


def username(request, *args, **kwargs):
    if kwargs.get('user'):
        username = kwargs['user'].username
    else:
        username = request.session.get('saved_username')
    return { 'username': username }


def redirect_to_form(*args, **kwargs):
    if not kwargs['request'].session.get('saved_username') and kwargs.get('user') is None:
        return HttpResponseRedirect('/form/')

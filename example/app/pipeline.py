from django.http import HttpResponseRedirect


def redirect_to_form(strategy, user=None, *args, **kwargs):
    if not strategy.session_get('saved_username') and user is None:
        return HttpResponseRedirect('/form/')


def username(strategy, user=None, *args, **kwargs):
    if user:
        username = user.username
    else:
        username = strategy.session_get('saved_username')
    return {'username': username}


def redirect_to_form2(strategy, *args, **kwargs):
    if strategy.session_get('saved_first_name'):
        return HttpResponseRedirect('/form2/')


def first_name(strategy, *args, **kwargs):
    if strategy.session_get('saved_first_name'):
        user = kwargs['user']
        user.first_name = strategy.session_get('saved_first_name')
        user.save()

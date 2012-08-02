# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, logout
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from social_auth.views import complete

SANDBOX_URL = 'http://api-sandbox.odnoklassniki.ru:8088/sandbox/protected/application/launch.do?appId={0:s}&userId=0'
class OdnoklassnikiInfo(TemplateView):
    template_name = 'odnoklassniki_info.html'
    
    def get(self, *args, **kwargs):
        if hasattr(settings, 'ODNOKLASSNIKI_APP_ID'):
            return redirect(SANDBOX_URL.format(settings.ODNOKLASSNIKI_APP_ID))
        else:
            return super(OdnoklassnikiInfo, self).get(*args, **kwargs)
    
ok_app_info = OdnoklassnikiInfo.as_view()

class OdnoklassnikiApp(TemplateView):
    template_name = 'odnoklassniki.html'
    
    def get(self, request, *args, **kwargs):
        result = None
        if request.GET.get('apiconnection', None):
            if request.user.is_authenticated() and 'OdnoklassnikiAppBackend' not in request.session.get(BACKEND_SESSION_KEY, ''):
                logout(request)
            result = complete(request, 'odnoklassnikiapp')
        if isinstance(result, HttpResponse):
            return result
        else:
            if not request.user.is_authenticated() or 'OdnoklassnikiAppBackend' not in request.session.get(BACKEND_SESSION_KEY, ''):
                request.user = AnonymousUser()
        
        context = self.get_context_data(params=kwargs)
        return self.render_to_response(context)
    
ok_app = OdnoklassnikiApp.as_view()
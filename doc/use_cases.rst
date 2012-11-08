Use Cases
=========

Some particular use cases are listed below.

1. Use social auth just for account association (no login)::

    from django.contrib.auth.decorators import login_required

    from social_auth.views import auth, complete, disconnect

    urlpatterns += patterns('',
        url(r'^associate/(?P<backend>[^/]+)/$',
            login_required(auth),
            name='socialauth_begin'),
        url(r'^associate/complete/(?P<backend>[^/]+)/$',
            login_required(complete),
            name='socialauth_complete'),

        url(r'^disconnect/(?P<backend>[^/]+)/$',
            disconnect,
            name='socialauth_disconnect'),
        url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$',
            disconnect,
            name='socialauth_disconnect_individual'),
    )

2. Include a similar snippet in your page to make BrowserID_ work::

    <!-- Include BrowserID JavaScript -->
    <script src="https://browserid.org/include.js" type="text/javascript"></script>

    <!-- Define a form to send the POST data -->
    <form method="post" action="{% url socialauth_complete "browserid" %}">
        <input type="hidden" name="assertion" value="" />
        <a rel="nofollow" id="browserid" href="#">BrowserID</a>
    </form>

    <!-- Setup click handler that retieves BrowserID assertion code and sends
         POST data -->
    <script type="text/javascript">
        $(function () {
            $('#browserid').click(function (e) {
                e.preventDefault();
                var self = $(this);

                navigator.id.get(function (assertion) {
                    if (assertion) {
                        self.parent('form')
                                .find('input[type=hidden]')
                                    .attr('value', assertion)
                                    .end()
                                .submit();
                    } else {
                        alert('Some error occurred');
                    }
                });
            });
        });
    </script>


3. Integration with client side authorization libraries

   OAuth providers like Facebook provide some form of Javascript library/SDK to
   perform client side authorization. That authorization can be stored using
   django-social-auth by defining a simple view like this::

    from django.contrib.auth import login
    from django.shortcuts import redirect
    from social_auth.decorators import dsa_view

    @dsa_view()
    def register_by_access_token(request, backend, *args, **kwargs):
        access_token = request.GET.get('access_token')
        user = backend.do_auth(access_token)
        if user and user.is_active:
            login(request, user)
        return redirect('/')

   This view just expect the ``access_token`` as a GET parameter and the
   backend name in the URL (check django-social-auth URLs).

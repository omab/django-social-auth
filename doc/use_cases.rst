Use Cases
=========

Some particular use cases are listed below.

1. Use social auth just for account association (no login)::

    urlpatterns += patterns('',
        url(r'^associate/(?P<backend>[^/]+)/$', associate,
            name='socialauth_associate_begin'),
        url(r'^associate/complete/(?P<backend>[^/]+)/$', associate_complete,
            name='socialauth_associate_complete'),
        url(r'^disconnect/(?P<backend>[^/]+)/$', disconnect,
            name='socialauth_disconnect'),
        url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$',
            disconnect, name='socialauth_disconnect_individual'),
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

---------
BrowserID
---------
Support for BrowserId_ is possible by posting the ``assertion`` code to
``/complete/browserid/`` URL.

The setup doesn't need any setting, just the usual BrowserId_ javascript
include in your document and the needed mechanism to trigger the POST to
`django-social-auth`_.

Include a similar snippet in your page to make BrowserId_ work::

    <!-- Include BrowserID JavaScript -->
    <script src="https://browserid.org/include.js" type="text/javascript"></script>

    <!-- Define a form to send the POST data -->
    <form method="post" action="{% url 'socialauth_complete' "browserid" %}">
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

.. _django-social-auth: https://github.com/omab/django-social-auth
.. _BrowserId: https://browserid.org

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import Template, Context, RequestContext


def home(request):
    return HttpResponse(Template(
    """
    <html>
      <head>
        <title>Social access</title>
      </head>
      <body>
        <h1>Login using any of the following methods:</h1>
        <div style="padding-left: 30px;">
          <div>
            <h2>Login using <a href="http://oauth.net/">OAuth</a> from:</h2>
            <ul>
              <li><a href="/login/twitter/">Twitter</a></li>
              <li><a href="/login/facebook/">Facebook</a></li>
            </ul>
          </div>
          <div>
            <h2>Login using <a href="http://openid.net/">OpenId</a> from:</h2>
            <ul>
              <li><a href="/login/google/">Google</a></li>
              <li><a href="/login/yahoo/">Yahoo</a></li>
              <li>
                <form action="/login/openid/" method="post">{% csrf_token %}
                  <label for="openid_identifier">Other provider:</label>
                  <input id="openid_identifier" type="text" value="" name="openid_identifier" />
                  <input type="submit" />
                </form>
              </li>
            </ul>
          </div>
        </div>
      </body>
    </html>
    """).render(Context(RequestContext(request))),
    content_type='text/html;charset=UTF-8')

@login_required
def done(request):
    user = request.user
    return HttpResponse(Template(
    """
    <html>
      <head>
        <title>Logged in</title>
        <style>th{text-align: left;}</style>
      </head>
      <body>
        <h1>Logged in!</h1>
        <table>
          <tr><th>Id:</th> <td>{{ user.id }}</td></tr>
          <tr><th>Username:</th> <td>{{ user.username }}</td></tr>
          <tr><th>Email:</th> <td>{{ user.email|default:"Not provided" }}</td></tr>
          <tr><th>First name:</th> <td>{{ user.first_name|default:"Not provided" }}</td></tr>
          <tr><th>Last name:</th> <td>{{ user.last_name|default:"Not provided" }}</td></tr>
        </table>
        <p><a href="/logout/">Logout</a></p>
      </body>
    </html>
    """).render(Context({'user':user})),
    content_type='text/html;charset=UTF-8')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

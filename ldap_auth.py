import os

from flask import Flask, request, Response

import ldap

app = Flask(__name__)

AUTH_MESSAGE = os.getenv(
    'AUTH_MESSAGE',
    'Unable to authenticate with current credentials'
)
LDAP_SERVER = os.getenv('LDAP_SERVER', 'ldap://localhost:389')
REALM = os.getenv('REAML', 'Login Required')


def ldap_authenticate(user_dn, user_pw):
    success = False
    try:
        l = ldap.initialize(LDAP_SERVER)
    except Exception as e:
        print(e)
        return False

    try:
        l.bind_s(user_dn, user_pw)
    except (ldap.INVALID_CREDENTIALS, ldap.LDAPError) as e:
        pass
    else:
        success = True

    l.unbind()

    return success


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        AUTH_MESSAGE, 401, {
            'WWW-Authenticate': 'Basic realm="{}"'.format(REALM)
        }
    )


@app.route("/<user_dn>")
def auth(user_dn):
    authr = request.authorization
    if authr is None:
        return authenticate()

    user_dn = user_dn.format(username=authr.username)
    if ldap_authenticate(user_dn, authr.password):
        return Response('', 204)

    return authenticate()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

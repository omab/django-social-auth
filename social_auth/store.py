import time
import base64

from openid.association import Association as OIDAssociation
from openid.store.interface import OpenIDStore
from openid.store.nonce import SKEW

from .models import Association, Nonce


class DjangoOpenIDStore(OpenIDStore):
    def __init__(self):
        self.max_nonce_age = 6 * 60 * 60 # Six hours

    def storeAssociation(self, server_url, association):
        args = {'server_url': server_url, 'handle': association.handle}
        try:
            assoc = Association.objects.get(**args)
        except Association.DoesNotExist:
            assoc = Association(**args)
        assoc.secret = base64.encodestring(association.secret)
        assoc.issued = association.issued
        assoc.lifetime = association.lifetime
        assoc.assoc_type = association.assoc_type
        assoc.save()

    def getAssociation(self, server_url, handle=None):
        args = {'server_url': server_url}
        if handle is not None:
            args['handle'] = handle

        associations, expired = [], []
        for assoc in Association.objects.filter(**args):
            association = OIDAssociation(assoc.handle,
                                         base64.decodestring(assoc.secret),
                                         assoc.issued,
                                         assoc.lifetime,
                                         assoc.assoc_type)
            if association.getExpiresIn() == 0:
                expired.append(assoc.id)
            else:
                associations.append(association)

        if expired: # clear expired associations
            Association.objects.filter(pk__in=expired).delete()

        if associations:
            associations.sort(key=lambda x: x.issued, reverse=True)
            return associations[0]

    def useNonce(self, server_url, timestamp, salt):
        if abs(timestamp - time.time()) > SKEW:
            return False
        nonce, created = Nonce.objects.get_or_create(server_url=server_url,
                                                     timestamp=timestamp,
                                                     salt=salt)
        return created

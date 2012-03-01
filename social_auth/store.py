"""OpenId storage that saves to django models"""
import time
import base64

from openid.association import Association as OIDAssociation
from openid.store.interface import OpenIDStore
from openid.store.nonce import SKEW

from social_auth.models import Association, Nonce


class DjangoOpenIDStore(OpenIDStore):
    """Storage class"""
    def __init__(self):
        """Init method"""
        super(DjangoOpenIDStore, self).__init__()
        self.max_nonce_age = 6 * 60 * 60  # Six hours

    def storeAssociation(self, server_url, association):
        """Store new assocition if doesn't exist"""
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
        """Return stored assocition"""
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

        if expired:  # clear expired associations
            Association.objects.filter(pk__in=expired).delete()

        if associations:  # return most recet association
            associations.sort(key=lambda x: x.issued, reverse=True)
            return associations[0]

    def useNonce(self, server_url, timestamp, salt):
        """Generate one use number and return *if* it was created"""
        if abs(timestamp - time.time()) > SKEW:
            return False
        return Nonce.objects.get_or_create(server_url=server_url,
                                           timestamp=timestamp,
                                           salt=salt)[1]

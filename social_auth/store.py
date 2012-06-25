"""OpenId storage that saves to django models"""
import time
import base64

from openid.store.interface import OpenIDStore
from openid.store.nonce import SKEW

from social_auth.models import delete_associations
from social_auth.models import get_oid_associations
from social_auth.models import store_association
from social_auth.models import use_nonce


class DjangoOpenIDStore(OpenIDStore):
    """Storage class"""
    def __init__(self):
        """Init method"""
        super(DjangoOpenIDStore, self).__init__()
        self.max_nonce_age = 6 * 60 * 60  # Six hours

    def storeAssociation(self, server_url, association):
        """Store new assocition if doesn't exist"""
        store_association(server_url, association)

    def getAssociation(self, server_url, handle=None):
        """Return stored assocition"""
        oid_associations = get_oid_associations(server_url, handle)
        associations = [association
                        for assoc_id, association in oid_associations
                        if association.getExpiresIn() > 0]
        expired = [assoc_id for assoc_id, association in oid_associations
                   if association.getExpiresIn() == 0]

        if expired:  # clear expired associations
            delete_associations(expired)

        if associations:  # return most recet association
            return associations[0]

    def useNonce(self, server_url, timestamp, salt):
        """Generate one use number and return *if* it was created"""
        if abs(timestamp - time.time()) > SKEW:
            return False
        return use_nonce(server_url, timestamp, salt)

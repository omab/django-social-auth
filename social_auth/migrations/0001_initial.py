# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration

from social_auth.models import UserSocialAuth, Nonce, Association


def fields(model):
    return [(f.name, f) for f in model._meta.local_fields]


class Migration(SchemaMigration):
    def forwards(self, orm):
        table = UserSocialAuth._meta.db_table
        db.create_table(table, fields(UserSocialAuth))
        db.send_create_signal('social_auth', ['UserSocialAuth'])
        db.create_unique(table, ['provider', 'uid'])

        table = Nonce._meta.db_table
        db.create_table(table, fields(Nonce))
        db.send_create_signal('social_auth', ['Nonce'])

        table = Association._meta.db_table
        db.create_table(table, fields(Association))
        db.send_create_signal('social_auth', ['Association'])

    def backwards(self, orm):
        table = UserSocialAuth._meta.db_table
        db.delete_unique(table, ['provider', 'uid'])
        db.delete_table(table)
        db.delete_table(Nonce._meta.db_table)
        db.delete_table(Association._meta.db_table)

    complete_apps = ['social_auth']

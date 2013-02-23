# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration

from social_auth.models import Nonce, Association


class Migration(SchemaMigration):
    def forwards(self, orm):
        db.create_index(Nonce._meta.db_table, ['timestamp'])
        db.create_unique(Nonce._meta.db_table, ['timestamp', 'salt',
                                                'server_url'])
        db.create_index(Association._meta.db_table, ['issued'])
        db.create_unique(Association._meta.db_table, ['handle', 'server_url'])

    def backwards(self, orm):
        db.delete_unique(Association._meta.db_table, ['handle', 'server_url'])
        db.delete_index(Association._meta.db_table, ['issued'])
        db.delete_unique(Nonce._meta.db_table, ['timestamp', 'salt',
                                                'server_url'])
        db.delete_index(Nonce._meta.db_table, ['timestamp'])

    complete_apps = ['social_auth']

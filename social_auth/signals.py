"""Signals"""
from django.dispatch import Signal

# Pre update signal
#   This signal is sent when user instance is about to be updated with
#   new values from services provided. This way custom actions can be
#   attached and values updated if needed before the saving time.
#
#   Handlers must return True if any value was updated/changed,
#   otherwise must return any non True value.
#
#   The parameters passed are:
#       sender:   A social auth backend instance
#       user:     Current user instance (retrieved from db or recently
#                 created)
#       response: Raw auth service response
#       details:  Processed details values (basic fields)
pre_update = Signal(providing_args=['user', 'response', 'details'])

socialauth_registered = Signal(providing_args=['user', 'response', 'details'])

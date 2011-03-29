from django.core.exceptions import ValidationError
from django.db import models
from django.utils import simplejson


class JSONField(models.TextField):
    """Simple JSON field that stores python structures as JSON strings
    on database.
    """

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """
        Convert the input JSON value into python structures, raises
        django.core.exceptions.ValidationError if the data can't be converted.
        """
        if self.blank and not value:
            return None
        if isinstance(value, basestring):
            try:
                return simplejson.loads(value)
            except Exception, e:
                raise ValidationError(str(e))
        else:
            return value

    def validate(self, value, model_instance):
        """Check value is a valid JSON string, raise ValidationError on
        error."""
        super(JSONField, self).validate(value, model_instance)
        try:
            return simplejson.loads(value)
        except Exception, e:
            raise ValidationError(str(e))

    def get_db_prep_value(self, value, connection, prepared=False):
        """Convert value to JSON string before save"""
        try:
            return simplejson.dumps(value)
        except Exception, e:
            raise ValidationError(str(e))

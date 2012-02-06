from social_auth.backends import PIPELINE
from social_auth.utils import setting


PIPELINE_ENTRY = 'social_auth.backends.pipeline.misc.save_status_to_session'


def save_status_to_session(request, backend, details, response, uid,
                           *args, **kwargs):
    """Saves current social-auth status to session."""
    next_entry = setting('SOCIAL_AUTH_PIPELINE_RESUME_ENTRY')

    try:
        if next_entry:
            idx = PIPELINE.index(next_entry)
        else:
            idx = PIPELINE.index(PIPELINE_ENTRY) + 1
    except ValueError:
        idx = None

    name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
    request.session[name] = {
        'backend': backend.name,
        'uid': uid,
        'details': details,
        'response': response,
        'is_new': kwargs.get('is_new', True),
        'next_index': idx
    }
    request.session.modified = True

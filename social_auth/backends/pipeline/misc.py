from social_auth.backends import PIPELINE
from social_auth.utils import setting


PIPELINE_ENTRY = 'social_auth.backends.pipeline.misc.save_status_to_session'

def tuple_index(t, e):
    for (i, te) in enumerate(t):
        if te == e:
            return i
    return None

def save_status_to_session(request, auth, *args, **kwargs):
    """Saves current social-auth status to session."""
    next_entry = setting('SOCIAL_AUTH_PIPELINE_RESUME_ENTRY')

    if next_entry:
        idx = tuple_index(PIPELINE, next_entry)
    else:
        idx = tuple_index(PIPELINE, PIPELINE_ENTRY)
        if idx:
            idx += 1

    data = auth.to_session_dict(idx, *args, **kwargs)

    name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
    request.session[name] = data
    request.session.modified = True

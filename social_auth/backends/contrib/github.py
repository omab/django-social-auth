from django.conf import settings


if getattr(settings, 'GITHUB_ORGANIZATION', None):
    from social.backends.github import \
            GithubOrganizationOAuth2 as GithubBackend
else:
    from social.backends.github import GithubOAuth2 as GithubBackend

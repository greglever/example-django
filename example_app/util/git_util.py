"""
Utility for accessing git-related attributes
"""
from git import Repo

from django.conf import settings

REPO = Repo(settings.BASE_DIR)


def get_tags():
    return REPO.tags


def get_latest_tag():
    tags = get_tags()
    latest_tag = tags[-1].name if tags else None
    return latest_tag

from importlib import import_module

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse


def get_model():
    """
    Returns the comment model class.
    """
    return AppConfig.get_model('Comment')


def get_form():
    """
    Returns the comment ModelForm class.
    """
    from forms import CommentForm
    return CommentForm


def get_form_target():
    """
    Returns the target URL for the comment form submission view.
    """
    return reverse("tango_comments.views.comments.post_comment")


def get_flag_url(comment):
    """
    Get the URL for the "flag this comment" view.
    """
    return reverse("tango_comments.views.moderation.flag", args=(comment.id,))


def get_delete_url(comment):
    """
    Get the URL for the "delete this comment" view.
    """
    return reverse("tango_comments.views.moderation.delete", args=(comment.id,))


def get_approve_url(comment):
    """
    Get the URL for the "approve this comment from moderation" view.
    """
    return reverse("tango_comments.views.moderation.approve", args=(comment.id,))

from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse


COMMENT_APP = 'tango_comments'


def get_comment_app():
    """
    Get the comment app as defined in the settings
    """
    # Make sure the app's in INSTALLED_APPS
    if COMMENT_APP not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured("%s must be in INSTALLED_APPS" % COMMENT_APP)

    # Try to import the package
    try:
        package = import_module(COMMENT_APP)
    except ImportError:
        raise ImproperlyConfigured("% is not installed." % COMMENT_APP)

    return package


def get_model():
    """
    Returns the comment model class.
    """
    return get_comment_app().get_model()


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
    if hasattr(get_comment_app(), "get_form_target"):
        return get_comment_app().get_form_target()
    else:
        return reverse("tango_comments.views.comments.post_comment")


def get_flag_url(comment):
    """
    Get the URL for the "flag this comment" view.
    """
    if hasattr(get_comment_app(), "get_flag_url"):
        return get_comment_app().get_flag_url(comment)
    else:
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

from __future__ import absolute_import

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings
from django.utils import six

import tango_comments
from tango_comments.models import Comment
from tango_comments.forms import CommentForm

from . import CommentTestCase


class CommentAppAPITests(CommentTestCase):
    """Tests for the "comment app" API"""


    def testGetForm(self):
        self.assertEqual(tango_comments.get_form(), CommentForm)

    def testGetFormTarget(self):
        self.assertEqual(tango_comments.get_form_target(), "/post/")

    def testGetFlagURL(self):
        c = Comment(id=12345)
        self.assertEqual(tango_comments.get_flag_url(c), "/flag/12345/")

    def getGetDeleteURL(self):
        c = Comment(id=12345)
        self.assertEqual(tango_comments.get_delete_url(c), "/delete/12345/")

    def getGetApproveURL(self):
        c = Comment(id=12345)
        self.assertEqual(tango_comments.get_approve_url(c), "/approve/12345/")


@override_settings(
    COMMENTS_APP='custom_comments',
    INSTALLED_APPS=list(settings.INSTALLED_APPS) + [
        'custom_comments'],
)
class CustomCommentTest(CommentTestCase):
    urls = 'testapp.urls'

    def testGetModel(self):
        from custom_comments.models import CustomComment
        self.assertEqual(tango_comments.get_model(), CustomComment)

    def testGetForm(self):
        from custom_comments.forms import CustomCommentForm
        self.assertEqual(django_comments.get_form(), CustomCommentForm)

    def testGetFormTarget(self):
        self.assertEqual(tango_comments.get_form_target(), "/post/")

    def testGetFlagURL(self):
        c = Comment(id=12345)
        self.assertEqual(tango_comments.get_flag_url(c), "/flag/12345/")

    def getGetDeleteURL(self):
        c = Comment(id=12345)
        self.assertEqual(tango_comments.get_delete_url(c), "/delete/12345/")

    def getGetApproveURL(self):
        c = Comment(id=12345)
        self.assertEqual(tango_comments.get_approve_url(c), "/approve/12345/")

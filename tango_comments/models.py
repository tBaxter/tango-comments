from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from tango_shared.models import BaseUserContentModel

from .managers import CommentManager


COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)


@python_2_unicode_compatible
class Comment(BaseUserContentModel):
    """
    A user comment about some object.
    """

    # Unlike django.contrib.comments, we're not allowing unauthenticated users to comment
    # because we've learned better. So, no user_email etc.
    
    # Metadata about the comment
    ip_address = models.IPAddressField(_('IP address'), blank=True, null=True)
    is_public = models.BooleanField(_('is public'), default=True,
                    help_text=_('Uncheck this box to make the comment effectively ' \
                                'disappear from the site.'))
    is_removed = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the comment is inappropriate. ' \
                                'A "This comment has been removed" message will ' \
                                'be displayed instead.'))

    content_type = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="contenttype_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    # Metadata about the comment
    site = models.ForeignKey(Site, related_name='comment_site')

    # Manager
    objects = CommentManager()

    class Meta:
        db_table = "django_comments"
        ordering = ('post_date',)
        permissions = [("can_moderate", "Can moderate comments")]
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return "%s" % (self.content_object)

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return urlresolvers.reverse(
            "comments-url-redirect",
            args=(self.content_type_id, self.object_pk)
        )

    def get_absolute_url(self, anchor_pattern="#c%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    def get_as_text(self):
        """
        Return this comment as plain text.  Useful for emails.
        """
        d = {
            'user': self.user or self.name,
            'date': self.post_date,
            'comment': self.text,
            'domain': self.site.domain,
            'url': self.get_absolute_url()
        }
        return _('Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % d


@python_2_unicode_compatible
class CommentFlag(models.Model):
    """
    Records a flag on a comment. This is intentionally flexible; right now, a
    flag could be:

        * A "removal suggestion" -- where a user suggests a comment for (potential) removal.

        * A "moderator deletion" -- used when a moderator deletes a comment.

    You can (ab)use this model to add other flags, if needed. However, by
    design users are only allowed to flag a comment with a given flag once;
    if you want rating look elsewhere.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name="comment_flag")
    comment = models.ForeignKey(Comment, verbose_name=_('comment'), related_name="flags")
    flag = models.CharField(_('flag'), max_length=30, db_index=True)
    flag_date = models.DateTimeField(_('date'), default=None)

    # Constants for flag types
    SUGGEST_REMOVAL = "removal suggestion"
    MODERATOR_DELETION = "moderator deletion"
    MODERATOR_APPROVAL = "moderator approval"

    class Meta:
        db_table = 'django_comment_flags'
        unique_together = [('user', 'comment', 'flag')]
        verbose_name = _('comment flag')
        verbose_name_plural = _('comment flags')

    def __str__(self):
        return "%s flag of comment ID %s by %s" % \
            (self.flag, self.comment_id, self.user.get_username())

    def save(self, *args, **kwargs):
        if self.flag_date is None:
            self.flag_date = timezone.now()
        super(CommentFlag, self).save(*args, **kwargs)

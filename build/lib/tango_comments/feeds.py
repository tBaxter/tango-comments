from django.contrib.syndication.views import Feed
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext as _

import tango_comments as comments

class LatestCommentFeed(Feed):
    """Feed of latest comments on the current site."""

    def __call__(self, request, *args, **kwargs):
        self.site = get_current_site(request)
        return super(LatestCommentFeed, self).__call__(request, *args, **kwargs)

    def title(self):
        return _("%(site_name)s comments") % dict(site_name=self.site.name)

    def link(self):
        return "http://%s/" % (self.site.domain)

    def description(self):
        return _("Latest comments on %(site_name)s") % dict(site_name=self.site.name)

    def items(self):
        qs = comments.get_model().objects.filter(
            site__pk = self.site.pk,
            is_public = True,
            is_removed = False,
        )
        return qs.order_by('-post_date')[:40]

    def item_pubdate(self, item):
        return item.post_date

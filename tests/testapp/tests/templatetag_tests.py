from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.template import Template, Context, Library

from tango_comments.forms import CommentForm
from tango_comments.models import Comment

from tests.testapp.models import Article, Author
from . import CommentTestCase

register = Library()

@register.filter
def noop(variable, param=None):
    return variable


class CommentTemplateTagTests(CommentTestCase):

    def render(self, t, **c):
        ctx = Context(c)
        out = Template(t).render(ctx)
        return ctx, out

    def testCommentFormTarget(self):
        out = self.render("{% load comments %}{% comment_form_target %}")
        self.assertEqual(out[1], "/post/")

    def testGetCommentForm(self, tag=None):
        t = "{% load comments %}" + (tag or "{% get_comment_form for testapp.article a.id as form %}")
        out = Template(t).render(Context({'a': Article.objects.get(pk=1)}))
        self.assertEqual(out, "")
        #self.assertTrue(isinstance(ctx["form"], CommentForm))

    def testGetCommentFormFromLiteral(self):
        self.testGetCommentForm("{% get_comment_form for testapp.article 1 as form %}")

    def testGetCommentFormFromObject(self):
        self.testGetCommentForm("{% get_comment_form for a as form %}")

    def testRenderCommentForm(self, tag=None):
        t = "{% load comments %}" + (tag or "{% render_comment_form for testapp.article a.id %}")
        out = Template(t).render(Context({'a': Article.objects.get(pk=1)}))
        self.assertTrue(out.strip().startswith("<form action="))
        self.assertTrue(out.strip().endswith("</form>"))

    def testRenderCommentFormFromLiteral(self):
        self.testRenderCommentForm("{% render_comment_form for testapp.article 1 %}")

    def testRenderCommentFormFromObject(self):
        self.testRenderCommentForm("{% render_comment_form for a %}")

    def testRenderCommentFormFromObjectWithQueryCount(self):
        with self.assertNumQueries(1):
            self.testRenderCommentFormFromObject()

    def verifyGetCommentCount(self, tag=None):
        t = "{% load comments %}" + (tag or "{% get_comment_count for testapp.article a.id as cc %}") + "{{ cc }}"
        out = self.render(t, a=Article.objects.get(pk=1))
        self.assertEqual(out[1], "2")

    def testGetCommentCount(self):
        self.createSomeComments()
        self.verifyGetCommentCount("{% get_comment_count for testapp.article a.id as cc %}")

    def testGetCommentCountFromLiteral(self):
        self.createSomeComments()
        self.verifyGetCommentCount("{% get_comment_count for testapp.article 1 as cc %}")

    def testGetCommentCountFromObject(self):
        self.createSomeComments()
        self.verifyGetCommentCount("{% get_comment_count for a as cc %}")

    def verifyGetCommentList(self, tag=None):
        c2 = Comment.objects.all()[1]
        t = "{% load comments %}" +  (tag or "{% get_comment_list for testapp.author a.id as cl %}")
        ctx, out = self.render(t, a=Author.objects.get(pk=1))
        self.assertEqual(out, "")
        self.assertEqual(list(ctx["cl"]), [c2])

    def testGetCommentList(self):
        self.createSomeComments()
        self.verifyGetCommentList("{% get_comment_list for testapp.author a.id as cl %}")

    def testGetCommentListFromLiteral(self):
        self.createSomeComments()
        self.verifyGetCommentList("{% get_comment_list for testapp.author 1 as cl %}")

    def testGetCommentListFromObject(self):
        self.createSomeComments()
        self.verifyGetCommentList("{% get_comment_list for a as cl %}")

    def testRenderCommentList(self, tag=None):
        t = "{% load comments %}" + (tag or "{% render_comment_list for testapp.article a.id %}")
        out = self.render(t, a=Article.objects.get(pk=1))[1]
        self.assertTrue(out.strip().startswith("<dl id=\"comments\">"))
        self.assertTrue(out.strip().endswith("</dl>"))

    def testRenderCommentListFromLiteral(self):
        self.testRenderCommentList("{% render_comment_list for testapp.article 1 %}")

    def testRenderCommentListFromObject(self):
        self.testRenderCommentList("{% render_comment_list for a %}")

    def testNumberQueries(self):
        """
        Ensure that the template tags use cached content types to reduce the
        number of DB queries.
        Refs #16042.
        """

        self.createSomeComments()

        # {% render_comment_list %} -----------------

        # Clear CT cache
        ContentType.objects.clear_cache()
        with self.assertNumQueries(4):
            self.testRenderCommentListFromObject()

        # CT's should be cached
        with self.assertNumQueries(3):
            self.testRenderCommentListFromObject()

        # {% get_comment_list %} --------------------

        ContentType.objects.clear_cache()
        with self.assertNumQueries(4):
            self.verifyGetCommentList()

        with self.assertNumQueries(3):
            self.verifyGetCommentList()

        # {% render_comment_form %} -----------------

        ContentType.objects.clear_cache()
        with self.assertNumQueries(3):
            self.testRenderCommentForm()

        with self.assertNumQueries(2):
            self.testRenderCommentForm()

        # {% get_comment_form %} --------------------

        ContentType.objects.clear_cache()
        with self.assertNumQueries(3):
            self.testGetCommentForm()

        with self.assertNumQueries(2):
            self.testGetCommentForm()

        # {% get_comment_count %} -------------------

        ContentType.objects.clear_cache()
        with self.assertNumQueries(3):
            self.verifyGetCommentCount()

        with self.assertNumQueries(2):
            self.verifyGetCommentCount()

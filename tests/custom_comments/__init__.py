from django.urls import reverse

def get_custom_model():
    from .models import CustomComment
    return CustomComment
    
def get_custom_form():
    from .forms import CustomCommentForm
    return CustomCommentForm

def get_model():
    return get_custom_model()

def get_form():
    return get_custom_form()

def get_form_target():
    return reverse(
        "custom_comments.views.custom_submit_comment"
    )

def get_flag_url(c):
    return reverse(
        "custom_comments.views.custom_flag_comment",
        args=(c.id,)
    )

def get_delete_url(c):
    return reverse(
        "custom_comments.views.custom_delete_comment",
        args=(c.id,)
    )

def get_approve_url(c):
    return reverse(
        "custom_comments.views.custom_approve_comment",
        args=(c.id,)
    )

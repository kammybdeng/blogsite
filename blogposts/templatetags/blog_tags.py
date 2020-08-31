from django import template
from ..models import Post
register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()
@register.simple_tag
def user_total_posts(author_id):
    return Post.objects.filter(author=author_id).count()

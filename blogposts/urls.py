from django.urls import path
from . import views

app_name = 'blogposts'
urlpatterns = [
    # ex: /polls/
    path('signup/', views.signup, name = 'signup'),
    path('', views.IndexView.as_view(), name = 'index'),
    # ex: /polls/5/
    # the 'name' value as called by the {% url %} template tag
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:post_id>/create_comment/', views.create_comment, name='create_comment'),
    path('<int:post_id>/like_post/', views.like_post, name='like_post'),
    path('create_post/', views.create_post, name='create_post')]

    # ex: /polls/5/results/
#     path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

from django.urls import path
#from django.views import generic.TemplateView
from django.conf.urls import include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import UserLoginForm

app_name = 'blogposts'
urlpatterns = [
    # ex: /polls/
    #path('', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name = 'signup'),
    #path('connection/',TemplateView.as_view(template_name = 'blogposts/login.html')),
    path('login/', LoginView.as_view(template_name= 'registration/login.html',
    authentication_form = UserLoginForm), name = 'login'),
    path('logout/', LogoutView.as_view(template_name= 'registration/logout.html'),
    name = 'logout'),
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

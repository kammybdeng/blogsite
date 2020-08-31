from django.urls import path, reverse_lazy
from django.contrib.sitemaps.views import sitemap
from blogposts.sitemaps import PostSitemap
#from django.views import generic.TemplateView
from django.conf.urls import include
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from . import views
from .forms import UserLoginForm

app_name = 'blogposts'
sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    # ex: /polls/
    #path('', include('django.contrib.auth.urls')),

    #path('connection/',TemplateView.as_view(template_name = 'blogposts/login.html')),
    path('index/', views.post_list, name = 'index'),
    path('', views.dashboard, name = 'dashboard'),
    path('login/', LoginView.as_view(template_name= 'registration/login.html',
    authentication_form = UserLoginForm), name = 'login'),
    path('logout/', LogoutView.as_view(template_name= 'registration/logout.html'),
    name = 'logout'),
    path('signup/', views.signup, name = 'signup'),
    path('edit/', views.edit, name='edit'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_change/', PasswordChangeView.as_view(success_url = reverse_lazy('blogposts:password_change_done')), name='password_change'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('new_post/', views.new_post, name='new_post'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/create_comment/', views.create_comment, name='create_comment'),
    path('<int:post_id>/like_post/', views.like_post, name='like_post'),
    path('<int:post_id>/delete_post/', views.delete_post, name ='delete_post'),
    path('tag/<slug:tag_slug>/', views.post_list, name = 'post_list_by_tag'),
    path('search/', views.post_search, name='post_search'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
    name = 'django.contrib.sitemaps.views.sitemap')]
    # ex: /polls/5/results/
#     path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

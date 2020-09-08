from django.urls import path, reverse_lazy
from django.contrib.sitemaps.views import sitemap
from blogposts.sitemaps import PostSitemap
from django.conf.urls import include
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from .forms import UserLoginForm

app_name = 'blogposts'
sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    #path('', include('django.contrib.auth.urls')),
    #path('connection/',TemplateView.as_view(template_name = 'blogposts/login.html')),
    path('index/', views.post_list, name = 'index'),
    #path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:post_id>/', views.post_detail, name='detail'),
    path('new_post/', views.new_post, name='new_post'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/create_comment/', views.create_comment, name='create_comment'),
    path('<int:post_id>/like_post/', views.like_post, name='like_post'),
    path('<int:post_id>/delete_post/', views.delete_post, name ='delete_post'),
    path('tag/<slug:tag_slug>/', views.post_list, name = 'post_list_by_tag'),
    path('search/', views.post_search, name='post_search'),

    path('', views.dashboard, name = 'dashboard'),
    path('login/', LoginView.as_view(template_name= 'registration/login.html',
    authentication_form = UserLoginForm), name = 'login'),
    path('logout/', LogoutView.as_view(template_name= 'registration/logout.html'),
    name = 'logout'),
    path('signup/', views.signup, name = 'signup'),
    path('edit/', views.edit, name='edit'),
    path('password_change/', PasswordChangeView.as_view(success_url = reverse_lazy('blogposts:password_change_done')), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(success_url = reverse_lazy('blogposts:password_reset_done')), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url = reverse_lazy('blogposts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
    name = 'django.contrib.sitemaps.views.sitemap'),

    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('users/follow/', views.user_follow, name='user_follow'),

]

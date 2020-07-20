from django.shortcuts import render, get_object_or_404, redirect
#from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.contrib.auth.models import User
from .forms import SignUpForm
#LoginForm
from .models import Post


# def index(request):
#     return HttpResponse("Hello, You're at the post homepage.")

# class SignupView(generic.DetailView):
#     model = Post
#     template_name = 'blogposts/signup.html'


class IndexView(generic.ListView):
    #model = Post
    template_name = 'blogposts/index.html'
    context_object_name = 'last_ten_in_ascending_order'

    def get_queryset(self):
        """Return the last ten published questions."""
        last_ten = Post.objects.order_by('-published_date')[:10]
        last_ten_in_ascending_order = reversed(last_ten)
        return last_ten_in_ascending_order

# def details(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     post_text = Post.objects.get(pk=post_id).post_text
#     return HttpResponse("Hello, You're viewing the detail page of %s. \n\n %s" % (post_id,post_text))

## generic template view

class DetailView(generic.DetailView):
    model = Post
    template_name = 'blogposts/detail.html'


def signup(request):
    # if request.user.is_authenticated:
    #     return render(request, 'blogposts/index.html')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username= username, password =raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('blogposts:index'))
    else:
        form = SignUpForm()
    return render(request, 'blogposts/signup.html', {'form': form})

@login_required
def dashboard(request):
    print("HERE")
    return render(request, 'blogposts/dashboard.html', {"section" : 'dashboard'})

def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    pending_comment = request.POST['comment']
    if pending_comment != '':
        post.comment_set.create(comment_text = pending_comment,
                                published_date = timezone.now())
    return HttpResponseRedirect(reverse('blogposts:detail', args=(post.id,)))
    # else:
    #     return HttpResponseRedirect(reverse('blogposts:detail', args=(post.id,)))

def create_post(request):
    pending_post = request.POST['create_post']
    if pending_post != '':
        if request.user.is_authenticated:
            current_user = request.user
            post = Post(content = pending_post,
                        published_date = timezone.now(),
                        author = current_user)
            post.save()
        return HttpResponseRedirect(reverse('blogposts:detail', args=(post.id,)))
    return HttpResponseRedirect(reverse('blogposts:index'))


def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.is_authenticated:
        current_user = request.user
        user_id = User.objects.get(pk=current_user.id).id
        if user_id not in post.liked_users:
                num_likes = post.likes
                post.likes = num_likes + 1
                post.liked_users.append(user_id)
                post.save()
    else:
        return HttpResponse("You already liked blog %s." % post_id)
    return HttpResponseRedirect(reverse('blogposts:detail', args=(post.id,)))


# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         # POST => HttpResponseRedirect => success page
#         # GET => HttpResponse => success page
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
#     return HttpResponse("You're voting on question %s." % question_id)



    # <form action="{% url 'polls:vote' question.id %}" method="post">
    # {% csrf_token %}
    # {% for choice in question.choice_set.all %}
    #     <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    #     <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    # {% endfor %}
    # <input type="submit" value="Vote">
    # </form>

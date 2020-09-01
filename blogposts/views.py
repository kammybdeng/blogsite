from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from taggit.models import Tag
from .forms import SignUpForm, UserEditForm, ProfileEditForm, EmailPostForm, NewPostForm, SearchForm
from .models import Post, Profile

# class IndexView(generic.ListView):
#     model = Post
#     template_name = 'blogposts/index.html'
#     context_object_name = 'last_ten_in_ascending_order'
#     paginate_by = 5
#     def get_queryset(self):
#         """Return the last ten published questions."""
#         last_ten_in_ascending_order = Post.objects.order_by('-published_date')[:10]
#         #last_ten_in_ascending_order = reversed(last_ten)
#         #print(last_ten_in_ascending_order)
#         return last_ten_in_ascending_order

def post_list(request, tag_slug=None):
    object_list = Post.objects.all().order_by('-id')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        object_list = object_list.filter(tags__in = [tag])
    paginator = Paginator(object_list, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        ## if page is not an integer return the first page
        posts = paginator.page(1)
    except EmptyPage:
        ## if page is out of range, return the last page
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blogposts/index.html', {'page': page,
                                                    'posts': posts,
                                                    'tag': tag})

# class DetailView(generic.DetailView):
#     model = Post
#     template_name = 'blogposts/detail.html'

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    ## List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in = post_tags_ids).exclude(id=post_id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-published_date')[:4]
    return render(request, 'blogposts/detail.html', {'post': post,
                                                      # 'comments': comment,
                                                      'similar_posts': similar_posts})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            new_user = authenticate(username= username, password =raw_password)
            Profile.objects.create(user=new_user)
            login(request, new_user)
            return HttpResponseRedirect(reverse('blogposts:index'))
    else:
        form = SignUpForm()
    return render(request, 'blogposts/signup.html', {'form': form})

@login_required
def dashboard(request):
    #context_object_name = 'dashboard_last_ten_in_ascending_order'
    def get_queryset(request):
        """Return the user's last ten published questions."""
        current_user = request.user
        dashboard_last_ten_in_ascending_order = Post.objects.filter(author = current_user).order_by('-published_date')[:10]
        return dashboard_last_ten_in_ascending_order
    user_post_list = get_queryset(request)
    return render(request, 'blogposts/dashboard.html', {"section" : 'dashboard',
    'dashboard_last_ten_in_ascending_order' : user_post_list})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'blogposts/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    pending_comment = request.POST['comment']
    if pending_comment != '':
        post.comment_set.create(commenter = request.user,
                                comment_text = pending_comment,
                                published_date = timezone.now())
    return HttpResponseRedirect(reverse('blogposts:detail', args=(post.id,)))

@login_required
def new_post(request):
    if request.method == 'POST':
        new_post_form = NewPostForm(instance = request.user,
                                    data=request.POST)
        if new_post_form.is_valid():
            new_post_form.save(commit=False)
            cleaned_data = new_post_form.cleaned_data
            current_user = request.user
            post = Post(title = cleaned_data['title'],
                        content = cleaned_data['content'],
                        published_date = timezone.now(),
                        author = current_user)
            post.save()
            post.tags.add(*cleaned_data['tags'])
            return HttpResponseRedirect(reverse('blogposts:detail', args=(post.id,)))
        else:
            messages.error(request, 'Error creating new post')
    else:
        new_post_form = NewPostForm(instance = request.user)
    return render(request, 'blogposts/new_post.html', {'new_post_form': new_post_form})


# def create_post(request):
#     pending_post = request.POST['create_post']
#     if pending_post != '':
#         if request.user.is_authenticated:
#             current_user = request.user
#             post = Post(content = pending_post,
#                         published_date = timezone.now(),
#                         author = current_user)
#             post.save()
#         return HttpResponseRedirect(reverse('blogposts:detail', args=(post.id,)))
#     return HttpResponseRedirect(reverse('blogposts:index'))
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.is_authenticated:
        current_user = request.user
        post_author = post.author
        if current_user == post_author:
            post.delete()
            deleted = True
            messages.success(request, 'Post deleted successfully')
        else:
            messages.error(request, 'Cannot Delete Post')
            return HttpResponseRedirect(reverse('blogposts:detail', args=(post.id,)))
    return HttpResponseRedirect(reverse('blogposts:index'))

@login_required
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
@login_required
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, pk=post_id)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'kammyinquiries@gmail.com',
                      [cd['email']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blogposts/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'content')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(search = search_vector,
                                            rank = SearchRank(search_vector, search_query)
                                            ).filter(search=search_query).order_by('-rank')
            print(results, '--'*10)
            if not results:
                results = Post.objects.annotate(similarity = TrigramSimilarity('title', query),
                ).filter(similarity__gt = 0.1).order_by('-similarity')
    return render(request, 'blogposts/search.html', {'form': form,
                                                    'query': query,
                                                    'results': results})



    # <form action="{% url 'polls:vote' question.id %}" method="post">
    # {% csrf_token %}
    # {% for choice in question.choice_set.all %}
    #     <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    #     <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    # {% endfor %}
    # <input type="submit" value="Vote">
    # </form>

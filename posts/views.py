from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import HashTag, Post
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            for word in post.content.split():
                if word.startswith('#'):
                    # hashtag 추가
                    hashtag = HashTag.objects.get_or_create(
                        content=word)[0]  # (obj, Ture or False 반환)
                    post.hashtags.add(hashtag)
            return redirect("posts:index")
    else:
        form = PostForm()
    context = {
        'form': form
    }

    return render(request, 'posts/form.html', context)


def hashtags(request, id):
    hashtag = get_object_or_404(HashTag, id=id)

    posts = hashtag.tagged_post.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def like(request, id):
    user = request.user
    post = get_object_or_404(Post, id=id)
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)


# def update(request, id):
#     post = get_object_or_404(Post, id=id)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save()
#             post.hashtags.clear()
#             for word in post.content.split():
#                 if word.startswith('#'):
#                     # hashtag 추가
#                     hashtag = HashTag.objects.get_or_create(content=)
#                     post.hashtags.add(hashtag)
#                     return redirect('posts:index')
#     else:
#         form = PostForm(instance=post)
#     context: {
#         'form': form
#     }
#     return render(request, 'posts/form.html', context)

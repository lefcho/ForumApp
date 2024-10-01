from django.shortcuts import render, redirect

from ForumApp.posts.forms import SearchForm, PostCreateForm, PostDeleteForm
from ForumApp.posts.models import Post


def index(request):
    context = {
        'my_form': '',
    }

    return render(request, 'base.html', context)


def dashboard(request):
    form = SearchForm(request.GET)
    posts = Post.objects.all()

    if request.method == 'GET':
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = posts.filter(title__icontains=query)

    context = {
        'posts': posts,
        'form': form,
    }

    return render(request, 'posts/dashboard.html', context)


def add_post(request):
    form = PostCreateForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        'form': form,
    }

    return render(request, 'posts/add-post.html', context)


def edit_post(request, pk:int):
    pass


def detail_post(request, pk:int):
    post = Post.objects.get(pk=pk)

    context = {
        'post': post,
    }

    return render(request, 'posts/details-post.html', context)


def delete_post(request, pk:int):
    post = Post.objects.get(pk=pk)
    form = PostDeleteForm(instance=post)

    if request.method == 'POST':
        post.delete()
        return redirect('dashboard')

    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'posts/details-post.html', context)













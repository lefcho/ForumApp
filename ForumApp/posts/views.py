from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import classonlymethod, method_decorator
from django.views.generic import TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView, DetailView

from ForumApp.posts.decorators import measure_execution_time
from ForumApp.posts.forms import SearchForm, PostCreateForm, PostDeleteForm, PostEditForm, CommentFormSet
from ForumApp.posts.mixins import TimeRestrictionMixin
from ForumApp.posts.models import Post


class BaseView:
    @classonlymethod
    def as_view(cls):

        def view(request, *args, **kwargs):
            view_instance = cls()
            return view_instance.dispatch(request, *args, **kwargs)

        return view

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.get(request, *args, **kwargs)
        elif request.method == "POST":
            return self.post(request, *args, **kwargs)


@method_decorator(measure_execution_time, name='dispatch')
class IndexView(TimeRestrictionMixin, TemplateView):
    # template_name = 'common/index.html'
    # extra_context = {
    #     'static_time': datetime.now()
    # }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['dynamic_time'] = datetime.now()

        return context

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['common/index_logged_in.html']
        else:
            return ['common/index.html']


# def index(request):
#     post_form = modelform_factory(
#         Post,
#         fields=('title', 'content', 'author'),
#     )
#
#     context = {
#         'my_form': post_form,
#     }
#
#     return render(request, 'common/index.html', context)


class DashboardView(ListView, FormView):
    template_name = 'posts/dashboard.html'
    model = Post
    context_object_name = 'posts'
    form_class = SearchForm
    success_url = reverse_lazy('dashboard')
    paginate_by = 2

    def get_queryset(self):
        queryset = self.model.objects.all()

        if not self.request.user.has_perm('posts.can_approve_posts'):
            queryset = queryset.filter(approved=True)

        if 'query' in self.request.GET:
            query = self.request.GET.get('query')
            queryset = queryset.filter(title__icontains=query)

        return queryset


# def dashboard(request):
#     form = SearchForm(request.GET)
#     posts = Post.objects.all()
#
#     if request.method == 'GET':
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             posts = posts.filter(title__icontains=query)
#
#     context = {
#         'posts': posts,
#         'form': form,
#     }
#
#     return render(request, 'posts/dashboard.html', context)


def approve_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.approved = True
    post.save()

    return redirect(request.META.get('HTTP_REFERER'))


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/add-post.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('dashboard')


# def add_post(request):
#     form = PostCreateForm(request.POST or None, request.FILES or None)
#
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'posts/add-post.html', context)


class EditPostView(UpdateView):
    model = Post
    template_name = 'posts/edit_post.html'
    success_url = reverse_lazy('dashboard')

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return modelform_factory(Post, fields=('title', 'content', 'author', 'languages'))
        else:
            return modelform_factory(Post, fields=('content', ))

# def edit_post(request, pk:int):
#     post = Post.objects.get(pk=pk)
#
#     if request.method == 'POST':
#         form = PostEditForm(request.POST, instance=post)
#
#         if form.is_valid():
#             post.save()
#             return redirect('dashboard')
#     else:
#         form = PostEditForm(instance=post)
#
#     context = {
#         'post': post,
#         'form': form,
#     }
#
#     return render(request, 'posts/edit_post.html', context)


# def detail_post(request, pk:int):
#     post = Post.objects.get(pk=pk)
#     formset = CommentFormSet(request.POST or None)
#     comments = post.comments.all()
#
#     if request.method == 'POST':
#         if formset.is_valid():
#             for form in formset:
#                 if form.cleaned_data:
#                     comment = form.save(commit=False)
#                     comment.post = post
#                     comment.save()
#
#         return redirect('details-post', pk=post.id)
#
#     context = {
#         'post': post,
#         'formset': formset,
#         'comments': comments,
#     }
#
#     return render(request, 'posts/details-post.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/details-post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = CommentFormSet()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        formset = CommentFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    comment = form.save(commit=False)
                    comment.post = post
                    comment.save()

            return redirect('details-post', pk=post.id)

        context = self.get_context_data()
        context['formset'] = formset

        return self.render_to_response(context)


class DeletePostView(DeleteView, FormView):
    model = Post
    template_name = 'posts/delete-post.html'
    # form_class = PostDeleteForm
    success_url = reverse_lazy('dashboard')

    # def get_initial(self):
    #     pk = self.kwargs.get(self.pk_url_kwarg)
    #     post = Post.objects.get(pk=pk)
    #     return post.__dict__


# def delete_post(request, pk:int):
#     post = Post.objects.get(pk=pk)
#     form = PostDeleteForm(instance=post)
#
#     if request.method == 'POST':
#         post.delete()
#         return redirect('dashboard')
#
#     context = {
#         'form': form,
#         'post': post,
#     }
#
#     return render(request, 'posts/delete-post.html', context)













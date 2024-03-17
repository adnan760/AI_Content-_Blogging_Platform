from django.shortcuts import render, redirect
from .models import PostModel
from dashboard.models import *
from dashboard.urls import *
from .forms import PostModelForm, PostUpdateForm, CommentForm
from django.contrib import messages
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    posts = PostModel.objects.all()
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('blog-index')
    else:
        form = PostModelForm()
    context = {
        'posts': posts,
        'form': form
    }

    return render(request, 'blog/post_index.html', context)


@login_required
def post_detail(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('blog-post-detail', pk=post.id)
    else:
        c_form = CommentForm()
    context = {
        'post': post,
        'c_form': c_form,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_edit(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog-post-detail', pk=post.id)
    else:
        form = PostUpdateForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post_edit.html', context)


@login_required
def post_delete(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog-index')
    context = {
        'post': post
    }
    return render(request, 'blog/post_delete.html', context)

@login_required
def post_blog_topic(request, uniqueId):
    try:
        blog1 = Blog.objects.get(uniqueId=uniqueId)
    except:
        messages.error(request, "Something went wrong")
        return redirect('view-generated-blog')

    try:
        blog1 = Blog.objects.get(uniqueId=uniqueId)
        blogSections1 = BlogSection.objects.filter(blog=blog1)

        context ={}

        for item in blogSections1:
            org_content = item.title + item.body
            soup = BeautifulSoup(org_content, 'html.parser')
            cleaned_content = soup.get_text(separator='\n\n')
            postdata = PostModel.objects.create(title=blog1.title, content=cleaned_content, author=request.user)

            postdata.save()
    except:
        messages.error(request, "You have already posted a blog on this topic. Go for a new one!")
        return redirect(f'/dashboard/view-generated-blog/{blog1.slug}')

    return redirect('blog-index')
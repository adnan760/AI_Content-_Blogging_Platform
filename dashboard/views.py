from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from django.conf import settings
import requests
from datetime import datetime as dt
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .functions import *

@login_required
def home(request):
    emptyBlogs = []
    completedBlogs = []
    monthCount = 0
    blogs = Blog.objects.filter(profile=request.user.profile)
    for blog in blogs:
        sections = BlogSection.objects.filter(blog=blog)
        if sections.exists():
            #Blog words
            blogWords = 0
            for section in sections:
                # section.save()
                blogWords += int(section.wordCount)
                monthCount += int(section.wordCount)
                blog.wordCount = str(blogWords)
                blog.save()
            completedBlogs.append(blog)
        else:
            emptyBlogs.append(blog)

    allowance = checkCountAllowance(request.user.profile)

    context = {}
    context['numBlogs'] = len(completedBlogs)
    context['monthCount'] = request.user.profile.monthlyCount
    context['countReset'] =  getSubscriptionDate(request.user.profile)
    context['emptyBlogs'] = emptyBlogs
    context['completedBlogs'] = completedBlogs
    context['allowance'] =  allowance
    return render(request, 'dashboard/home.html', context)

@login_required
def profile(request):
    context = {}
    
    if request.method == 'GET':
        form  = ProfileForm(instance = request.user.profile, user=request.user)
        image_form = ProfileImageForm(instance = request.user.profile)
        context['form'] = form
        context['image_form'] = image_form
        return render(request, 'dashboard/profile.html', context)

    if request.method == 'POST':
        if request.user:
            form  =  ProfileForm(request.POST, instance = request.user.profile, user=request.user)
            image_form = ProfileImageForm(request.POST, request.FILES, instance = request.user.profile)

            if form.is_valid():
                form.save()
                return redirect('profile')

            if image_form.is_valid():
                image_form.save()
                return redirect('profile')
        else:
            messages.error(request, "Something")
            return('profile')

    return render(request, 'dashboard/profile.html', context)


@login_required
def blogTopic(request):
    context = {}

    if request.method == "POST":
        blogIdea = request.POST['blogIdea']
        request.session['blogIdea']=blogIdea

        keywords = request.POST['keywords']
        request.session['keywords']=keywords

        audience = request.POST['audience']
        request.session['audience']=audience


        blogTopics = generateBlogTopicIdeas(blogIdea, audience, keywords)
        if len(blogTopics)>0:
            request.session['blogTopics'] = blogTopics
            return redirect('blog-sections')
        else:
            messages.error(request, "Oops! We could not generate any blog ideas for you, please try again.")
            return redirect('blog-topic')


    return render(request, 'dashboard/blog-topic.html', context)

@login_required
def blogSections(request):
    if 'blogTopics' in request.session:
        pass
    else:
        messages.error(request, "Start by creating blg topic ideas")
        return redirect('blog-topic')

    context ={}
    context['blogTopics'] = request.session['blogTopics']

    return render (request, 'dashboard/blog-sections.html', context)

@login_required
def saveBlogTopic(request, blogTopic):
    if 'blogIdea' in request.session and 'keywords' in request.session and 'audience' in request.session and 'blogTopics' in request.session:
        blog = Blog.objects.create(
        title = blogTopic,
        blogIdea = request.session['blogIdea'],
        keywords = request.session['keywords'],
        audience = request.session['audience'],
        profile = request.user.profile
        )
        blog.save()
        blogTopics = request.session['blogTopics']
        blogTopics.remove(blogTopic)
        request.session['blogTopics'] = blogTopics
        return redirect('blog-sections')
    else:
        return redirect('blog-topic')


@login_required
def useBlogTopic(request, blogTopic):
    context = {}
    if 'blogIdea' in request.session and 'keywords' in request.session and 'audience' in request.session:

        if Blog.objects.filter(title=blogTopic).exists():
            blog = Blog.objects.get(title=blogTopic)

        else:

            blog = Blog.objects.create(
            title = blogTopic,
            blogIdea = request.session['blogIdea'],
            keywords = request.session['keywords'],
            audience = request.session['audience'],
            profile = request.user.profile
            )
            blog.save()
        blogSections= generateBlogSectionTitles(blogTopic, request.session['audience'], request.session['keywords'])
        
    else:
        return redirect('blog-topic')

    
    if len(blogSections)>0:
        request.session['blogSections'] = blogSections
        context['blogSections'] = blogSections
    else:
        messages.error(request, "Oops! We could not generate any blog sections for you, please try again.")
        return redirect('blog-topic')

    if request.method == "POST":
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:
                section = generateBlogSectionDetails(blogTopic, val, request.session['audience'], request.session['keywords'],request.user.profile)

                blogSec =  BlogSection.objects.create(
                    title = val,
                    body = section,
                    blog = blog
                )
                blogSec.save()

        return redirect('view-generated-blog',slug=blog.slug)

    return render(request, 'dashboard/select-blog-sections.html', context)
    

@login_required
def viewGeneratedBlog(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        messages.error(request, "Something went wrong")
        return redirect('blog-topic')

    blogSections = BlogSection.objects.filter(blog=blog)
    context ={}
    context['blog']=blog
    context['blogSections'] = blogSections

    return render(request, 'dashboard/view-generated-blog.html', context)

@login_required
def createBlogFromTopic(request, uniqueId):
    context = {}
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
    except:
        messages.error(request, "Blog not found")
        return redirect('dashboard')


        
    blogSections= generateBlogSectionTitles(blog.title, blog.audience, blog.keywords)

    
    if len(blogSections)>0:
        request.session['blogSections'] = blogSections
        context['blogSections'] = blogSections
    else:
        messages.error(request, "Oops! We could not generate any blog sections for you, please try again.")
        return redirect('blog-topic')

    if request.method == "POST":
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:
                section = generateBlogSectionDetails(blog.title, val, blog.audience, blog.keywords, request.user.profile)

                blogSec =  BlogSection.objects.create(
                    title = val,
                    body = section,
                    blog = blog
                )
                blogSec.save()

        return redirect('view-generated-blog',slug=blog.slug)

    return render(request, 'dashboard/select-blog-sections.html', context)

@login_required
def deleteBlogTopic(request, uniqueId):
    try:
        blog = Blog.objects.get(uniqueId= uniqueId)
        if blog.profile == request.user.profile:
            blog.delete()
            redirect('dashboard')
        else:
            messages.error(request, "Access denied")
        return redirect('dashboard')
    except:
        messages.error(request, "Blog not found")
        return redirect('dashboard')

@login_required
def billing(request):
    context={}

    context['nextBillingDate'] = getSubscriptionDate(request.user.profile)

    return render(request, 'dashboard/billing.html', context)
    
@login_required
def PaymentSuccess(request):
    print(request.POST['type'])
    if request.POST['type'] =='starter':
        try:
            profile = Profile.objects.get(uniqueId=request.POST['userId'])
            profile.subscribed = True
            profile.subscriptionType = 'starter'
            profile.subscriptionReference = request.POST['subscriptionID']
            current_datetime = timezone.now()
            next_date = current_datetime + relativedelta(months=1)
            profile.subscriptionDate = next_date
            print(request.POST['subscriptionID'])
            profile.save()
            return JsonResponse({'result':'SUCCESS'})
        except:
            return JsonResponse({'result':'FAIL'})
    
    elif request.POST['type'] =='advanced':
        try:
            profile = Profile.objects.get(uniqueId=request.POST['userId'])
            profile.subscribed = True
            profile.subscriptionType = 'advanced'
            profile.subscriptionReference = request.POST['subscriptionID']
            current_datetime = timezone.now()
            next_date = current_datetime + relativedelta(months=1)
            profile.subscriptionDate = next_date
            profile.save()
            return JsonResponse({'result':'SUCCESS'})
        except:
            return JsonResponse({'result':'FAIL'})
    else:
        return JsonResponse({'result':'FAIL'})

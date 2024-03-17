import os
import openai
from django.conf import settings

import requests
from dateutil.relativedelta import relativedelta
import datetime
from django.utils import timezone
import json

openai.api_key = settings.OPENAI_API_KEYS


def returnMonth(month):
    if month == 1:
        return 'January'
    elif month == 2:
        return 'February'
    elif month == 3:
        return 'March'
    elif month == 4:
        return 'April'
    elif month == 5:
        return 'May'
    elif month == 6:
        return 'June'
    elif month == 7:
        return 'July'
    elif month == 8:
        return 'August'
    elif month == 9:
        return 'September'
    elif month == 10:
        return 'October'
    elif month == 11:
        return 'November'
    else:
        return 'December'
    
    


def generateBlogTopicIdeas(topic, audience, keywords):
    blog_topics =[]
    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Generate 5 blog topic ideas on the following topic without displaying quotation marks in output:{}\nAudience: {}\nKeywords: {} \n*".format(topic, audience, keywords),
    temperature=1,
    max_tokens=256,
    top_p=1,
    best_of=1,
    frequency_penalty=0,
    presence_penalty=0)

    if 'choices' in response:
        if len(response['choices'])>0:
            res  = response['choices'][0]['text']
        else:
            return []
    else:
        return []

    #a_list = res.split('*')
    lines = res.strip().split('\n')

    a_list = []
    for line in lines:
        # Split each line into words
        words = line.split()
        # Filter out non-content words (e.g., numbers, punctuation)
        content_words = [word for word in words if word.isalpha()]
        # Join the remaining words into a single string and append to the content list
        a_list.append(' '.join(content_words))


    if len(a_list)>0:
        for blog in a_list :
            blog_topics.append(blog)

    else:
        return []

    return blog_topics

def generateBlogSectionTitles(topic, audience, keywords):
    blog_sections =[]
    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Generate  7 adequate sub sections but display only headings for those sections following blog topic, audience and keywords:{}\nAudience: {}\nKeywords: {} \n*".format(topic, audience, keywords),
    temperature=1,
    max_tokens=256,
    top_p=1,
    best_of=1,
    frequency_penalty=0,
    presence_penalty=0)

    if 'choices' in response:
        if len(response['choices'])>0:
            res  = response['choices'][0]['text']
        else:
            return []
    else:
        return []

    # a_list = res.split('*')

    lines = res.strip().split('\n')

    a_list = []
    for line in lines:
        # Split each line into words
        words = line.split()
        # Filter out non-content words (e.g., numbers, punctuation)
        content_words = [word for word in words if word.isalpha()]
        # Join the remaining words into a single string and append to the content list
        a_list.append(' '.join(content_words))



    if len(a_list)>0:
        for blog in a_list :
            blog_sections.append(blog)

    else:
        return []

    return blog_sections


def generateBlogSectionDetails(blogTopic, sectionTopic, audience, keywords, profile):
    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Generate a detailed blog section write up for the following blog section heading using the blog title, audience and keywords provided.\nBlog Title: {}\nBlog Section Heading:  {}\nAudience: {}\nKeywords: {}\n".format(blogTopic, sectionTopic, audience, keywords),
    temperature=1,
    max_tokens=1000,
    top_p=1,
    best_of=1,
    frequency_penalty=0,
    presence_penalty=0)

    if 'choices' in response:
        if len(response['choices'])>0:
            res  = response['choices'][0]['text']
            if not res == '':
                cleanedRes =  res.replace('\n','<br>')
                if profile.monthlyCount:
                    
                    oldCount = int(profile.monthlyCount)

                else:
                    oldCount =0

                oldCount += len(cleanedRes.split(' '))
                profile.monthlyCount = str(oldCount)
                profile.save()
                return cleanedRes
            else:
                return ''
        else:
            return ''
    else:
        return ''
    

def checkCountAllowance(profile):
    if profile.subscribed:
        type = profile.subscriptionType
        if type == 'free':
            max_limit = 5000
            if profile.monthlyCount:
                if int(profile.monthlyCount) < max_limit:
                    return True
                else:
                    return False
            else:
                return True
        elif type=='starter':
            max_limit = 40000
            if profile.monthlyCount:
                if int(profile.monthlyCount) < max_limit:
                    return True
                else:
                    return False
            else:
                return True
        elif type == 'advanced':
            return True
        else:
            return False
    else:
        max_limit = 5000
        if profile.monthlyCount:
            if int(profile.monthlyCount) < max_limit:
                return True
            else:
                return False
        else:
            return True



def getSubscriptionDate(profile):
    subId = profile.subscriptionReference
    subDate =  profile.subscriptionDate
    current_datetime = timezone.now()
    

    if profile.subscriptionType:
        type = profile.subscriptionType
        if type == 'free':
            return 'Plan Validity: Free. Word Limit: 5000'
        elif type=='starter':

            if subDate >= current_datetime:
                
                next_date = current_datetime + relativedelta(months=1)
                next_month = returnMonth(next_date.month)
                year = next_date.year
                return 'Plan Validity: {} {} {}. Word Limit: 40000 Words'.format(next_date.day, next_month, year)
            
            elif subDate < current_datetime:
                profile.subscribed = False
                profile.subscriptionType = 'free'
                profile.save()
                return 'Plan Validity: Free. Word Limit: 5000'

            else:
                print('Error in fetching data')

        elif type == 'advanced':
            if subDate >= current_datetime:
                next_date = current_datetime + relativedelta(months=1)
                next_month = returnMonth(next_date.month)
                year = next_date.year
                return 'Plan Validity: {} {} {}. Word Limit: Unlimited Words'.format(next_date.day, next_month, year)
            
            elif subDate < current_datetime:
                profile.subscribed = False
                profile.subscriptionType = 'free'
                profile.save()
                return 'Plan Validity: Free. Word Limit: 5000'

            else:
                print('Error in fetching data')
    else:
        print('Some error occured')

        



from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='dashboard'),
    path('profile',views.profile,name='profile'),

    path('generate-blog-topic',views.blogTopic,name='blog-topic'),
    path('generate-blog-sections',views.blogSections,name='blog-sections'),

    path('save-blog-topic/<str:blogTopic>/',views.saveBlogTopic,name='save-blog-topic'),
    path('use-blog-topic/<str:blogTopic>/',views.useBlogTopic,name='use-blog-topic'),
    path('view-generated-blog/<slug:slug>/', views.viewGeneratedBlog, name ="view-generated-blog"),

    path('delete-blog-topic/<str:uniqueId>/',views.deleteBlogTopic,name='delete-blog-topic'),
    path('generate-blog-from-topic/<str:uniqueId>/',views.createBlogFromTopic,name='generate-blog-from-topic'),

    #Billing
    path('billing',views.billing,name='billing'),
    path('payment-success',views.PaymentSuccess,name='payment-success'),
]
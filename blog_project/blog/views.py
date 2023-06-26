from pdb import post_mortem
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import  BlogPostForm
from django.views.generic import UpdateView
from rest_framework.generics import UpdateAPIView
from django.contrib import messages
from .serializers import BlogPostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from blog import serializers
from rest_framework import generics









def blogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "blog/blog.html", {'posts':posts})

def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content','')
        blog_id =request.POST.get('blog_id','')
        comment = Comment(user = user, content = content, blog=post)
        comment.save()
    return render(request, "blog/blog_comments.html", {'post':post, 'comments':comments})
@login_required
def Delete_Blog_Post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        if request.user == post_mortem.author:

            posts.delete()
            return redirect('/')
        else:
            return HttpResponseForbidden("You are not allowed to delete this post.")


    return render(request, 'blog/delete_blog_post.html', {'posts':posts})

# # @login_required
# def delete_blog_post(request, slug):
#     post = get_object_or_404(BlogPost, slug=slug)

#     if request.method == "POST":
#         # Check if the authenticated user is the author of the post
#         if request.user == post.author:
#             post.delete()
#             return redirect('/')
#         else:
#             # User is not authorized to delete the post
#             return HttpResponseForbidden("You are not allowed to delete this post.")
    
#     return render(request, 'blog/delete_blog_post.html', {'post': post})

# def search(request):
#     if request.method == "POST":
#         searched = request.POST['searched']
#         blogs = BlogPost.objects.filter(title__contains=searched)
#         return render(request, "blog/search.html", {'searched':searched, 'blogs':blogs})
#     else:
#         return render(request, "blog/search.html", {})

@login_required(login_url = '/login')
def add_blogs(request):
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "blog/add_blogs.html",{'obj':obj, 'alert':alert})
    else:
        form=BlogPostForm()
    return render(request, "blog/add_blogs.html", {'form':form})

class UpdatePostAPI(UpdateAPIView):
    model = BlogPost
    # template_name = 'blog/edit_blog_post.html'
    # fields = ['title', 'slug', 'content', 'image']
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class BlogPostListAPIView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]


class BlogPostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]






class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'blog/edit_blog_post.html'
    fields = ['title','content', 'image']
    

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        print(pk)
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise serializers.ValidationError("Blog post does not exist.")

class BlogPostListCreateAPIView(ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

class BlogPostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]



# def user_profile(request, myid):
#     post = BlogPost.objects.filter(id=myid)
#     return render(request, "blog/user_profile.html", {'post':post})

# def Profile(request):
#     return render(request, "blog/profile.html")

# def edit_profile(request):
#     try:
#         profile = request.user.profile
#     except Profile.DoesNotExist:
#         profile = Profile.objects.create(user=request.user)
#     if request.method == "POST":
#         form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             alert = True
#             return render(request, "blog/edit_profile.html", {'alert': alert})
#     else:
#         form = ProfileForm(instance=profile)
#     return render(request, "blog/edit_profile.html", {'form': form})


def Register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'blog/login.html')   
    return render(request, "blog/register.html")

def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'blog/blog.html')   
    return render(request, "blog/login.html")

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')
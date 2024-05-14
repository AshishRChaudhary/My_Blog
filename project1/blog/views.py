from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render,get_object_or_404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PostForm,CommentForm
from django.views.generic import TemplateView,ListView,DetailView,CreateView, UpdateView, DeleteView
from.models import Post,Comment
# Create your views here.

class HomeView(TemplateView):
    template_name= "home.html"
    

class PostListView(ListView):
    model= Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
class PostDetailView(DetailView):
    model= Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url="/login/" #if not login will take u to login page
    redirect_field_name="blog/post_detail.html" #after login will take to detail of the post
    form_class=PostForm #form to use while creating post after login
    model=Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url="/login/" #if not login will take u to login page
    redirect_field_name="blog/post_detail.html" #after login will take to detail of the post
    form_class=PostForm #form to use while creating post after login
    model=Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model= Post
    success_url= reverse_lazy("post_list")

class DraftListView(LoginRequiredMixin,ListView):
    login_url="/login/"
    redirect_field_name="blog/post_list.html"
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    

######## func based views for comment section ##############
####################################################


@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comments_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk) #line A - storing all Post model data
    if request.method=='POST':
        form =  CommentForm(request.POST) #storing feilds in form variable along with filled values by the user
        if form.is_valid():
            comment= form.save(commit=False) #saving form data in "comment" without commiting to DB
            comment.post = post #grabbing post attribute(foreign key) and saving objects from Post Model (post from line A)
            comment.save() #commiting the values in DB
            return redirect('post_detail', pk= post.pk) #going to post_detail named url and keeping pk intact as earlier
    else:
        form=CommentForm()
    return render (request, 'blog/comment_form.html',{'form':form})    

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment, pk=pk) 
    comment.approve()# approve method in Comment model is called
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment, pk=pk) 
    post_pk=comment.post.pk #storing pk of post before deleting
    comment.delete()
    return redirect('post_detail', pk=post_pk)


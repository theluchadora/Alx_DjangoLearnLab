from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Tag
from django.utils.text import slugify

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created succesfully for {username} you can login now!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.alert(request, f'Update successfully!')
            return redirect('profile')  # stay on the same page after update
    else:
        form = ProfileUpdateForm(instance=request.user)
    # Get posts of the logged-in user
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')

    context = {
        'form': form,
        'user_posts': user_posts
    }
    return render(request, 'blog/profile.html', context)


# LoginRequiredMixin ensures only logged-in users can create, edit, or delete.
# UserPassesTestMixin ensures only the post author can edit/delete.

from django.db.models import Q
from django.views.generic import ListView

#Tag list view & search view
class TaggedPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # reuse list template
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=slug)
        return tag.posts.order_by('-published_date')

def search(request):
    q = request.GET.get('q', '').strip()
    queryset = Post.objects.none()
    if q:
        queryset = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by('-published_date')
    return render(request, 'blog/search_results.html', {'posts': queryset, 'query': q})


# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5  # optional pagination

# View post details
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)  # creates post
        # handle tags
        tag_names = form.cleaned_data.get('tags_field', '')
        self.object.tags.clear()
        for t in [n.strip() for n in tag_names.split(',') if n.strip()]:
            tag_obj, _ = Tag.objects.get_or_create(name=t, slug=slugify(t))
            self.object.tags.add(tag_obj)
        return response

# Update a post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # same tag handling
        tag_names = form.cleaned_data.get('tags_field', '')
        self.object.tags.clear()
        for t in [n.strip() for n in tag_names.split(',') if n.strip()]:
            tag_obj, _ = Tag.objects.get_or_create(name=t, slug=slugify(t))
            self.object.tags.add(tag_obj)
        return response
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Create a comment
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']  # pk(kinda id) from URL
        return super().form_valid(form)

# Update a comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

# Delete a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()
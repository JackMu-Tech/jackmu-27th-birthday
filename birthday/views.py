from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Birthday, BirthdayMessage, BirthdayCard, Event, Gift, Photo

from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.db.models import Count
from django.views.generic import ListView
from .forms import EmailPostForm
from taggit.models import Tag
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

@login_required
def home(request):
    # Fetch necessary data from models
    birthdays = Birthday.objects.all()
    messages = BirthdayMessage.objects.all()
    cards = BirthdayCard.objects.all()
    events = Event.objects.all()
    gifts = Gift.objects.all()
    photos = Photo.objects.all()

    # Pass data to template and render it
    return render(request, 'birthday/home.html', {'birthdays': birthdays, 'messages': messages, 'cards': cards, 'events': events, 'gifts': gifts, 'photos': photos})

@login_required
def about(request):
    # Add logic to fetch data or perform other actions related to the About page
    return render(request, 'birthday/about.html')

@login_required
def events(request):
    # Add logic to fetch data or perform other actions related to the Events page
    return render(request, 'birthday/events.html')

@login_required
def gallery(request):
    # Add logic to fetch data or perform other actions related to the Gallery page
    return render(request, 'birthday/gallery.html')

@login_required
def contact(request):
    # Add logic to fetch data or perform other actions related to the Contact page
    return render(request, 'birthday/contact.html')



class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'birthday/list.html'

def post_list(request, tag_slug=None):
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1)

    try:
        posts = paginator.page(page_number)
    
    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'birthday/list.html',{'posts':posts,'tag':tag})

def post_detail(request,year, month,day,post):
    post = get_object_or_404(Post, status = Post.Status.PUBLISHED,
            slug = post, publish__year = year, publish__month = month,
                    publish__day = day)
    

    
    # List of similar posts
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids.exclude(id=post.id))
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]


    return render(request, 'birthday/detail.html', {'post':post,'similar_posts':similar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id,status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject,message,'chief.jackson99@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'birthday/share.html',{'post':post, 'form':form, 'sent':sent})


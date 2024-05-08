from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class Birthday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s birthday on {self.date_of_birth}"

class BirthdayMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Birthday, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.user.username} ({self.date_sent})"

class BirthdayCard(models.Model):
    sender = models.ForeignKey(User, related_name='sent_cards', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_cards', on_delete=models.CASCADE)
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card from {self.sender.username} to {self.recipient.username} ({self.sent_date})"

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Gift(models.Model):
    recipient = models.ForeignKey(User, related_name='received_gifts', on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    description = models.TextField()
    date_given = models.DateField()

    def __str__(self):
        return f"Gift from {self.sender} to {self.recipient.username} ({self.date_given})"

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='birthday_photos/')
    caption = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo uploaded by {self.user.username} ({self.upload_date})"


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISHED)

class Post(models.Model):

    tags = TaggableManager()

    class Status(models.TextChoices):
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250, unique_for_date = 'publish')
    author = models.ForeignKey(User,on_delete = models.CASCADE, related_name = 'birthday_posts')
    body = models.TextField()
    publish  = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('birthday:post_detail',args = [self.publish.year,self.publish.month,
                                                self.publish.day, self.slug])


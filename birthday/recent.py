import markdown
from.models import Post
from django.urls import reverse_lazy
from django.template.defaultfilters import truncatewords_html
from django.contrib.syndication.views import Feed

class LatestBirthDayFeed(Feed):
    title = "The 27TH Birthday of JackMu"
    link = reverse_lazy('birthday:post_list')
    description = 'Latest posts of JackMu Birthday'
    
    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title
    
    def item_description(self,item):
        return truncatewords_html(markdown.markdown(item.body),30)

    def item_pubdate(self, item):
        return item.publish

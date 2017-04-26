from django.conf.urls import *
from . import views
urlpatterns =[
	url(r'^$',views.post_tweet,name='post_tweet'),
	url(r'^thankyou',views.thank_you,name='thankyou'),
	url(r'^edit/(?P<tweet_id>\d+)',views.post_tweet,name='posttweet'),
	]
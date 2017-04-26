from django.conf.urls import *
from . import views
urlpatterns=[
	url(r'^$',views.list_tweets,name='list_tweets'),
	url(r'^review/(?P<tweet_id>\d+)$',views.review_tweet,name='review_tweet'),
	]
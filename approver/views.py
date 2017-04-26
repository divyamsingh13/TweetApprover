from django.shortcuts import render
from datetime import datetime
from django import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required

from twython import Twython
from myproject import settings
from poster.views import *
from poster.models import Tweet, Comment

# Create your views here.
@permission_required('poster.can_approve_or_reject_tweet',
	login_url='/login')
def list_tweets(request):
	pending_tweets=Tweet.objects.filter(state='pending').order_by('created_at')
	published_tweets=Tweet.objects.filter(state='published').order_by('-published_at')
	return render(request,'list_tweets.html',{'pending_tweets':pending_tweets,
		'published_tweets':published_tweets})


class ReviewForm(forms.Form):
	new_comment=forms.CharField(max_length=300,widget=forms.Textarea(attrs={'cols':50,'rows':6}),required=False)
	APPROVAL_CHOICES=(
		('approve','aprove this tweet and post'),
		('reject','reject this tweet and send to author with comment'))
	approval=forms.ChoiceField(choices=APPROVAL_CHOICES,widget=forms.RadioSelect)

@permission_required('poster.can_approve_or_reject_tweet',
	login_url='/login')
def review_tweet(request,tweet_id):
	reviewed_tweet=get_object_or_404(Tweet,id=tweet_id)
	if(request.method=='POST'):
		form=ReviewForm(request.POST)
		if form.is_valid():
			new_comment=form.cleaned_data['new_comment']
			if form.cleaned_data['approval']=='approve':
				send_approval_mail(reviewed_tweet,new_comment)
				publish_tweet(reviewed_tweet)
				
				reviewed_tweet.published_at=datetime.now()
				reviewed_tweet.state='published'
			else:
				link=request.build_absolute_uri(
					reverse(post_tweet,args=[reviewed_tweet.id]))
				send_rejection_mail(reviewed_tweet,new_comment,link)
				reviewed_tweet.state='rejected'
			reviewed_tweet.save()
			if new_comment:
				c=Comment(tweet=reviewed_tweet,text=new_comment)
				c.save()
			return HttpResponseRedirect('/approve/')
	else:
		form=ReviewForm()
	return render(request,'review_tweet.html',{'form':form,'tweet':reviewed_tweet,
		'comments':reviewed_tweet.comment_set.all()})

def send_approval_mail(tweet,new_comment):
	body=['Your tweet (%r) was approved and published on twitter.'%tweet.text]
	if new_comment:
		body.append(
			'the reviewer gave this feedback : %r .'%new_comment)
		body=str(body)
		# send_mail('Tweet published','%s\r\n' % (' '.join(body)),settings.DEFAULT_FROM_EMAIL,[tweet.author_email])
		send_mail('Tweet published',body,settings.DEFAULT_FROM_EMAIL,[tweet.author_email])

def send_rejection_mail(tweet,new_comment,link):
	body=['Your tweet (%r) was rejected \n' %tweet.text]
	if new_comment:
		body.append(
			'the reviewer gave this feedback : %r .'%new_comment)
		body.append(
			'the edit tweet : %s .'% link)
		body=str(body)
		send_mail('Tweet rejected',body,settings.DEFAULT_FROM_EMAIL,[tweet.author_email])

def publish_tweet(tweet):
	twitter=Twython(
		
			app_key=settings.TWITTER_CONSUMER_KEY,
			app_secret=settings.TWITTER_CONSUMER_SECRET,
			oauth_token=settings.TWITTER_OAUTH_TOKEN,
			oauth_token_secret=settings.TWITTER_OAUTH_TOKEN_SECRET,
			)
	twitter.update_status(status=tweet.text.encode("utf-8"))
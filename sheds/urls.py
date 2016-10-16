from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<day>all)$', views.index),
    url(r'^(?P<day>today)$', views.index),
    url(r'^monday$', views.index, kwargs={'day': 0}),
    url(r'^tuesday$', views.index, kwargs={'day': 1}),
    url(r'^wednesday$', views.index, kwargs={'day': 2}),
    url(r'^thursday$', views.index, kwargs={'day': 3}),
    url(r'^friday$', views.index, kwargs={'day': 4}),
    url(r'^saturday$', views.index, kwargs={'day': 5}),
    url(r'^sunday$', views.index, kwargs={'day': 6}),
    url(r'^day/(?P<day>.*)$', views.index),
    url(r'^bot/(?P<bot_token>.+)$', views.TelegramBotReceiverView.as_view()),
]

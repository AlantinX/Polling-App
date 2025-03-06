from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from .views import PollList, Vote, NewPoll, DeletePoll

app_name = 'polls'

urlpatterns = [
    path('', PollList.as_view(), name='index'),
    path('vote/<int:pk>/', Vote.as_view(), name='vote'),
    path('new/', NewPoll.as_view(), name='new_poll'),
    path('delete/<int:pk>/', DeletePoll.as_view(), name='delete_poll'),
]


urlpatterns += staticfiles_urlpatterns()
from django.urls import path

from postings.views import PostingView, PostsView


urlpatterns = [
    path('', PostingView.as_view()),
    path('/<int:posting_id>', PostingView.as_view()),
    path('/list', PostsView.as_view())
]
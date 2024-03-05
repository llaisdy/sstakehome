from django.urls import path

from .views import PoIListView

urlpatterns = [
    path('', PoIListView.as_view()),
]

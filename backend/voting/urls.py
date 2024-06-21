from django.urls import path

from .views import positions_list, vie_for_position, vote, results

urlpatterns = [
    path('positions/', positions_list, name='positions_list'),
    path('vie_for_position/<int:position_id>/', vie_for_position, name='vie_for_position'),
    path('vote/<int:position_id>/', vote, name='vote'),
    path('results/', results, name='results'),
]
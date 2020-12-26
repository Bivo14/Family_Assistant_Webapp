from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name="home"),

    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('account/', views.accountSettings, name="account"),

    path('memories/', views.memoriesPage, name="memories"),
    path('upload_memory/', views.uploadImage, name="upload_memory"),
    path('delete_memory/<str:pk>', views.removeImage, name="delete_memory"),
    path('update_memory/<str:pk>', views.updateMemory, name="update_memory"),
    path('comment/<str:pk>', views.addComment, name="comment_to_memory"),


    path('add_child_item/<str:pk>', views.addItem, name="addChildItem"),
    path('view_lists/<str:pk>', views.viewItems, name="viewLists"),
    path('delete_item/<str:pk>', views.removeItem, name="delete_item"),
    path('tick_item/<str:pk>', views.checkItem, name="tick_item"),

    path('add_personal_event/<str:pk>', views.addPersonalEvent, name="addPersonalEvent"),
    path('view_personal_events/<str:pk>', views.viewPersonalEvents, name="viewPersonalEvents"),
    path('delete_personal_event/<str:pk>', views.removePersonalEvent, name="delete_personal_events"),
    path('tick_personal_event/<str:pk>', views.checkPersonalEvent, name="tick_personal_event"),


    path('travel/', views.calculate_distance_view, name="travel"),
    path('delete_travel/<str:pk>', views.removeTravel, name="delete_travel"),
    path('vote_travel/<str:pk>', views.VoteView, name="vote_travel"),
    path('unvote_travel/<str:pk>', views.UnVoteView, name="unvote_travel"),
    path('approve_travel/<str:pk>', views.approveTravel, name="approve_travel"),

    path('schedule/', views.CalendarView.as_view(), name="schedule"),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<event_id>/', views.event, name='event_edit'),
]


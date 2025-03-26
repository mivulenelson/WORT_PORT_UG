from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),
    path("all-buses/", views.all_buses, name="all-buses"),
    path("all-tickets/", views.all_tickets, name="all-tickets"),
    path("all-services/", views.all_services, name="all-services"),
    path("archived-tickets/", views.view_archived_tickets, name="archived-tickets"),
    path("archived-books/<str:bus_id>/", views.view_archived_books, name="archived-books"),
    path("bus-tickets/<str:bus_id>/", views.all_bus_tickets, name="bus-tickets"),

    # all creations urls
    path("enter-bus/", views.enter_bus, name="bus"),
    path("book-ticket/", views.book_bus, name="book"),
    path("create-service/", views.service_create_view, name="enter-service"),
    path("attachment/<str:book_id>/", views.attachment_create_view, name="attach"),

    # all update urls
    path("update-ticket/<str:book_id>/", views.book_update_view, name="update-ticket"),
    path("update-bus/<str:bus_id>/", views.bus_update_view, name="update-bus"),
    path("update-service/<str:service_id>/", views.service_update_view, name="update-service"),
    path("update-bus/<str:bus_id>/", views.update_archived_bus, name="update-archived"),

    # All details urls
    path("bus-details/<str:bus_id>/", views.bus_details_views, name="bus-details"),
    path("book-details/<str:book_id>/", views.book_details_view, name="book-details"),
    path("service-details/<str:service_id>/", views.service_details_view, name="service-details"),
    path("attach-details/<str:book_id>/", views.attachment_details, name="attach-details"),

    # All delete urls
    path("delete-ticket/<str:book_id>/", views.delete_book_view, name="delete-ticket"),
    path("delete-bus/<str:bus_id>/", views.delete_bus_view, name="delete-bus"),
    path("delete-service/<str:service_id>/", views.delete_service_view, name="delete-service"),
]


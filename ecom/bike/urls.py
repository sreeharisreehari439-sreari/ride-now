from django.urls import path
from . import views
urlpatterns =[
    path('',views.home,name="home"),
    path('login/',views.login_view,name="login"),
    path('register/',views.register,name="register"),
    path("admin-dashboard/",views.admin_dashboard,name="admin_dashboard"),
    path("logout/",views.logout_view,name="logout"),
    path("user-dashboard/",views.user_dashboard,name="user_dashboard"),
    path("add-bike/",views.add_bike,name="add_bike"),path("bikes/",views.bike_list,name="bike_list"),
    path("bike/<int:bike_id>/",views.bike_detail,name="bike_detail"),
    path("add-category/",views.add_category,name="add_category"),
    path('bike/<int:bike_id>/', views.bike_detail, name='bike_detail'),
    path('book/<int:bike_id>/', views.book_now, name='book_now'),

    path('my-orders/', views.my_orders, name='my_orders'),
    path('admin-dashboard/orders/', views.admin_orders, name='admin_orders'),

    path('admin-dashboard/orders/approve/<int:order_id>/',
        views.approve_order,
        name='approve_order'),

    path('admin-dashboard/orders/reject/<int:order_id>/',
        views.reject_order,
        name='reject_order'),
    path('bikes/', views.all_bikes, name='all_bikes'),    

]
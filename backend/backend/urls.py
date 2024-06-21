"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from admin_section.views import *
from django.conf import settings
from django.conf.urls.static import static
from admin_section.views import add_room

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_page/',login_view,name="login_page"),
    path('home/',home,name="home"),
    path('menu_category/',category_input,name='menu_category'),
    path('create_product/',create_product,name='create_product'),
    path('register/',register,name="register"),
    path('send_registration_email/',send_registration_email,name="send_registration_email"),
    path('registration_success/',registration_success,name="registration_success"),
    path('generate_and_register_user/',generate_and_register_user,name='generate_and_register_user'),
    path('CustomLoginView/',CustomLoginView.as_view(),name='CustomLoginView'),
    path('member_logout/', logout_view, name='member_logout'),
    path('home_page/',homepage,name='homepage'),
    path('register_waiter/',register_waiter,name='register_waiter'),
    path('waiter_success/',waiter_success,name='waiter_success'),
    path('addfoodmenu/',addfoodmenu,name="addfoodmenu"),
    path('addroomadmin/',addroomadmin,name="addroomadmin"),
    path('landingpage/',landingpage,name='landingpage'),
    path('adminmemberspage/',adminmemberspage,name='adminmemberspage'),
    path('adminwaiterspage/',adminwaiterspage,name='adminwaiterspage'),

    path('upload/', upload_image, name='upload_image'),
    path('success/', image_success, name='image_success'),
    path('send-registration-link/', send_registration_link, name='send_registration_link'),
    path('add_room/', add_room, name='add_room'),
    path('member_home/',member_home,name='member_home'),
    path('dine/',dine,name='dine'),
    path('room/',room,name='room'),
    path('waiter_login/',waiter_login,name='waiter_login'),
    path('member_logout/',member_logout,name='member_logout'),
    path('', include('members.urls')),
    path('', include('voting.urls')),
    path('categories/', category_list, name='category_list'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('room/<int:room_id>/', room_detail, name='room_detail'),
    path('book/', book_room, name='book_room'),
    path('waiter_home/', waiter_home, name='waiter_home'),
    path('waiter_leaderboard/', waiter_leaderboard, name='waiter_leaderboard'),
    path('waiter_order/', waiter_order, name='waiter_order'),
    path('chatbot/', include('chatbot.urls')),
    path('mpesa-stk-push/', MpesaStkPushView.as_view(), name='mpesa_stk_push'),
    path('transaction-success/', lambda request: render(request, 'transaction_success.html'), name='transaction_success'),
    path('transaction-failure/', lambda request: render(request, 'transaction_failure.html'), name='transaction_failure'),
    path('adminmenu/edit/<int:product_id>/', edit_product, name='edit_product'),
    path('adminmenu/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('',landing_page,name='landing_page'),
    path('gallery/',gallery,name='gallery'),
    path('logins/',logins,name='logins'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

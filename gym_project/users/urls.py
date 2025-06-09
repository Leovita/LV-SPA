from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users.views.home import home
from users.views.auth import profile, login, register, user_logout, change_password_view
from users.views.profile import profile_view, update_profile, update_profile_picture, delete_account
from users.views.booking import book_gym_class, book_spa_service, my_bookings, cancel_gym_booking, cancel_spa_booking
from users.views.courses import gest_corsi, delete_course, add_course, course_details, edit_course
from users.views.admin import gest_prenotazioni, admin_delete_booking, booking_details, edit_booking

urlpatterns = [
    path('', home, name='home'),  
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/update-picture/', update_profile_picture, name='update_profile_picture'),
    path('profile/change-password/', change_password_view, name='change_password'),
    path('profile/delete-account/', delete_account, name='delete_account'),
    path('gest-prenotazioni/', gest_prenotazioni, name='gest_prenotazioni'),
    path('book-gym/<int:class_id>/', book_gym_class, name='book_gym'),
    path('book-spa/<int:service_id>/', book_spa_service, name='book_spa'),
    path('login/', login, name='login'), 
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('gest-corsi/', gest_corsi, name='gest_corsi'),
    path('cancel-gym-booking/<int:booking_id>/', cancel_gym_booking, name='cancel_gym_booking'),
    path('cancel-spa-booking/<int:booking_id>/', cancel_spa_booking, name='cancel_spa_booking'),
    path('admin-delete-booking/', admin_delete_booking, name='admin_delete_booking'),
    path('delete-course/<str:type>/<int:id>/', delete_course, name='delete_course'),
    path('add-course/', add_course, name='add_course'),
    path('course-details/<str:type>/<int:id>/', course_details, name='course_details'),
    path('edit-course/<str:type>/<int:id>/', edit_course, name='edit_course'),
    path('booking-details/<str:type>/<int:id>/', booking_details, name='booking_details'),
    path('edit-booking/<str:type>/<int:id>/', edit_booking, name='edit_booking'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

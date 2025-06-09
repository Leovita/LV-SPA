from users.views.auth import profile, login, register, user_logout, change_password_view
from users.views.profile import profile_view, update_profile, update_profile_picture, delete_account
from users.views.booking import book_gym_class, book_spa_service, my_bookings, cancel_gym_booking, cancel_spa_booking
from users.views.courses import gest_corsi, delete_course, add_course, course_details, edit_course
from users.views.admin import gest_prenotazioni, admin_delete_booking, booking_details, edit_booking
from users.views.home import home
from users.views.utils import ajax_ok, ajax_error

__all__ = [
    'home',
    'profile', 'login', 'register', 'user_logout', 'change_password_view',
    'profile_view', 'update_profile', 'update_profile_picture', 'delete_account',
    'book_gym_class', 'book_spa_service', 'my_bookings', 'cancel_gym_booking', 'cancel_spa_booking',
    'gest_corsi', 'delete_course', 'add_course', 'course_details', 'edit_course',
    'gest_prenotazioni', 'admin_delete_booking', 'booking_details', 'edit_booking',
    'ajax_ok', 'ajax_error'
]
# Altri import verranno aggiunti man mano che modularizziamo le altre view 
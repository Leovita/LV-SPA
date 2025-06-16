from .auth import profile, login, register, user_logout, change_password_view
from .profile import profile_view, update_profile, update_profile_picture, delete_account
from .booking import my_bookings
from .courses import gest_corsi, delete_course, add_course, course_details, edit_course
from .admin import gest_prenotazioni, admin_delete_booking, booking_details, edit_booking
from .home import home
from .utils import ajax_ok, ajax_error

__all__ = [
    'home',
    'profile', 'login', 'register', 'user_logout', 'change_password_view',
    'profile_view', 'update_profile', 'update_profile_picture', 'delete_account',
    'my_bookings',
    'gest_corsi', 'delete_course', 'add_course', 'course_details', 'edit_course',
    'gest_prenotazioni', 'admin_delete_booking', 'booking_details', 'edit_booking',
    'ajax_ok', 'ajax_error'
]
# Altri import verranno aggiunti man mano che modularizziamo le altre view 
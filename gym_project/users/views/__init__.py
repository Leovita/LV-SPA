from .auth import *
from .courses import *
from .home import *
from .profile import *
from .admin import *

__all__ = [
    'home',
    'profile', 'login', 'register', 'user_logout', 'change_password_view',
    'profile_view', 'update_profile', 'update_profile_picture', 'delete_account',
    'book_gym_class', 'book_spa_service', 'my_bookings', 'cancel_gym_booking', 'cancel_spa_booking',
    'gest_corsi', 'delete_course', 'add_course', 'course_details', 'edit_course',
    'gest_prenotazioni', 'admin_delete_booking', 'booking_details', 'edit_booking'
]
# Altri import verranno aggiunti man mano che modularizziamo le altre view 
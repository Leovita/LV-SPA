from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from palestra.models import GymClass
from spa.models import SpaService
from users.models import User
from users.views.utils import ajax_error, ajax_ok
from django.utils import timezone
from dateutil import parser
import json
from django.http import JsonResponse
from datetime import datetime

@login_required
@user_passes_test(lambda u: u.is_staff)
def gest_corsi(req):
    now = timezone.now()
    gym = GymClass.objects.filter(scheduled__gte=now)
    spa = SpaService.objects.filter(scheduled__gte=now)
    all_corsi = list(gym) + list(spa)
    instructors = User.objects.filter(is_staff=True)
    ctx = {
        'gym_courses': gym,
        'spa_services': spa,
        'all_courses': all_corsi,
        'total_gym_courses': gym.count(),
        'total_spa_services': spa.count(),
        'instructors': instructors,
    }
    return render(req, 'users/gest_corsi.html', ctx)

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["DELETE"])
def delete_course(request, type, id):
    try:
        if type == 'gym':
            course = GymClass.objects.get(id=id)
        elif type == 'spa':
            course = SpaService.objects.get(id=id)
        else:
            return ajax_error('Il tipo di corso non è valido (gym o spa)')
        try:
            course.delete()
            return ajax_ok('Corso eliminato con successo')
        except Exception as e:
            return ajax_error(str(e))

    except (GymClass.DoesNotExist, SpaService.DoesNotExist):
        return ajax_error('Corso non trovato')
    except Exception as e:
        return ajax_error(str(e))

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
@require_http_methods(["POST"])
def add_course(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    try:
        course_type = request.POST.get('type')
        name = request.POST.get('name')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        instructor_id = request.POST.get('instructor')
        image = request.FILES.get('image')
        max_partecipants = request.POST.get('max_partecipants')
        scheduled = request.POST.get('scheduled')

        if not all([course_type, name, description, duration, instructor_id, image, scheduled]):
            if is_ajax:
                return ajax_error("Tutti i campi obbligatori devono essere compilati.")
            messages.error(request, "Tutti i campi obbligatori devono essere compilati.")
            return redirect('gest-corsi')

        instructor = User.objects.filter(id=instructor_id).first()
        if not instructor:
            if is_ajax:
                return ajax_error("Istruttore/Operatore non valido.")
            messages.error(request, "Istruttore/Operatore non valido.")
            return redirect('gest-corsi')

        try:
            scheduled_dt = timezone.make_aware(datetime.strptime(scheduled, '%Y-%m-%dT%H:%M'))
        except ValueError:
            if is_ajax:
                return ajax_error("Formato data e ora non valido.")
            messages.error(request, "Formato data e ora non valido.")
            return redirect('gest-corsi')

        if course_type == 'gym':
            if not max_partecipants:
                if is_ajax:
                    return ajax_error("Capacità massima richiesta per i corsi palestra.")
                messages.error(request, "Capacità massima richiesta per i corsi palestra.")
                return redirect('gest-corsi')
            try:
                max_partecipants_int = int(max_partecipants)
                if max_partecipants_int < 1:
                    raise ValueError
            except (TypeError, ValueError):
                return ajax_error("Capacità massima richiesta per i corsi palestra (deve essere almeno 1).")
            try:
                new_course = GymClass.objects.create(
                    name=name,
                    description=description,
                    duration=duration,
                    instructor=instructor,
                    max_partecipants=max_partecipants_int,
                    imgs=image,
                    scheduled=scheduled_dt
                )
            except Exception as e:
                return ajax_error("Errore durante la creazione del corso.")

            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': f"Corso palestra '{name}' aggiunto con successo.",
                    'course': {
                        'id': new_course.id,
                        'name': new_course.name,
                        'description': new_course.description,
                        'duration': new_course.duration,
                        'instructor': instructor.full_name if instructor else '',
                        'instructor_id': instructor.id if instructor else '',
                        'max_partecipants': new_course.max_partecipants,
                        'scheduled': new_course.scheduled.strftime('%Y-%m-%dT%H:%M'),
                        'type': 'gym',
                        'status': 'active',
                        'image_url': new_course.imgs.url if new_course.imgs else '',
                    }
                })
            messages.success(request, f"Corso palestra '{name}' aggiunto con successo.")

        elif course_type == 'spa':
            price = request.POST.get('price')
            spa_type = request.POST.get('spa_type')
            if not price:
                if is_ajax:
                    return ajax_error("Prezzo richiesto per i servizi spa.")
                messages.error(request, "Prezzo richiesto per i servizi spa.")
                return redirect('gest-corsi')

            new_service = SpaService.objects.create(
                name=name,
                description=description,
                operator=instructor,
                duration=duration,
                price=price,
                imgs=image,
                max_partecipants=max_partecipants if max_partecipants else 1,
                scheduled=scheduled_dt,
                type=spa_type or 'massage'
            )
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': f"Servizio spa '{name}' aggiunto con successo.",
                    'service': {
                        'id': new_service.id,
                        'name': new_service.name,
                        'description': new_service.description,
                        'duration': new_service.duration,
                        'operator': instructor.full_name if instructor else '',
                        'operator_id': instructor.id if instructor else '',
                        'price': new_service.price,
                        'scheduled': new_service.scheduled.strftime('%Y-%m-%dT%H:%M'),
                        'type': spa_type or '',
                        'status': 'active',
                        'image_url': new_service.imgs.url if new_service.imgs else '',
                    }
                })
            messages.success(request, f"Servizio spa '{name}' aggiunto con successo.")

        else:
            if is_ajax:
                return ajax_error("Tipo corso/servizio non valido.")
            messages.error(request, "Tipo corso/servizio non valido.")
            return redirect('gest-corsi')

        if not is_ajax:
            return redirect('gest-corsi')
        return ajax_ok('Operazione completata con successo.')

    except Exception as e:
        if is_ajax:
            return ajax_error(f"Errore durante l'aggiunta: {str(e)}")
        messages.error(request, f"Errore durante l'aggiunta: {str(e)}")
        return redirect('gest-corsi')

@login_required
@user_passes_test(lambda u: u.is_staff)
def course_details(request, type, id):
    try:
        if type == 'gym':
            course = get_object_or_404(GymClass, id=id)
            template = 'gym_course_details.html'
        elif type == 'spa':
            course = get_object_or_404(SpaService, id=id)
            template = 'spa_service_details.html'
        else:
            messages.error(request, "Tipo di corso non valido")
            return redirect('gest-corsi')

        return render(request, template, {'course': course})
    except Exception as e:
        messages.error(request, f"Errore nel caricamento dei dettagli: {str(e)}")
        return redirect('gest-corsi')

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def edit_course(request, type, id):
    try:
        if type == 'gym':
            course = get_object_or_404(GymClass, id=id)
        elif type == 'spa':
            course = get_object_or_404(SpaService, id=id)
        else:
            return ajax_error('Tipo non valido')

        name = request.POST.get('name')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        instructor_id = request.POST.get('instructor')
        scheduled = request.POST.get('scheduled')
        image = request.FILES.get('image')

        if not all([name, description, duration, instructor_id, scheduled]):
            return ajax_error("Tutti i campi obbligatori devono essere compilati.")

        instructor = User.objects.filter(id=instructor_id).first()
        if not instructor:
            return ajax_error("Istruttore/Operatore non valido.")

        try:
            scheduled_dt = timezone.make_aware(datetime.strptime(scheduled, '%Y-%m-%dT%H:%M'))
        except ValueError:
            return ajax_error("Formato data e ora non valido.")

        course.name = name
        course.description = description
        course.duration = duration
        course.scheduled = scheduled_dt
        if image:
            course.imgs = image

        if type == 'gym':
            max_partecipants = request.POST.get('max_partecipants')
            course.max_partecipants = int(max_partecipants) if max_partecipants else 1
            course.instructor = instructor
        else:
            price = request.POST.get('price')
            max_partecipants = request.POST.get('max_partecipants')
            course.price = price
            course.operator = instructor
            course.type = request.POST.get('spa_type') or 'massage'
            course.max_partecipants = int(max_partecipants) if max_partecipants else 1

        course.save()

        return JsonResponse({
            'success': True,
            'message': f"{'Corso' if type == 'gym' else 'Servizio'} modificato con successo.",
            'course': {
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'duration': course.duration,
                'instructor': instructor.full_name if instructor else '',
                'instructor_id': instructor.id if instructor else '',
                'scheduled': course.scheduled.strftime('%Y-%m-%dT%H:%M'),
                'status': 'active',
                'image_url': course.imgs.url if course.imgs else '',
                'type': type,
                **({'max_partecipants': course.max_partecipants} if type == 'gym' else {'price': course.price})
            }
        })

    except Exception as e:
        return ajax_error(f"Errore durante la modifica: {str(e)}") 
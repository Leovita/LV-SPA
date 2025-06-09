from django.http import JsonResponse

def ajax_error(err_message):
    return JsonResponse({'success': False, 'error': err_message})

def ajax_ok(mess_ok):
    return JsonResponse({'success': True, 'message': mess_ok}) 
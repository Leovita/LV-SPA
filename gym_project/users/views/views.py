from django.http import JsonResponse

def ajax_ok(message, data=None):
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    return JsonResponse(response)

def ajax_error(message, data=None):
    response = {'success': False, 'message': message}
    if data is not None:
        response['data'] = data
    return JsonResponse(response) 
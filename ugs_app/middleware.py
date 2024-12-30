from django.utils.deprecation import MiddlewareMixin

class ReferrerPolicyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # print(request)
        response['X-Frame-Options'] = 'ALLOWALL'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response
from django.views.generic.base import View

from braces.views import JSONResponseMixin, CsrfExemptMixin


class ApiAuthView(CsrfExemptMixin, JSONResponseMixin, View):
    """
    Returns user_id if user is authenticated.
    """
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            result = {'success': True,
                      'user_id': request.user.id,
                      'is_staff': request.user.is_staff}
        else:
            result = {'success': False}

        return self.render_json_response(result)

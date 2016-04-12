class RequestBridge(object):
    """Request bridge with project's interface.
    """
    def __init__(self, django_request):
        self.django_request = django_request

    @property
    def user(self):
        return self.django_request.user

    @property
    def query_params(self):
        return self.django_request.query_params


class LogicViewMixin(object):
    """View mixin that adds business logic to derived view as 'logic' property.
    It must be inherited by views that use business logic. Business logic must be written in
    separate class that is derived from 'BaseLogic' and must be in the view as
    'logic_class' attribute.
    """
    __logic_instance = None

    @property
    def logic(self):
        if not self.__logic_instance:
            request_bridge = RequestBridge(django_request=self.request)

            self.__logic_instance = self.logic_class(request_bridge=request_bridge)

        return self.__logic_instance


class BaseLogic(object):
    """Class that adds request obj bridge to our interface as 'request' attribute.
    It must be inherited by classes with business logic.
    """
    def __init__(self, request_bridge):
        self.request = request_bridge

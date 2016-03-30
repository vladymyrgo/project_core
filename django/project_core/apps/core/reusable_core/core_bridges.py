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


class LogicBridgeView(object):
    """Abstract view that adds business logic to derived view as 'logic' property.
    It must be inherited by views that use business logic. Business logic must be written in
    separate class that is derived from 'BaseLogic' and must be in the view as
    'logic_class' attribute.
    """
    logic_instance = None

    @property
    def logic(self):
        if not self.logic_instance:
            request_bridge = RequestBridge(django_request=self.request)

            self.logic_instance = self.logic_class(request_bridge=request_bridge)

        return self.logic_instance


class BaseLogic(object):
    """Abstract class that adds request obj bridge with our interface as 'request' attribute.
    It must be inherited by classes with business logic.
    """
    def __init__(self, request_bridge):
        self.request = request_bridge

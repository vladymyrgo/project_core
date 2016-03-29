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
    """Abstract view that adds business logic to derived view as 'logic' attribute.
    It must be inherited by views that use business logic. Business logic must be written in
    separate class that is derived from 'BaseLogic'.
    """
    def __init__(self):
        request_bridge = RequestBridge(django_request=self.request)

        self.logic = self.logic_view(request_bridge=request_bridge)


class BaseLogic(object):
    """Abstract class that adds request obj bridge with our interface as 'request' attribute.
    It must be inherited by classes with business logic.
    """
    def __init__(self, request_bridge):
        self.request = request_bridge

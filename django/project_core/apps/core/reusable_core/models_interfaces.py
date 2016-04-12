class CoreInterface(object):
    # _required_attributes must be specified

    def __getattr__(self, name):
        if name in self._required_attributes:
            msg = "'{}' is not implemented".format(name)
            raise NotImplementedError(msg)
        else:
            cls = type(self)
            msg = "'{}' object has no attribute '{}'".format(cls.__name__, name)
            raise AttributeError(msg)


class CoreModelInterface(CoreInterface):

    def __unicode__(self):
        raise NotImplementedError()

    @property
    def prt_is_active(self):
        raise NotImplementedError()

    @property
    def prt_created(self):
        raise NotImplementedError()

    @property
    def prt_updated(self):
        raise NotImplementedError()


class ImageInterface(CoreModelInterface):
    _required_attributes = [
        # properties:
        'prt_img',

        # methods:
        'delete',
        'delete_img',
    ]

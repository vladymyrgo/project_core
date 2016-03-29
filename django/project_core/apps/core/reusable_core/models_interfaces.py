class CoreModelInterface(object):

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

    def delete(self):
        raise NotImplementedError()

    @property
    def prt_img(self):
        raise NotImplementedError()

    def delete_img(self):
        raise NotImplementedError()

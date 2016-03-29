class CoreModelAdapter(object):

    @property
    def prt_is_active(self):
        return self.is_active

    @property
    def prt_created(self):
        return self.created

    @property
    def prt_updated(self):
        return self.updated


class ImageAdapter(CoreModelAdapter):

    @property
    def prt_img(self):
        return self.img

    def delete_img(self):
        self.img.delete(save=False)

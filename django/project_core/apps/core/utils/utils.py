from hashlib import md5
from os.path import splitext

from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def send_mail_alternatives(to, subject, html_content, text_content=None, from_email=None, reply_to=None):
    if text_content is None:
        text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to, reply_to=reply_to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def handle_filename(instance, filename):
    filename, extension = splitext(filename)
    if isinstance(filename, unicode):
        filename = filename.encode('utf8')
    filename = md5(filename).hexdigest()
    return "{}/{}/{}{}".format(filename[:2], filename[2:4], filename[4:], extension)

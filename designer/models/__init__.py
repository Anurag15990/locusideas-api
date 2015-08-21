__author__ = 'anurag'

from designer.app import engine
import datetime
from designer.services.utils import get_random, decode_base64
from PIL import Image, ImageFile
import os, random, base64
from designer.settings import MEDIA_FOLDER
from mongoengine import signals

class ImageModel(engine.Document):

    image = engine.ImageField()
    image_path = engine.StringField()
    image_updated_time = engine.DateTimeField(default=datetime.datetime.now())
    thumbnail_path = engine.StringField()
    thumbnail_updated_time = engine.DateTimeField(default=datetime.datetime.now())
    icon_path = engine.StringField()
    icon_updated_time = engine.DateTimeField(default=datetime.datetime.now())

    meta = {
        "allow_inheritance" : True,
    }

def save_image(base64String):

    from designer.settings import CDN_URL, USE_CDN
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    size = 300, 300
    icon_size = 64, 64


    if not os.path.exists(os.getcwd() + '/designer/' + MEDIA_FOLDER):
        os.mkdir(os.getcwd() + '/designer/' + MEDIA_FOLDER)
    file_content = decode_base64(str(base64String))
    name = str(datetime.datetime.now()).split(' ')[0].replace('-', '') + "-" + str(random.randrange(9999999999999, 999999999999999999))
    if USE_CDN:
        from designer.app import bucket_key

        path = '/tmp/%s.jpg' %name
        file = open(path, 'wb')
        file.write(file_content)


        thumbnail_name = '%s-thumbnail.jpg' %name
        icon_name = '%s-icon.jpg' %name
        thumbnail_path = '/tmp/%s' %thumbnail_name
        icon_path = '/tmp/%s' %icon_name

        bucket_key.key = MEDIA_FOLDER + name + '.jpg'
        bucket_key.set_contents_from_string(file_content)
        cdn_path = CDN_URL + MEDIA_FOLDER + name + '.jpg'

        bucket_key.key = MEDIA_FOLDER + thumbnail_name
        thumbnail_image = Image.open(path)
        thumbnail_image.thumbnail(size, Image.ADAPTIVE)
        thumbnail_image.save(thumbnail_path, "JPEG")

        with open(thumbnail_path, 'rb') as thumbnail_image:
            bucket_key.set_contents_from_string(decode_base64(str(base64.b64encode(thumbnail_image.read()))))
        cdn_thumbnail_path = CDN_URL + MEDIA_FOLDER + thumbnail_name

        bucket_key.key = MEDIA_FOLDER + icon_name
        icon_image = Image.open(path)
        icon_image.thumbnail(icon_size, Image.ADAPTIVE)
        icon_image.save(icon_path, "JPEG")

        with open(icon_path, 'rb') as icon_image:
            bucket_key.set_contents_from_string(decode_base64(str(base64.b64encode(icon_image.read()))))
        cdn_icon_path = CDN_URL + MEDIA_FOLDER + icon_name

        return cdn_path, cdn_thumbnail_path, cdn_icon_path, path

    path = os.getcwd() + '/designer/' +  "%s/%s.jpg" %(MEDIA_FOLDER, name)
    file = open(path, "wb")
    file.write(file_content)
    thumbnail_path = os.getcwd() + '/designer/' +"%s/%s-thumbnail.jpg" %(MEDIA_FOLDER, name)
    icon_path = os.getcwd() + '/designer/' + "%s/%s-icon.jpg" %(MEDIA_FOLDER, name)
    thumbnail_image = Image.open(path)
    thumbnail_image.thumbnail(size, Image.ADAPTIVE)
    thumbnail_image.save(thumbnail_path, "JPEG")

    icon_image  = Image.open(path)
    icon_image.thumbnail(icon_size, Image.ADAPTIVE)
    icon_image.save(icon_path, "JPEG")
    file.close()
    return path, thumbnail_path, icon_path, path

class Node(object):

    title = engine.StringField()
    description = engine.StringField()
    created_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    updated_timestamp = engine.DateTimeField(default=datetime.datetime.now())
    slug = engine.StringField()

    @classmethod
    def get_by_id(cls, id):
        return cls.objects(pk=id).first()

    @classmethod
    def get_by_slug(cls, slug):
        return cls.objects(slug__iexact=slug).first()


class Location(engine.Document):
    location = engine.StringField()
    geo_location = engine.PointField()
    city = engine.StringField()
    state = engine.StringField()
    country = engine.StringField()
    zipCode = engine.StringField()


def handler(event):

    def decorator(fn):
        def apply(cls):
            event.connect(fn, sender=cls)
            return cls

        fn.apply = apply
        return fn
    return decorator


@handler(signals.pre_save)
def update_content(sender, document):
    if hasattr(document, 'published') and document.published_timestamp is None:
        document.published_timestamp = datetime.datetime.now()

    if (not hasattr(document, 'slug') or document.slug is None or len(document.slug) is 0) and document.id is not None:
        update_slug(sender, document, document.__class__.__name__.lower(), document.id)


def update_slug(sender, document, type, id):
    _doc = document.__class__.objects(pk=str(id)).first()
    original_slug = '/%s/%s' %(type, str(id))
    if not _doc:
        _slug = original_slug
        count = 1
        while document.__class__.objects(slug=_slug).first() is not None:
            _slug = original_slug + str(count)
            count += 1
    else:
        _slug = original_slug
    document.slug = _slug

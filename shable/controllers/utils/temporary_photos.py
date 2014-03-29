import logging
from PIL import Image
from tgext.datahelpers.utils import fail_with
from tgext.datahelpers.attachments import AttachedImage
from tg import TGController, expose, validate, session
from shable.model import TemporaryPhotosBucket
from datetime import datetime
from tw2.forms import FileValidator
from tw2.core import IntValidator

log = logging.getLogger('shable')


class TemporaryPhotosUploader(TGController):
    @classmethod
    def get_bucket(cls):
        bucket = None
        bucket_id = session.get('temporary_photos_bucket_id')
        if bucket_id is not None:
            bucket = TemporaryPhotosBucket.query.get(_id=bucket_id)

        if bucket is None:
            bucket = TemporaryPhotosBucket(created_at=datetime.utcnow())

        session['temporary_photos_bucket_id'] = bucket._id
        session.save()
        return bucket

    @classmethod
    def new_bucket(cls):
        bucket = TemporaryPhotosBucket(created_at=datetime.utcnow())
        session['temporary_photos_bucket_id'] = bucket._id
        session.save()
        return bucket

    @classmethod
    def current_photos(cls):
        bucket = cls.get_bucket()
        return [dict(url=p.thumb_url, uid=str(idx)) for idx, p in enumerate(bucket.photos)]

    @classmethod
    def recover_photos(cls, photos):
        bucket = cls.get_bucket()
        bucket.photos = photos
        return [dict(url=p.thumb_url, uid=str(idx)) for idx, p in enumerate(bucket.photos)]


    @classmethod
    def save_image(cls, file):
        attached_image = AttachedImage(file.file, file.filename)
        attached_image.thumbnail_size = (200, 200)
        attached_image.write()
        image_data = {'file': attached_image.local_path,
                      'url': attached_image.url,
                      'filename': attached_image.filename,
                      'uuid': attached_image.uuid,
                      'thumb_local_path': attached_image.thumb_local_path,
                      'thumb_url': attached_image.thumb_url}
        return image_data

    @expose('json')
    @validate({'file': FileValidator(required=True),
               'uid': IntValidator()},
              error_handler=fail_with(403))
    def save(self, file, uid=None):
        bucket = self.get_bucket()

        try:
            Image.open(file.file)
            file.file.seek(0)
        except:
            log.exception('Failed to upload image')
            return dict(photos=self.current_photos())

        if uid is None:
            image = self.save_image(file)
            bucket.photos.append(image)
        else:
            bucket.photos[uid] = self.save_image(file)

        return dict(photos=self.current_photos())


    @expose('json')
    @validate({'uid': IntValidator(required=True)},
              error_handler=fail_with(403))
    def remove(self, uid=None):
        bucket = self.get_bucket()
        try:
            bucket.photos.pop(uid)
        except:
            log.exception('Trying to pop an unexisting image')

        return dict(photos=self.current_photos())



from datetime import datetime
from ming import schema as s
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass
from session import DBSession


class TemporaryPhotosBucket(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'temporary_photos_bucket'

    _id = FieldProperty(s.ObjectId)
    created_at = FieldProperty(s.DateTime, required=True, if_missing=datetime.utcnow)
    photos = FieldProperty([{'file': s.String(required=True),
                             'url': s.String(required=True),
                             'thumb_url': s.String(required=True),
                             'thumb_local_path': s.String(required=True),
                             'uuid': s.String(required=True),
                             'filename': s.String(required=True)}])


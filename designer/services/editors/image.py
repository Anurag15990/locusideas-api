__author__ = 'anurag'

from designer.services.editors.base import BaseEditor
from designer.models import EmbeddedImageField
class ImageEditor(BaseEditor):

    def _invoke(self):
        if self.command == 'upload-image':
            return upload_image(self.data)


def upload_image(data):
    if data['image'] is not None:
        return EmbeddedImageField.create(data['image'])
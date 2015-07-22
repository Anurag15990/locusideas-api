__author__ = 'anurag'

from designer.services.editors.base import BaseEditor
from designer.models.image import UserImage, ContentImage
class ImageEditor(BaseEditor):

    def _invoke(self):
        if self.command == 'upload-user-image':
            return upload_user_image(self.data, self.node)
        if self.command == 'upload-content-image':
            return upload_content_image(self.data, self.node)



def upload_user_image(data, node):
    if data['image'] is not None:
        return UserImage.create(data, node)

def upload_content_image(data, node):
    if data['image'] is not None:
        return ContentImage.create(data, node)
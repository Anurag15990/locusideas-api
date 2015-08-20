__author__ = 'anurag'

from designer.services.editors.base import BaseEditor, response_handler
from designer.models.image import UserImage, CreativesImage
class ImageEditor(BaseEditor):

    def _invoke(self):
        if self.command == 'upload-user-image':
            return upload_user_image(self.data, self.node)
        if self.command == 'upload-creative-image':
            return upload_creative_image(self.data, self.node)


#@response_handler('Successfully uploaded User Image', 'Failed to upload User Image')
def upload_user_image(data, node):
    if data['image'] is not None:
        return UserImage.create(data, node)

@response_handler('Successfully uploaded creatives image', 'Failed to upload creatives image')
def upload_creative_image(data, node):
    if data['image'] is not None:
        return CreativesImage.create(data, node)
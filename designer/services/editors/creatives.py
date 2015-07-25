__author__ = 'anurag'

from designer.services.editors.base import BaseEditor
from designer.models.creatives import PortFolio, Designs

class CreativesEditor(BaseEditor):

        def _invoke(self):
            if self.command == 'create-new-portfolio':
                pass
            if self.command == 'create-new-design':
                pass
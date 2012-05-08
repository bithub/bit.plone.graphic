from zope.interface import implements

from trinity.content.copy.interfaces import ICopyable
from trinity.content.copy.copier import Copyable

from bit.content.graphic.interfaces import\
    IGraphical, ICustomGraphic


class GraphicsCopier(Copyable):
    implements(ICopyable)

    def copy(self, name):
        source_graphics = IGraphical(self.source)
        target_graphics = IGraphical(self.target)

        for k in source_graphics.graphicKeys(expand=False):
            v = source_graphics.getRawGraphic(k, expand=False)

            # translate portal relative references
            if v.startswith('/'):
                source_portal = self.source.portal_url.getPortalObject()
                source_path = '/'.join(
                    [''] + list(
                        self.source.getPhysicalPath()[len(
                                source_portal.getPhysicalPath()):]))

                if v.startswith(source_path):
                    target_portal = self.target.portal_url.getPortalObject()
                    target_path = '/'.join(
                        [''] + list(
                            self.target.getPhysicalPath()[len(
                                    target_portal.getPhysicalPath()):]))
                    v = target_path + v[len(source_path):]

            target_graphics.setGraphic(k, v)

        source_custom = ICustomGraphic(self.source)
        target_custom = ICustomGraphic(self.target)

        custom_image = source_custom.getImage()

        if custom_image:
            target_custom.setImage(
                custom_image.data,
                custom_image.contentType,
                custom_image.filename)

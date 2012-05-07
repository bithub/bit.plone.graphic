from types import StringType
from StringIO import StringIO

from zope.interface import implements
from zope import component
from zope.annotation.interfaces import IAnnotations

from bit.plone.graphic.interfaces import IGraphicalImage, IThumbnailer

ANNO_IMAGE = 'bit.plone.graphic.Image'

_accessor = True
try:
    from trinity.content.thumbnail.interfaces import IDocumentDataAccessor
except ImportError:
    _accessor = False


class Thumbnailer(object):
    implements(IThumbnailer)

    def __init__(self, context):
        self.context = context

    def generateThumb(self):
        if not _accessor:
            return
        accessor = component.queryAdapter(
            self.context,
            IDocumentDataAccessor,
            unicode(self.context.get_content_type()))
        firstpage = None
        if accessor is not None:
            if hasattr(self.context.aq_inner, 'image'):
                req = self.context.REQUEST
                if not req in 'file_file'\
                        or not req['file_file']\
                        or hasattr(req, 'ALREADY_BUILT'):
                    return
                req.ALREADY_BUILT = True

            firstpage = accessor.generateFirstPageAsImage()
            if not firstpage:
                return
            if type(firstpage) is StringType:
                firstpage = StringIO(firstpage)

        return firstpage


class GraphicalImage(object):
    implements(IGraphicalImage)

    def __init__(self, context):
        self.context = context

    def getImage(self):
        return IAnnotations(self.context).get(ANNO_IMAGE)

    def setImage(self, image):
        #        IAnnotations(self.context).set(ANNO_IMAGE, image)
        pass

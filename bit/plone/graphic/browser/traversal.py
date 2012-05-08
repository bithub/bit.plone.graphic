from zope.component import adapts
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse, NotFound

from plone.namedfile.utils import set_headers, stream_data

from Products.Five.browser import BrowserView

from bit.content.graphic.interfaces import\
    IGraphicallyCustomized, ICustomGraphic


class CustomGraphicTraverser(BrowserView):
    """Browser traverser for IArchiveFile."""

    adapts(IGraphicallyCustomized, IPublishTraverse)
    implements(IPublishTraverse)

    def __init__(self, context, request):
        super(CustomGraphicTraverser, self).__init__(context, request)
        self.context = context
        self.request = request
        self.name = None

    def browserDefault(self, request):
        return self.context, ('image', )

    def publishTraverse(self, request, name):
        if self.name == None:
            self.name = name[6:]
        else:
            raise NotFound(self, name, request)
        return self

    def __call__(self):
        graphic = ICustomGraphic(self.context).get_image(self.name)
        if graphic:
            set_headers(graphic, self.request.response)
            return stream_data(graphic)
        raise NotFound(self, self.name, self.request)

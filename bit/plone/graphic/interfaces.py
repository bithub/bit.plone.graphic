from zope.interface import Interface as I

from bit.content.graphic.interfaces import IGraphicallyCustomized

class IThumbnailer(I):

    def generateThumb():
        pass


class IGraphicsView(I):

    def render(self):
        pass


class IGraphicalImage(I):

    def getImage():
        pass

    def setImage():
        pass

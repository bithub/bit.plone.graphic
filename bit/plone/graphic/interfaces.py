from zope.interface import Interface as I


class IThumbnailer(I):

    def generateThumb():
        pass


class ICustomGraphic(I):

    def getImage():
        pass

    def setImage():
        pass


class IGraphicallyCustomized(I):
    pass


class IGraphicsView(I):

    def render(self):
        pass


class IIconic(I):
    """Allow the getIcon to be adapted
    """

    def getIcon():
        """ return a custom icon
        """


class IGraphicalImage(I):

    def getImage():
        pass

    def setImage():
        pass


class IGraphical(I):

    def getGraphic(graphic):
        pass

    def setGraphic(graphic, path):
        pass

    def graphicKeys():
        pass

    def graphicList():
        pass

    def clearGraphics():
        pass

    def getRawGraphic(graphic, path):
        pass


IGraphicalRepresentation = IGraphical

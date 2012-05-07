from zope.interface import Interface as I

from bit.plone.graphic.interfaces\
    import IGraphicalRepresentation, IIconic

from plone.indexer.decorator import indexer


@indexer(I)
def getIcon(obj, **kwa):
    graphical = IGraphicalRepresentation(obj, None)
    icon = ''
    if graphical:
        icon = graphical.getGraphic('icon')
    if not icon:
        iconic = IIconic(obj, None)
        if iconic:
            icon = iconic.get_icon()
    if not icon:
        icon = obj.getIcon(True)
    return icon


@indexer(I)
def getGraphics(obj, **kwa):
    graphical = IGraphicalRepresentation(obj, None)
    return graphical and graphical.graphicList()


@indexer(I)
def getThumbnail(obj, **kwargs):
    graphical = IGraphicalRepresentation(obj, None)
    return graphical and graphical.getGraphic('thumb') or None

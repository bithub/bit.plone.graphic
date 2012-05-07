from zope.interface import Interface as I
from zope import schema
from plone.namedfile import field
from plone.formwidget.namedfile.interfaces import INamedImageWidget


class IGraphicAssociation(I):
    """ a graphical association """
    name = schema.TextLine(
        title=u"name",
        required=False)
    association = schema.TextLine(
        title=u"association",
        required=False,
        default=u'')


class IGraphicsForm(I):
    """ A graphics form """
    custom_graphic = field.NamedBlobImage(
        title=u'Custom graphic',
        description=u"Add a custom graphic to this item of content",
        required=False)

    graphic_associations = schema.List(
        title=u"Associate graphics",
        required=False,
        value_type=schema.Object(
            schema=IGraphicAssociation,
            required=False))


class INamedBlobImageWidget(INamedImageWidget):
    """A widget for a named blob image field
    """

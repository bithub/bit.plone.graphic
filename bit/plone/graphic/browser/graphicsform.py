from z3c.form import form, field
from z3c.form.object import registerFactoryAdapter

from plone.z3cform.layout import wrap_form

from bit.content.graphic.interfaces import\
    IGraphical, ICustomGraphic
from bit.plone.graphic.browser.interfaces\
    import IGraphicsForm, IGraphicAssociation


class GraphicAssociation(object):
    implements(IGraphicAssociation)
    title = u'association'

    def __init__(self):
        pass

    def update(self, name, assoc):
        self.name = name
        self.association = assoc
        return self
registerFactoryAdapter(IGraphicAssociation, GraphicAssociation)


class GraphicsFormAdapter(object):

    def __init__(self, context, *largs, **kwargs):
        self.context = context
        graphical = IGraphical(self.context, None)
        self.graphics = '\n'.join(graphical.getRawList())
        self.custom_graphic = ICustomGraphic(self.context).getImage()
        self.graphic_associations = [
            GraphicAssociation().update(unicode(x), unicode(y or ''))
            for x, y in graphical.get_graphics().items()]


class GraphicsForm(form.EditForm):
    fields = field.Fields(IGraphicsForm)
    label = "Manage graphics associated with this object"

    def applyChanges(self, data):
        ICustomGraphic(self.context).setImage(data['custom_graphic'])
        #import pdb; pdb.set_trace()
        self._set_graphics(data)
        self.context.reindexObject()
        return self.context.REQUEST.response.redirect(
            '%s/@@manage-graphics' % self.context.absolute_url())

    def updateWidgets(self):
        super(GraphicsForm, self).updateWidgets()

        for widget in self.widgets['graphic_associations'].widgets:
            widget.subform.widgets['name'].addClass('graphicName')
            widget.subform.widgets['association'].addClass(
                'graphicAssociation')

    def _set_graphics(self, data):
        graphics = data.get('graphic_associations', '') or []
        graphical = IGraphical(self.context)
        if graphical:
            graphical.clear_graphics()
            [graphical.set_graphic(g.name, g.association or '')
             for g in graphics if g.name]
        if not 'base' in graphical.graphicKeys(expand=False)\
                and data.get('custom_graphic'):
            graphical.set_graphic('base', 'custom_graphic/image')

        if graphical.get_raw_graphic('base') == 'custom_graphic/image'\
                and not data.get('custom_graphic'):
            graphical.set_graphic('base')

GraphicsFormView = wrap_form(GraphicsForm)

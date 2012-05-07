from z3c.form import form, field

from plone.z3cform.layout import wrap_form

from bit.plone.graphic.interfaces import\
    IGraphicalRepresentation, ICustomGraphic
from bit.plone.graphic.browser.interfaces import IGraphicsForm


class GraphicsForm(form.EditForm):
    fields = field.Fields(IGraphicsForm)
    label = "Manage graphics associated with this object"

    def applyChanges(self, data):
        ICustomGraphic(self.context).setImage(data['custom_graphic'])
        #import pdb; pdb.set_trace()
        self._setGraphics(data)
        self.context.reindexObject()
        return self.context.REQUEST.response.redirect(
            '%s/@@manage-graphics' % self.context.absolute_url())

    def updateWidgets(self):
        super(GraphicsForm, self).updateWidgets()

        for widget in self.widgets['graphic_associations'].widgets:
            widget.subform.widgets['name'].addClass('graphicName')
            widget.subform.widgets['association'].addClass(
                'graphicAssociation')

    def _setGraphics(self, data):
        graphics = data.get('graphic_associations', '') or []
        graphical = IGraphicalRepresentation(self.context)
        if graphical:
            graphical.clearGraphics()
            [graphical.setGraphic(g.name, g.association or '')
             for g in graphics if g.name]
        if not 'base' in graphical.graphicKeys(expand=False)\
                and data.get('custom_graphic'):
            graphical.setGraphic('base', 'custom_graphic/image')

        if graphical.getRawGraphic('base') == 'custom_graphic/image'\
                and not data.get('custom_graphic'):
            graphical.setGraphic('base')

GraphicsFormView = wrap_form(GraphicsForm)

import os

from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from bit.plone.cp.interfaces import IControlPanel
from bit.plone.cp.cp import ControlPanel


def _path(context, path):
    portal = getToolByName(context, 'portal_url')
    return os.path.join(*list(portal.getPhysicalPath()) + path.split('/'))


class GraphicCP(ControlPanel):
    implements(IControlPanel)

    def __init__(self, context):
        self.context = context

    def get_title(self):
        return 'Content graphics'

    def display_data(self, data):
        data = super(self.__class__, self).display_data(data)
        for res in data:
            data[res]['thumb'] = (data[res]['thumb'], data[res]['original'])
        return data

    def get_data(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog()
        content = {}
        paths = [x.getPath() for x in results]
        for result in results:
            item = self.get_item(result)
            if item:
                for g in result.graphics:
                    graph = ':'.join(g.split(':')[1:])
                    if graph.startswith('/'):
                        if _path(
                            self.context,
                            os.path.dirname(graph)) not in paths:
                            item['broken_graphics'] = True
                content[result.getPath()] = item
        return content

    def get_item(self, result):
        item = super(self.__class__, self).get_item(result)
        item['graphics'] = result.graphics
        item['broken_graphics'] = False

        for g in result.graphics:
            if g.startswith('thumb:'):
                thumb = g[len('thumb:'):]
                if not thumb.startswith('/')\
                        and not (
                    thumb.startswith('http://')\
                        or thumb.startswith('https://')):
                    thumb = '/'.join((
                            result.getPath().rstrip('/'),
                            thumb))
                item['thumb'] = thumb
                break
        for g in result.graphics:
            if g.startswith('original:'):
                original = g[len('original:'):]
                if not original.startswith('/')\
                        and not (
                    original.startswith('http://')\
                        or original.startswith('https://')):
                    original = '/'.join((
                            result.getPath().rstrip('/'),
                            original))
                item['original'] = original
                break
        if not item.get('original'):
            item['original'] = False
        if not item.get('thumb'):
            item['thumb'] = False
        return item

    def get_buttons(self):
        buttons = super(self.__class__, self).get_buttons()
        buttons['reindex graphics'] = 'reindex_graphics_confirm:method'
        buttons['fix broken graphics'] = 'fix_graphics_confirm:method'
        return buttons

    def get_fields(self):
        fields = super(self.__class__, self).get_fields()
        fields['fields'].update({
                'thumb': {
                    'type': 'image',
                    'sort': True,
                    'title': 'Thumb',
                    'visible': True,
                    },
                'graphics': {
                    'sort': True,
                    'visible': True,
                    'type': 'list',
                    'title': 'Graphics',
                    },
                'broken_graphics': {
                    'sort': True,
                    'visible': True,
                    'title': 'Broken graphics',
                    },
                })
        fields['index'] += [
            'thumb',
            'graphics',
            'broken_graphics',
            'delete'
            ]
        fields['index'].remove('description')
        fields['index'].remove('description_length')
        return fields

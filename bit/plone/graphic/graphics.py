from persistent.dict import PersistentDict
from zope.interface import alsoProvides, noLongerProvides, implements

from zope.annotation.interfaces import IAnnotations

from plone.namedfile import NamedBlobImage
from plone.namedfile.interfaces import INamedBlobImage

from Products.CMFCore.utils import getToolByName

from bit.content.graphic.interfaces import\
    ICustomGraphic, IGraphicallyCustomized, IGraphical
from bit.content.graphic.graphics import CustomGraphic, Graphical


class PloneCustomGraphic(CustomGraphic):
    implements(ICustomGraphic)

    _annotation = 'bit.plone.graphic.CustomGraphic'

    _sizes = {'large': (768, 768),
              'preview': (400, 400),
              'mini': (200, 200),
              'thumb': (128, 128),
              'tile': (64, 64),
              'icon': (32, 32),
              'listing': (16, 16),
         }

    def _resize(self, original, size):
        return NamedBlobImage(
            super(PloneCustomGraphic, self)._resize(original, size),
            filename=original.filename)

    def set_image(self, image, contentType=None, filename=None):
        if image and not INamedBlobImage.providedBy(image):
            if hasattr(image, 'data'):
                data = image.data
            elif hasattr(image, 'read'):
                data = image.read()
            else:
                data = image
            if hasattr(image, 'filename') and not filename:
                filename = unicode(image.filename)
            elif hasattr(image, 'name') and not filename:
                filename = image.name.split('/').pop()
            if hasattr(image, 'contentType') and not contentType:
                contentType = image.contentType
            elif hasattr(image, 'encoding') and not contentType:
                contentType = image.encoding
            image = NamedBlobImage(data, contentType, unicode(filename))

        if not image and IGraphicallyCustomized.providedBy(self.context):
            noLongerProvides(self.context, IGraphicallyCustomized)
            del IAnnotations(self.context)[self._annotation]
        if image and not IGraphicallyCustomized.providedBy(self.context):
            alsoProvides(self.context, IGraphicallyCustomized)
        if image:
            IAnnotations(
                self.context)[self._annotation] = PersistentDict()
            IAnnotations(
                self.context).get(
                self._annotation)['original'] = image


class PloneGraphical(Graphical):
    implements(IGraphical)

    _annotation = 'bit.plone.graphic.Graphical'

    def get_graphic(self, graphicid, acquire=False, ctx=None):
        ctx = ctx or self.context
        res = super(PloneGraphical, self).get_graphic(graphicid, acquire, ctx)
        if not res and acquire:
            try:
                return self.get_graphic(
                    graphicid, acquire, ctx=ctx.aq_inner.aq_parent)
            except:
                return None
        if not res:
            return None
        base_url = ctx.absolute_url_path()
        if res.startswith('http://'):
            return res
        if res.startswith('/'):
            root = getToolByName(ctx, 'portal_url').getPortalObject()
            res = res[1:]
            path = root.absolute_url_path()
        else:
            path = base_url
        if path.endswith('/'):
            path = path[:-1]
        return res

    def clear_graphics(self):
        super(PloneGraphical, self).clear_graphics()
        self.context.reindexObject(idxs=['graphics'])

    def set_graphic(self, graphic, path=None):
        anno = IAnnotations(self.context)
        if not anno.get(self._annotation):
            anno[self._annotation] = PersistentDict()
        if path is not None:
            anno[self._annotation][graphic] = path
        else:
            del anno[self._annotation][graphic]
        self.context.reindexObject(idxs=['graphics'])


class ArchetypeGraphical(PloneGraphical):

    def _path(self, ob):
        portal = ob.portal_url.getPortalObject()
        return '/'.join(ob.getPhysicalPath()[len(portal.getPhysicalPath()):])

    def get_raw_graphic(self, graphicid, acquire=False, expand=True):
        graphics = IAnnotations(
            self.context).get(self._annotation)
        graphic = None
        if graphics:
            graphic = graphics.get(graphicid) or None
            if not graphic and 'base' in graphics.keys() and expand:
                graphic = '%s_%s' % (graphics.get('base'), graphicid)
        if not graphic:
            if graphicid in self._default_sizes:
                if self.context.Schema()['image'].get(self.context):
                    path = self._path(self.context)
                    if path.endswith('/'):
                        path = path[:-1]
                    graphic = 'image_%s' % graphicid
        return graphic and graphic.strip() or None


class PloneImageGraphical(ArchetypeGraphical):

    def graphic_ids(self):
        ids = set()
        ids.update(self._default_sizes)
        ids.update(super(PloneImageGraphical, self).graphic_ids())
        return list(ids)

    def get_graphic(self, graphic, acquire=False):
        if graphic in self._default_sizes:
            return 'image_%s' % graphic
        return ''


class PloneNewsItemGraphical(ArchetypeGraphical):

    def graphic_ids(self):
        ids = set()
        if self.context.Schema()['image'].get(self.context):
            ids.update(self._default_sizes)
        ids.update(super(PloneNewsItemGraphical, self).graphic_ids())
        return list(ids)

    def get_graphic(self, graphic, acquire=False):
        if graphic in self._default_sizes:
            if self.context.Schema()['image'].get(self.context):
                return 'image_%s' % graphic
        return ''

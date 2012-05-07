import os

from zope.annotation.interfaces import IAnnotations

from Products.Five import BrowserView as FiveView


class ReindexGraphicsView(FiveView):

    def get_content(self):
        return [(x, os.path.basename(x))
                for x in self.request.get('paths') or []]

    def reindex_graphics(self):
        content = self.request.get('content')
        if not content:
            return
        total = len(content)
        i = 1
        for path in content:
            print 'traversing to object %s (%s/%s)' % (path, i, total)
            try:
                obj = self.context.restrictedTraverse(path)
                print 'reindexing graphics for %s' % path
                anno = IAnnotations(obj)

                if 'an.other.graphic.Graphical' in anno.keys():
                    graphic = anno['an.other.graphic.Graphical']
                    anno['bit.plone.graphic.Graphical'] = graphic
                    del anno['an.other.graphic.Graphical']

                if 'an.other.graphic.CustomGraphic' in anno.keys():
                    graphic = anno['an.other.graphic.CustomGraphic']
                    anno['bit.plone.graphic.CustomGraphic'] = graphic
                    del anno['an.other.graphic.CustomGraphic']

                elif 'things.republic.interfaces.IGraphicalRepresentation' in anno.keys():
                    graphic = anno['things.republic.interfaces.IGraphicalRepresentation']
                    anno['bit.plone.graphic.Graphical'] = graphic
                    del anno['things.republic.interfaces.IGraphicalRepresentation']
                obj.reindexObject(idxs=['getGraphics', 'getIcon', 'Thumbnail'])
            except:
                print 'FAIL: %s' % path
            i += 1

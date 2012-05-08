import os
import logging

from zope.annotation.interfaces import IAnnotations

from Products.Five import BrowserView as FiveView

log = logging.getLogger('bit.plone.graphic')

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
            obj = self.context.restrictedTraverse(path)
            log.warn('reindexing graphics for %s' % path)
            anno = IAnnotations(obj)
            obj.reindexObject(idxs=['graphics', 'getIcon'])
            i += 1

import os

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
                obj.reindexObject(idxs=['getGraphics', 'getIcon', 'Thumbnail'])
            except:
                print 'FAIL: %s' % path
            i += 1

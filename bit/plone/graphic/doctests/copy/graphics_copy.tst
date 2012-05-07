===============================
Adapters: Graphics copy adapter
===============================

The copy adapter copies data from a source object to a target

We need to check that any graphical associations or customizations
are properly copied over

    >>> self.setRoles(['Manager',])

Let's get some imports

    >>> TEST_DIR = self.thisTestDir(__file__, __name__)

    >>> from zope.component import getMultiAdapter, getAdapters
    >>> from trinity.content.copy.interfaces import ICopier, ICopyable
    >>> from an.other.graphic.interfaces import IGraphicalRepresentation,ICustomGraphic

And create a couple of folders to play with and create a copier

    >>> srcfolder = self.portal[self.portal.invokeFactory('Folder','srcfolder')]
    >>> targetfolder = self.portal[self.portal.invokeFactory('Folder','targetfolder')]

    >>> copier = getMultiAdapter((srcfolder,targetfolder),ICopier)


Graphics copy adapter
---------------------

Let's check that we got the right kind of adapter

    >>> copier.copyable('graphics')
    <an.other.graphic.adapters.copier.GraphicsCopier ...>


Graphical associations
----------------------

    >>> src_graphics = IGraphicalRepresentation(srcfolder)
    >>> src_graphics.setGraphic('foo', 'bar.png')
    >>> src_graphics.setGraphic('base', 'baz.png')
    >>> src_graphics.setGraphic('baz', '/srcfolder/foo.png')

    >>> copier.copy()

    >>> target_graphics = IGraphicalRepresentation(targetfolder)
    >>> graphics = target_graphics.getGraphics()

    >>> graphics['foo']
    'bar.png'

    >>> graphics['base']
    'baz.png'

    >>> graphics['baz']
    '/targetfolder/foo.png'


Custom graphic
--------------

    >>> src_custom = ICustomGraphic(srcfolder)
    >>> src_custom.setImage(open('%s/test.png'%TEST_DIR,'r'))
    >>> src_image = src_custom.getImage()

    >>> copier.copy()

    >>> target_custom = ICustomGraphic(targetfolder)
    >>> target_image = target_custom.getImage()

The source and target custom images should not be the same object

    >>> src_image == target_image
    False

But should have the same information

    >>> len(target_image.data)
    315

    >>> src_image.data == target_image.data
    True

    >>> src_image.filename == target_image.filename == 'test.png'
    True

    >>> src_image.contentType == target_image.contentType == 'image/png'
    True


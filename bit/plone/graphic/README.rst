========================
Traversal: Archive files
========================

Let's start by logging in as a manager.

  >>> self.setRoles(['Manager'])

And get some tools

  >>> from zope.component import getMultiAdapter, getUtility
  >>> from zope.browser.interfaces import IBrowserView
  >>> from zope.publisher.browser import TestRequest
  >>> from bit.content.graphic.interfaces import IGraphical, IGraphicallyCustomized, ICustomGraphic

And set some stuff up!


  >>> import os
  >>> TEST_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests')
  >>> request = TestRequest()
  >>> from plone.testing.z2 import Browser
  >>> browser = Browser(layer['app'])
  >>> request = TestRequest()


And log in

  >>> from plone.app.testing import login, setRoles
  >>> from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
  >>> setRoles(layer['portal'], TEST_USER_ID, ['Member', 'Manager'])
  >>> login(layer['portal'], TEST_USER_NAME)  


We need a logged in user

    >>> self.app.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])
    >>> browser.addHeader('Authorization', 'Basic root:secret')


Folder graphics
---------------

Lets add a folder

    >>> folder = layer['portal'][layer['portal'].invokeFactory('Folder','folder')]

We can get a graphical adapter for the folder

    >>> from bit.content.graphic.interfaces import IGraphical
    >>> graphical = IGraphical(folder)
    >>> graphical
    <bit.plone.graphic.adapters.Graphical ...>

Currently it has not associations

    >>> graphical.graphic_list()
    []
    >>> graphical.graphic_ids()
    []    

The folder doesnt isnt graphically customized

    >>> IGraphicallyCustomized.providedBy(folder)
    False

Now lets give the folder a custom graphic

    >>> ICustomGraphic(folder).setImage(open('%s/test.png' % TEST_DIR, 'r'))
    >>> IGraphicallyCustomized.providedBy(folder)
    True

We can get the custom graphic

    >>> custom_graphic = ICustomGraphic(folder)
    >>> custom_graphic
    <bit.plone.graphic.adapters.CustomGraphic ...>

And from that we can get the image itself

    >>> custom_graphic_image = custom_graphic.get_image()
    >>> custom_graphic_image
    <plone.namedfile.file.NamedBlobImage object ...>


Graphic associations
--------------------

It still doesn't have any graphics associated

    >>> graphical.graphic_list()
    []

    >>> graphical.graphic_ids()
    []    

If we associate the path to our custom graphic as the 'base' image

    >>> graphical.set_graphic('base', 'custom_graphic/image')


We can automatically associate any images that have been automatically resized

    >>> sorted(graphical.graphic_ids())
    ['large', 'mini', 'original', 'preview', 'thumb', 'tile']

    >>> sorted(graphical.graphic_list())
    ['large:custom_graphic/image_large', 'mini:custom_graphic/image_mini', 'original:custom_graphic/image', 'preview:custom_graphic/image_preview', 'thumb:custom_graphic/image_thumb', 'tile:custom_graphic/image_tile']

The object has the graphics items stored in its catalog record

    >>> from Products.CMFCore.utils import getToolByName
    >>> portal_catalog = getToolByName(layer['portal'], 'portal_catalog')

    >>> record = portal_catalog(path='/plone/folder')[0]
    >>> sorted(record.getGraphics) == sorted(graphical.graphic_list())
    True


Graphical image
---------------

Lets add an image in our folder


The image automatically has different versions


Graphical news item
-------------------

Now lets add a news item to our folder

    >>> news_item = folder[folder.invokeFactory('News Item','news_item')]

    >>> graphical_news_item = IGraphical(news_item)
    >>> graphical_news_item
    <bit.plone.graphic.adapters.GraphicalNewsItem ...>

The news item doesnt have an image yet

    >>> graphical_news_item.graphic_ids()
    []

So lets add one and check the news item has the correct associations

    >>> news_item.setImage(open('%s/test.png' % TEST_DIR, 'r'))
    >>> sorted(graphical_news_item.graphic_ids())
    ['large', 'mini', 'original', 'preview', 'thumb', 'tile']

    >>> sorted(graphical_news_item.graphic_list())
    ['large:/folder/news_item/image_large', 'mini:/folder/news_item/image_mini', 'original:/folder/news_item/image_original', 'preview:/folder/news_item/image_preview', 'thumb:/folder/news_item/image_thumb', 'tile:/folder/news_item/image_tile']




    >>> # browser.open('http://nohost/plone/news_item/custom_graphic/image')
    >>> # browser.contents
    >>> # "<open file '/tmp/...>"



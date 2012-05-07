import unittest

from Products.CMFCore.utils import getToolByName

from bit.plone.graphic.testing import GRAPHIC_FUNCTIONAL_TESTING


class TestGraphicInstallationCase(unittest.TestCase):
    layer = GRAPHIC_FUNCTIONAL_TESTING

    def test_installed(self):
        return
        installer = getToolByName(
            self.layer['portal'], 'portal_quickinstaller')
        product_list = [i['id'] for i in  installer.listInstalledProducts()]
        installed = lambda x: x in product_list
        [self.failUnless(installed(x))
         for x in ['plone.namedfile']]
        # 'plone.formwidget.namedfile',]]
        # 'z3c.blobfile',
        # 'trinity.content.copyright']]

    def test_rolemap(self):
        pass

    def test_permissions(self):
        pass

    def test_portletManager(self):
        pass

from pynwn.gff import Gff

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

from pynwn.obj.item import RepositoryItem

class Store(NWObjectVarable):
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None
        self._locstr = {}

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.utm':
                resref = resref+'.utm'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self._utm = resref.val

        NWObjectVarable.__init__(self, self.gff)

    def __getattr__(self, name):
        if name == 'utm':
            if not self._utm: self._utm = self.gff.structure
            return self._utm

    def __getitem__(self, name):
        return self.utm[name].val

    @property
    def resref(self):
        """Resref."""
        return self['ResRef']

    @property
    def name(self):
        """Localized name."""
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['LocalizedName'])

        return self._locstr['name']

    @property
    def tag(self):
        """Tag."""
        return self['Tag']

    @property
    def mark_up(self):
        """Active flag."""
        return self['MarkUp']

    @property
    def mark_down(self):
        return self['MarkDown']

    @property
    def black_market(self):
        """Black market flag."""
        return self['BlackMarket']

    @property
    def mark_down_bm(self):
        return self['BM_MarkDown']

    @property
    def price_id(self):
        """Price to identify item.."""
        return self['IdentifyPrice']

    @property
    def price_max_buy(self):
        """Maximum buy price."""
        return self['MaxBuyPrice']

    @property
    def gold(self):
        """Gold."""
        return self['StoreGold']

    @property
    def script(self):
        """Scripts.  Responds to script events:

        #. Event.OPEN
        #. Event.CLOSE
        """
        if self._scripts: return self._scripts

        lbls = {}
        lbls[Event.OPEN] = 'OnOpenStore'
        lbls[Event.CLOSE] = 'OnStoreClosed'

        self._scripts = NWObjectScripts(self.utm, lbls)

        return self._scripts

    @property
    def will_not_buy(self):
        """Will not buy list.

        :returns: List of baseitem IDs that store will not buy.
        """
        return [i['BaseItem'] for i in self['WillNotBuy']]

    @property
    def will_only_buy(self):
        """Will only buy list.

        :returns: List of baseitem IDs that store will only buy.
        """
        return [i['BaseItem'] for i in self['WillOnlyBuy']]

    @property
    def items(self):
        """Items in inventory.

        :returns: a two dimensional array with the format:
        [<store page>][<RepositoryItem objects>]
        """
        res = []
        for page in self['StoreList']:
            items = []
            try:
                items = [RepositoryItem(i) for i in page['ItemList']]
            except Exception:
                pass

            res.append( items )

        return res

    @property
    def palette_id(self):
        """Palette ID"""
        return self['ID']

    @property
    def comment(self):
        """Comment"""
        return self['Comment']

class StoreInstance(Store):
    """A store instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Store.__init__(self, gff, None, True)
        self.is_instance = True
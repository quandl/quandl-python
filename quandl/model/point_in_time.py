from quandl.operations.get import GetOperation
from quandl.operations.list import ListOperation
from .data import Data
from .model_base import ModelBase
from datetime import date

import logging
log = logging.getLogger(__name__)


class PointInTime(GetOperation, ListOperation, ModelBase):
    def data(self, **options):
        if not options:
            options = {'params': {}}
        return Data.page(self, **options)

    def default_path(self):
        return "%s/:id/%s" % (self.lookup_key(), self.pit_url(),)

    def lookup_key(self):
        return 'pit'

    def pit_url(self):
        interval = self.options['pit']['interval']
        if interval in ['asofdate']:
            if 'date' not in self.options['pit'].keys():
                date_replace = date.today()
            else:
                date_replace = self.options['pit']['date']
            return "%s/%s" % (interval, date_replace, )
        else:
            start_date = self.options['pit']['start_date']
            end_date = self.options['pit']['end_date']
            if interval == 'between':
                return "%s/%s/%s" % (interval, start_date, end_date, )
            else:
                return "%s/%s/to/%s" % (interval, start_date, end_date, )

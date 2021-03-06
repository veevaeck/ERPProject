'''@author: Fery Febriyan Syah'''

from django.conf import settings
ugettext = lambda s: s
from django.utils.translation import ugettext

DAY = getattr (settings, 'DAY',     ((1, ugettext ('Senin')),
                                     (2, ugettext ('Selasa')),
                                     (3, ugettext ('Rabu')),
                                     (4, ugettext ('Kamis')),
                                     (5, ugettext ('Jumat')),
                                     (6, ugettext ('Sabtu')),
                                     (7, ugettext ('Minggu'))))


DAY_STATUS = getattr (settings, 'DAY_STATUS',     ((1, ugettext ('Hari Aktif')),
                                                   (2, ugettext ('Minggu')),
                                                   (3, ugettext ('Libur Nasional'))))


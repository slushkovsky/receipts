import re

from logbook import Logger, FileHandler

from web.models import SMS, AnalyseResult


log = Logger('ANALYSE_SMS')
FileHandler('/tmp/checkstar.analyse_sms.log').push_application()

RE = re.compile('[Pp]okupka.*([\W])([\n\r]*).*\d\d\d|[Дд]оступно всего..\d*\d|[Dd]ostupniy limit..\d*\d|Баланс..\d*\d|[Oo]statok.([\W])([\n\r]*)\d.*\d|[Dd]ostupn..\d*\d|[Пп]окупка.*([\W])([\n\r]*).*\d\d\d')

def analyse(sms): 
    isinstance(sms, SMS)
    
    log.info(sms.content)

    return AnalyseResult()

from handlers.config import *
from handlers.imports import *
from handlers.filters import IsOwnerFilter

"""LOGGING"""


class CsvFormatter(logging.Formatter):

    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        self.writer.writerow(['MY_MAC', record.asctime, record.levelname, record.msg])
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()


logging.basicConfig(filename=f'logs/run_info.csv',
                    filemode='a',
                    level=logging.INFO,
                    encoding='utf-16')

frmt = logging.Formatter('%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

ch = logging.StreamHandler()

'''BOT'''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)

dp.filters_factory.bind(IsOwnerFilter)

'''REDIS'''

r = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    charset="utf-8",
    decode_responses=True
)

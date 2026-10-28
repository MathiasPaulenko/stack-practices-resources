import logging, gzip, os
from logging.handlers import RotatingFileHandler

class CompressedRotatingFileHandler(RotatingFileHandler):
    def rotate(self, source, dest):
        super().rotate(source, dest)
        if os.path.exists(dest):
            with open(dest, 'rb') as f_in:
                with gzip.open(f'{dest}.gz', 'wb') as f_out:
                    f_out.writelines(f_in)
            os.remove(dest)

handler = CompressedRotatingFileHandler(
    '/var/log/app/application.log',
    maxBytes=100*1024*1024,  # 100MB
    backupCount=30,
)
logger = logging.getLogger('app')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

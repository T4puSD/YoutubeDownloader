import logging
from YTDownloader.Configuration.configuration import get_configuration

logging.basicConfig(filename=get_configuration().get_log_file_name,
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s"
                    )
# logging to both file and to console with this streamhandler
# if console output is no longer needed commnet this line bellow
logging.getLogger().addHandler(logging.StreamHandler())

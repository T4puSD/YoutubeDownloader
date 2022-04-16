import logging

logging.basicConfig(filename='../../log.txt',
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s"
                    )
# logging to both file and to console with this streamhandler
# if console output is no longer needed commnet this line bellow
logging.getLogger().addHandler(logging.StreamHandler())

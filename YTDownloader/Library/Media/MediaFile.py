import os

from pafy.backend_shared import BasePafy
from pafy.backend_youtube_dl import YtdlStream

from YTDownloader.Exceptions.general_exception import NotFoundException, IllegalArgumentException
from YTDownloader.Library.title_slugify import TitleSlugify
from YTDownloader.Configuration.config import Config
from YTDownloader.Configuration.configuration import get_configuration
from YTDownloader.debugger import logging


class _MediaFile:
    def __init__(self, pafy_obj: BasePafy):
        if pafy_obj is None:
            raise NotFoundException("Pafy object can not be none")
        self._title = pafy_obj.title
        self._author = pafy_obj.author
        self._thumbnail = pafy_obj.thumb
        self._title_slugify = TitleSlugify()
        self._config = get_configuration()

    def get_pafy_stream(self) -> YtdlStream:
        raise NotImplementedError("Please use a child class")

    def get_media_type_extension(self) -> str:
        raise NotImplementedError("Please use a child class")

    def start_download(self) -> None:
        raise NotImplementedError("Please use a child class")

    def get_download_dir(self) -> str:
        raise NotImplementedError("Please use a child class")

    def get_config(self) -> Config:
        if self._config is None:
            raise IllegalArgumentException("Config object can not be None")

        return self._config

    @property
    def get_author(self) -> str:
        return self._author

    def get_title(self) -> str:
        if self._title is None:
            raise NotFoundException("Media Title not found")
        return self._title_slugify.slugify_for_windows(self._title)

    def _get_extension(self) -> str:
        if self.get_pafy_stream() is None:
            raise IllegalArgumentException("Pafy stream object Can not be none")
        return self.get_pafy_stream().extension

    def get_original_title(self) -> str:
        return self.get_title() + "." + self._get_extension()

    def get_converted_title(self) -> str:
        return self.get_title() + "." + self.get_media_type_extension()

    def get_thumbnail(self) -> str:
        return self._thumbnail

    def get_download_path(self) -> str:
        return self.get_download_dir() + os.sep + self.get_original_title()

    def get_conversion_output_path(self) -> str:
        return self.get_download_dir() + os.sep + self.get_converted_title()

    def _prepare_download_dir(self) -> None:
        if not os.path.exists(self.get_download_dir()):
            try:
                logging.debug("Making Directory: {}".format(self.get_download_dir()))
                os.makedirs(self.get_download_dir())
            except Exception as e:
                logging.debug("Error occurred in making Directory: {}".format(self.get_download_dir()))
                logging.debug(e)
                raise e

    def _check_if_file_already_exist(self) -> None:
        if os.path.exists(self.get_download_path()) or \
                os.path.exists(self.get_conversion_output_path()):
            raise FileExistsError("File Already Exists!: " + self.get_title())

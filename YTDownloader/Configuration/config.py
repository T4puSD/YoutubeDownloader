from configparser import ConfigParser
from YTDownloader.Exceptions.general_exception import IllegalArgumentException


class Config:
    def __init__(self, configparser: ConfigParser):
        if configparser is None:
            raise IllegalArgumentException("ConfigParser can not be None")

        self._download_dir = configparser.get('conf', 'download_dir')
        self._download_dir_audio = configparser.get('conf', 'download_dir_audio')
        self._download_dir_video = configparser.get('conf', 'download_dir_video')
        self._temporary_dir = configparser.get('conf', 'temp_dir')
        self._log_file_name = configparser.get('conf', 'log_file')
        self._download_mode = configparser.get('conf', 'download_mode')
        self._number_of_threads = configparser.get('conf', 'number_of_threads')
        self._media_type = configparser.get('media_conf', 'media_type')
        self._media_quality = configparser.get('media_conf', 'media_quality')

    @property
    def get_download_dir(self):
        return self._download_dir

    @property
    def get_download_dir_audio(self):
        return self._download_dir_audio

    @property
    def get_download_dir_video(self):
        return self._download_dir_video

    @property
    def get_temporary_directory(self):
        return self._temporary_dir

    @property
    def get_log_file_name(self):
        return self._log_file_name

    @property
    def get_media_mode_type(self):
        return self._media_type

    @property
    def get_media_quality(self):
        return self._media_quality

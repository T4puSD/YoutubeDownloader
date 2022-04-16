import os
import pathlib
from configparser import ConfigParser

from YTDownloader.Configuration.config import Config
from YTDownloader.Enums import MediaType, DownloadMode, VideoQuality
from YTDownloader.Exceptions.general_exception import IllegalArgumentException


class Configuration:
    def __init__(self):
        self._home = pathlib.Path.home()
        self._config_file_path = os.path.join('configure.ini')
        self._user_download_directory = os.path.join(self._home, 'Downloads')
        self._default_download_directory = os.path.join(self._user_download_directory, 'YoutubeMusic')
        self._audio_download_directory = os.path.join(self._default_download_directory, 'Audio')
        self._video_download_directory = os.path.join(self._default_download_directory, 'Video')
        self._temp_dir = 'temp'
        self._log_file = 'log.txt'
        self._download_mode = DownloadMode.SINGLE
        self._number_of_threads = 2
        self.media_type = MediaType.AUDIO
        self.video_quality = VideoQuality.Q360P
        self._config_parser: ConfigParser = self._construct_config()

    def is_config_file_exists(self) -> bool:
        return os.path.exists(self._config_file_path)

    def _construct_config(self) -> ConfigParser:
        configparser = ConfigParser()
        configparser['conf'] = {
            'download_dir': self._default_download_directory,
            'download_dir_audio': self._audio_download_directory,
            'download_dir_video': self._video_download_directory,
            'temp_dir': self._temp_dir,
            'log_file': self._log_file,
            'download_mode': self._download_mode.name,
            'number_of_threads': self._number_of_threads
        }

        configparser['media_conf'] = {
            'media_type': self.media_type.name,
            'media_quality': self.video_quality.name
        }
        return configparser

    def load_configuration(self):
        self._config_parser.read(self._config_file_path)

    def save_configuration(self):
        self.re_construct_configuration()
        with open(self._config_file_path, 'w') as configfile:
            self._config_parser.write(configfile)

    def re_construct_configuration(self):
        self._config_parser = self._construct_config()

    def get_config(self) -> Config:
        if self._config_parser is None:
            raise IllegalArgumentException('Config parser can not be None')
        self.re_construct_configuration()
        return Config(self._config_parser)

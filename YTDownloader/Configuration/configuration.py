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

    def is_config_file_exists(self) -> bool:
        return os.path.exists(self._config_file_path)

    def get_configparser(self) -> ConfigParser:
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
        configparser = ConfigParser()
        configparser.read(self._config_file_path)

        if configparser is None:
            raise IllegalArgumentException("ConfigParser can not be None")

        self._user_download_directory = configparser.get('conf', 'download_dir')
        self._default_download_directory = configparser.get('conf', 'download_dir')
        self._audio_download_directory = configparser.get('conf', 'download_dir_audio')
        self._video_download_directory = configparser.get('conf', 'download_dir_video')
        self._temp_dir = configparser.get('conf', 'temp_dir')
        self._log_file = configparser.get('conf', 'log_file')
        self._download_mode = DownloadMode[configparser.get('conf', 'download_mode')]
        self._number_of_threads = configparser.getint('conf', 'number_of_threads')
        self.media_type = MediaType[configparser.get('media_conf', 'media_type')]
        self.video_quality = VideoQuality[configparser.get('media_conf', 'media_quality')]

    def save_configuration(self):
        configparser = self.get_configparser()
        with open(self._config_file_path, 'w') as configfile:
            configparser.write(configfile)

    def get_config(self) -> Config:
        configparser = self.get_configparser()
        if configparser is None:
            raise IllegalArgumentException('Config parser can not be None')
        return Config(configparser)

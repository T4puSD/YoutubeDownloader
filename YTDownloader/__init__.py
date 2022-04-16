from YTDownloader.Configuration.configuration import Configuration

configuration = Configuration()
if configuration.is_config_file_exists():
    configuration.load_configuration()
else:
    configuration.save_configuration()

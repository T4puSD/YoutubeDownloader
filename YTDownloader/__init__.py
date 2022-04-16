from YTDownloader.Configuration.configuration import Configuration

configuration = Configuration()
if not configuration.is_config_file_exists():
    configuration.save_configuration()
else:
    configuration.load_configuration()

import json


conf = {
    'download_dir_audio':['.','testing_downloads'],
    'download_dir_video':['.','testing_downloads','videos'],
    'temp_dir':['.','temp'],
    'log_file':['.','log.txt'],
}

# media_type = audio / video
# media_quality = normal / hq
# download_mode = single / playlist
download_conf = {
    'media_type':'audio',
    'media_quality':'normal',
    'download_mode':'single'
}

def generateJsonFile(basic_conf=None,basic_download_conf=None):
    try:
        with open("configure.json","w") as jsonFile:
            if basic_conf is None and basic_download_conf is None:
                json.dump({"conf":conf,"download_conf":download_conf},jsonFile)
            elif basic_conf is None and basic_download_conf is not None:
                json.dump({"conf":conf,"download_conf":basic_download_conf},jsonFile)
            elif basic_conf is not None and basic_download_conf is None:
                json.dump({"conf":basic_conf,"download_conf":download_conf},jsonFile)
            else:
                json.dump({"conf":basic_conf,"download_conf":basic_download_conf},jsonFile)

    except Exception as e:
        print("Exception dumping configure.json file")
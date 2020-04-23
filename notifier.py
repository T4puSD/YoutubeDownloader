import notify2
def notifyAboutTheService(summary,message):
    notify2.init("YoutubeDownloader")
    n  =notify2.Notification(summary,message)
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_timeout(5000)
    n.show()
        
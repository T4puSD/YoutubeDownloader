import platform
import time

def notifyAboutTheService(summary,message):
    if platform.system() == 'Linux':
        import notify2
        notify2.init("YoutubeDownloader")
        n  =notify2.Notification(summary,message)
        n.set_urgency(notify2.URGENCY_NORMAL)
        n.set_timeout(5000)
        n.show()
    if platform.system() == 'Windows':
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(summary,message,duration=3,threaded=True)
        while toaster.notification_active():
            time.sleep(0.1)

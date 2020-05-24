import platform
import threading
def winToast(summary,message):
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
    toaster.show_toast(summary,message,duration=3)

def notifyAboutTheService(summary,message):
    if platform.system() == 'Linux':
        import notify2        
        notify2.init("YoutubeDownloader")
        n  =notify2.Notification(summary,message)
        n.set_urgency(notify2.URGENCY_NORMAL)
        n.set_timeout(5000)
        n.show()
    if platform.system() == 'Windows':
        # win10toast module's native threaded argument is daemonthread
        # and it can't handle multiple notification at the same time and throws error
        t = threading.Thread(target=winToast,args=(summary,message))
        t.start()
        t.join()

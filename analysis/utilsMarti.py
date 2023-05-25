import datetime
import inspect


def printTime(verbose, b=None):
    if verbose:
        a = datetime.datetime.now()
        if b is None:
            print("[{} - {}] {}".format(a.strftime("%H:%M:%S.%f"), inspect.stack()[1].function.ljust(15), "START"))
        else:
            secs = (a-b).total_seconds()
            print("[{} - {}] {}".format(a.strftime("%H:%M:%S.%f"), inspect.stack()[1].function.ljust(15), "END ({}m {}s)".format(int(secs//60), round(secs%60, 6))))
        return a


def printWithTimestamp(text, timeStamp=True):
    if timeStamp:
        a = datetime.datetime.now()
        for l in text.splitlines():
            print("[{} - {}] {}".format(a.strftime("%H:%M:%S.%f"), inspect.stack()[1].function.ljust(15), l))
    else:
        print(text)

import platform
import datetime
import os


def FileMaker(topic):

    sys = platform.system()
    date = datetime.datetime.now()
    dtstr = date.strftime('%x')
    dtstr = dtstr.replace('/', '_')
    dtstr += '_' + topic
    if sys == 'Windows':
        newpath = r'.\\' + dtstr + '\\'
    elif sys == 'Darwin':
        newpath = r'./' + dtstr + '/'
    elif sys == 'Linux':
        newpath = r'./' + dtstr + '/'

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    return newpath
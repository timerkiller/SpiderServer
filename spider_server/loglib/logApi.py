__author__ = 'jclin'

import platform

if 'Windows' in platform.system():
    import loglib.core as coreWindows
    SYS_LOG = coreWindows.CMyLog.getLogger()
    currentPlatform = "Windows"
if 'Linux' in platform.system():
    import coreLinux
    SYS_LOG = coreLinux.CMyLog.getLogger()
    currentPlatform = "Linux"

class CPlatformLogger(object):
    @classmethod
    def isWindowsSystem(cls):
        if 'Windows' in platform.system():
            return True
        else:
            return False

    @classmethod
    def isLinuxSystem(cls):
        if 'Linux' in platform.system():
            return True
        else:
            return False

    @classmethod
    def getPlatform(cls):
        if cls.isWindowsSystem():
            return coreWindows.CMyLog.getLogger(),"Windows",coreWindows.CMyLog
        elif cls.isLinuxSystem():
            return coreLinux.CMyLog.getLogger(),"Linux",coreLinux.CMyLog
        else:
            return None,"unknow"

class CLog(object):
    SYS_LOG,_platform,_Log = CPlatformLogger.getPlatform()

    @classmethod
    def debug(cls):
        return cls.SYS_LOG

    @classmethod
    def info(cls):
        return cls.SYS_LOG

    @classmethod
    def warn(cls):
        return cls.SYS_LOG

    @classmethod
    def error(cls):
        return cls.SYS_LOG

    @classmethod
    def critical(cls):
        return cls.SYS_LOG


class CSysLog():
    error= CLog.error().error
    info= CLog.info().info
    critical= CLog.critical().critical
    warn= CLog.warn().warn
    debug= CLog.debug().debug
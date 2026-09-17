import math
import sys
import ctypes
from .clib_lookup import CLIBLookup

class timespec(ctypes.Structure):
    _fields_ = [("sec", ctypes.c_long), ("nsec", ctypes.c_long)]
    __slots__ = [name for name,type in _fields_]

    @classmethod
    def from_seconds(cls, secs):
        c = cls()
        c.seconds = secs
        return c
    
    @property
    def seconds(self):
        return self.sec + self.nsec / 1000000000

    @seconds.setter
    def seconds(self, secs):
        x, y = math.modf(secs)
        self.sec = int(y)
        self.nsec = int(x * 1000000000)


class itimerspec(ctypes.Structure):
    _fields_ = [("interval", timespec),("value", timespec)]
    __slots__ = [name for name,type in _fields_]
    
    @classmethod
    def from_seconds(cls, interval, value):
        spec = cls()
        spec.interval.seconds = interval
        spec.value.seconds = value
        return spec


if sys.platform.startswith("linux"):
    # function timerfd_create
    timerfd_create = CLIBLookup("timerfd_create", ctypes.c_int, (ctypes.c_long, ctypes.c_int))

    # function timerfd_settime
    timerfd_settime = CLIBLookup("timerfd_settime", ctypes.c_int, (ctypes.c_int, ctypes.c_int, ctypes.POINTER(itimerspec), ctypes.POINTER(itimerspec)))

    # function timerfd_gettime
    timerfd_gettime = CLIBLookup("timerfd_gettime", ctypes.c_int, (ctypes.c_int, ctypes.POINTER(itimerspec)))
else:
    # timerfd is Linux-only (no equivalent syscall on macOS/BSD).
    # thread.py falls back to a plain sleep-based loop on non-Linux
    # platforms, so these are never called there.
    timerfd_create = None
    timerfd_settime = None
    timerfd_gettime = None

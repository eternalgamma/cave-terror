#from cx_Freeze import setup, Executable
#
#setup(name = "Cave Terror", 
#      version = "1.1",
#      description = "",
#      executables = [Executable("caveterror.py")])

from distutils.core import setup
import py2exe

setup(console=['caveterror.py'])
import os
import ConfigParser
import mapUtils
import fileUtils
from mapConst import *

## Class used to read and save the configuration values
class MapConf():

    init_path = None
    init_width = 450
    init_height = 400
    init_zoom = MAP_MAX_ZOOM_LEVEL
    init_center = ((0,0),(128,128))

    ## Returns the Path to the configuration file
    def get_configpath(self):
        # the config file most be in the DEFAULT_PATH
        configpath = os.path.expanduser(DEFAULT_PATH)
        fileUtils.check_dir(configpath)
        configpath = os.path.join(configpath, 'gmapcatcher.conf')
        return configpath

    ## Initialise all variables
    #  If the file does not exit it will be created
    def __init__(self):
        configpath = self.get_configpath()
        if os.path.exists(configpath):
            self.read(configpath)
        else:
            self.write(configpath)

    ## Write the configuration to the given file
    def write(self, configpath):
        config = ConfigParser.RawConfigParser()
        strSection = 'init'
        config.add_section(strSection)
        if self.init_path:
            config.set(strSection, 'path', self.init_path)
        config.set(strSection, 'width', self.init_width)
        config.set(strSection, 'height', self.init_height)
        config.set(strSection, 'zoom', self.init_zoom)
        config.set(strSection, 'center', self.init_center)

        configfile = open(configpath, 'wb')
        config.write(configfile)

    ## Reads from a given file the configuration
    def read(self, configpath):
        config = ConfigParser.RawConfigParser()
        config.read(configpath)
        strSection = 'init'
        try:
            self.init_width = config.getint(strSection, 'width')
            self.init_height = config.getint(strSection, 'height')
            self.init_zoom = config.getint(strSection, 'zoom')
            strCenter = config.get(strSection, 'center')
            self.init_center = mapUtils.str_to_tuple(strCenter)
            self.init_path = config.get(strSection, 'path')
            if self.init_path.strip().lower() in ['none', '']:
                self.init_path = None
            else:
                # Check directory; If it does not exists try to create it.
                if not os.path.isdir(self.init_path):
                    try:
                        os.mkdir(self.init_path)
                    except Exception:
                        self.init_path = None
        except Exception:
            pass

    ## Write the configuration to the default file
    def save(self):
        configpath = self.get_configpath()
        self.write(configpath)

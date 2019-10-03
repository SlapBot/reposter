import os
import configparser


class Configurer:
    def __init__(self, filename="config.ini"):
        print("initialised")
        self.abs_filename = self.get_abs_filename(filename)
        self.config = configparser.ConfigParser()
        self.config.read(self.abs_filename)
        self.sections = self.config.sections()

    @staticmethod
    def get_abs_filename(filename):
        return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir, os.pardir, filename))

    def get_configuration(self, key, section="REDDIT"):
        try:
            value = self.config[section][key]
        except KeyError:
            print("API KEYS FOR '%s' is not provided in the config.ini file."
                  " Refer back to the docs, or just add the goddamn key." % key)
            return False
        if value:
            return value
        print("The correct API KEY wasn't provided or wasn't provided at all for %s, what the ... okay man"
              " now look back at docs to find how to do that, is pretty simple just one line long. "
              "Lazy ass" % key)
        return False

    def write_configuration(self, key, value, section="REDDIT"):
        self.config.set(section, key, value)
        with open(self.abs_filename, 'w') as configfile:
            self.config.write(configfile)
            configfile.close()
        return value


config = Configurer()

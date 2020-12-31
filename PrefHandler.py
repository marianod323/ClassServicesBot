import xml.etree.ElementTree as ET
import os
import pandas as pd
import shutil
import subprocess


def server_file_check(guild_id):
    return os.path.isfile('servers/'+str(guild_id)+'.xml')


class PrefHandler(object):

    ##
    # Handler initialization
    # @param      guild_id    Guild ID
    ##
    def __init__(self, guild_id):
        if not server_file_check(guild_id):
            shutil.copy('servers/server_model.xml', 'servers/'+str(guild_id)+'.xml')

        self.file_name = 'servers/'+str(guild_id)+'.xml'
        self.tree = ET.parse(self.file_name)
        self.root = self.tree.getroot()
        df = pd.read_csv('languages/lang_dictionary.csv', dtype='string', encoding='utf-8').transpose().values.tolist()
        self.languages = dict(zip(df[0], df[1]))

    def get_lang(self):
        for language in self.languages:
            if self.languages[language] == self.root[0].text:
                return ET.parse('languages/'+language+'.xml').getroot()

        return None

    def set_lang(self, new_lang):
        if new_lang in self.languages.values():
            self.root[0].text = new_lang
            self.tree.write(self.file_name)
            return 1
        else:
            return 0

    def get_timezone(self):
        return self.root.find('timezone').text

    def set_timezone(self, new_timezone):
        if int(new_timezone) in range(-11, 14, 1):
            self.root[1].text = new_timezone
            self.tree.write(self.file_name)
            return 1
        else:
            return 0

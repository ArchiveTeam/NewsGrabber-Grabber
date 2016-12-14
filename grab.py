import os
import random
import string
import subprocess
import threading
import time

import file
import settings


class Grab(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.grabs = {}

    def run(self):
        self.grab()

    def grab(self):
        while True:
            for filename in os.listdir(settings.dir_new_lists):
                while not settings.grab_running:
                    time.sleep(1)

                time.sleep(10)

                if filename.startswith('.'):
                    print filename + 'Invalid JSON file!' 
                    continue

                print filename
                filename_urls = os.path.join(settings.dir_old_lists, filename + '_urls')
                filejson = file.File(os.path.join(settings.dir_new_lists, filename)).read_json()

                if filejson['nick'] != settings.irc_nick:
                    settings.irc_bot.set_nick(filejson['nick'])

                file.File(filename_urls).write_lines(filejson['urls'])
                os.rename(os.path.join(settings.dir_new_lists, filename),
                        os.path.join(settings.dir_old_lists, filename))
                self.grabs[filename] = threading.Thread(target=self.grab_single, args=(filename_urls,))
                self.grabs[filename].daemon = True
                self.grabs[filename].start()

    @staticmethod
    def grab_single(name):
        video_string = '--youtube-dl ' if '-videos' in name else ''
        subprocess.Popen([
                os.path.expanduser('~/.local/bin/grab-site'),
                '--input-file='+name,
                '--level=0',
                '--ua=ArchiveTeam; Googlebot/2.1',
                '--no-sitemaps',
                '--concurrency=5',
                '--1',
                '--warc-max-size=524288000',
                '--wpull-args='+video_string+'--no-check-certificate --timeout=300'
            ],
            stdout=open(os.devnull, 'w'),
            stderr=subprocess.STDOUT)
        time.sleep(60)
        os.remove(name)

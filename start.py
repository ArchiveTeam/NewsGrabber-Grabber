import os
import time

import tools
import log
import settings
import irc
import grab
import upload

def main():
    if os.path.isfile('UPDATE'):
        os.remove('UPDATE')

    settings.init()
    settings.logger = log.Log(settings.log_file_name)
    settings.logger.daemon = True
    settings.logger.start()
    settings.logger.log('Starting grabber {name}'.format(
            name=settings.irc_nick))

    tools.create_dir(settings.dir_ready)
    tools.create_dir(settings.dir_new_lists)
    tools.create_dir(settings.dir_old_lists)

    if not os.path.isfile(settings.target_main):
        raise Exception("Please add a rsync target to file '{target_main}'."
            .format(target_main=settings.target_main))

    settings.irc_bot = irc.IRC()
    settings.irc_bot.daemon = True
    settings.irc_bot.start()
    time.sleep(30)
    settings.upload = upload.Upload()
    settings.upload.daemon = True
    settings.upload.start()
    settings.grab = grab.Grab()
    settings.grab.daemon = True
    settings.grab.start()

    while settings.running:
        if os.path.isfile('STOP'):
            os.remove('STOP')
            open('UPDATE', 'w').close()
            break
        time.sleep(1)

if __name__ == '__main__':
    main()
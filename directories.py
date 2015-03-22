# read configuration file and expand ~ to user directory

import json
import os

with open('config.json') as f:
    config = json.load(f)

datadir = os.path.expanduser(config['datadir'])


def set_filename(extension):
    return os.path.join(datadir, extension)

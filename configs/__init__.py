import os
import yaml
from misc.util import Struct

def load(config):
    # Load config
    config_dir = os.path.join("configs/%s/config.yaml" % config.name)
    with open(config_dir) as config_f:
        config = Struct(**yaml.load(config_f))

    return config

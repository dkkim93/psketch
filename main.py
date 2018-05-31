#!/usr/bin/env python2

import models
import trainers
import worlds
import configs
import logging
import os
import sys
import glob
import traceback
import yaml
from misc.util import Struct


def main():
    config = configure()
    world = worlds.load(config)
    model = models.load(config)
    trainer = trainers.load(config)
    trainer.train(model, world)


def configure():
    # Load config
    with open("config.yaml") as config_f:
        config = Struct(**yaml.load(config_f))
    config = configs.load(config)

    # Set up experiment
    config.experiment_dir = os.path.join("experiments/%s" % config.name)
    if not os.path.exists(config.experiment_dir):
        os.mkdir(config.experiment_dir)
    files = glob.glob(os.path.join(config.experiment_dir, "*"))
    for f in files:
        os.remove(f)

    # Set up logging
    log_name = os.path.join(config.experiment_dir, "run.log")
    logging.basicConfig(
            filename=log_name, level=logging.DEBUG,
            format='%(asctime)s %(levelname)-8s %(message)s')

    def handler(type, value, tb):
        logging.exception("Uncaught exception: %s", str(value))
        logging.exception("\n".join(traceback.format_exception(type, value, tb)))
    sys.excepthook = handler

    logging.info("BEGIN")
    logging.info(str(config))

    return config


if __name__ == "__main__":
    main()

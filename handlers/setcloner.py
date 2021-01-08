#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import subprocess
from telegram.ext import Dispatcher, CommandHandler

from utils.callback import callback_delete_message
from utils.config_loader import config
from utils.restricted import restricted
import fileinput
import os
import sys
from os.path import dirname, abspath

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('gclone', gclone))
    dispatcher.add_handler(CommandHandler('fclone', fclone))


@restricted
def gclone(update, context):
    homedirpath = dirname(dirname(abspath(__file__)))
    for line in fileinput.input(homedirpath+"/config.ini", inplace=True):
        print(line.replace("fclone", "gclone"),end="")
    from utils.config_loader import config
    update.message.reply_text('Succesfully Set to gclone !')
    gclonerpath = homedirpath+'/restart.py'
    runpath = ['python3', gclonerpath ]
    subprocess.Popen(runpath)
    print ("Restarting...")
    os._exit(0)                                      
@restricted
def fclone(update, context):
    homedirpath = dirname(dirname(abspath(__file__)))
    for line in fileinput.input(homedirpath+"/config.ini", inplace=True):
        print(line.replace("gclone", "fclone"),end="")
    from utils.config_loader import config
    rsp = update.message.reply_text('Succesfully Set to fclone !')
    rsp.done.wait(timeout=60)
    message_id = rsp.result().message_id
    if update.message.chat_id < 0:
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, message_id))
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, update.message.message_id))

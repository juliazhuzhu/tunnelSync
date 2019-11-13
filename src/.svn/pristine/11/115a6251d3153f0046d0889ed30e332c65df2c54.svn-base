import time
import os
import subprocess
import sys
import json
import logging
import logging.config
from configparser import ConfigParser

configparser_inst = None
helper_logger = None
setup_env_done = False


def get_configparser_inst(config_path=None):
    global configparser_inst

    if configparser_inst is None:
        if os.path.exists(config_path):
            logging.info("to read config file %s" % config_path)
            config = ConfigParser()
            try:
                config.read(config_path)
            except Exception as e:
                logging.error("failed to parse config file %s (%s)" % (config_path, e))
                sys.exit(10000)
            configparser_inst = config
        else:
            logging.error("config file %s doesn't exist?" % config_path)
            sys.exit(10001)

    return configparser_inst

def setup_logging():
    global helper_logger

    if helper_logger is None:
        log_config = get_configparser_inst().get('utils', 'log_config', fallback='config/log_config.json')
        if os.path.exists(log_config):
            try:
                with open(log_config, 'rt') as f:
                    config = json.load(f)
                    logging.config.dictConfig(config)
                    
                    helper_logger = logging.getLogger(__name__)
                    
                    helper_logger.info("App start logging")
            except Exception as e:
                logging.error("failed to parse log config file %s (%s)" % (log_config, e))
                sys.exit(10002)
        else:
            logging.error("log config file %s doesn't exist?" % log_config)
            sys.exit(10003)

def set_console_logger_level(lvl):
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if not isinstance(handler, logging.handlers.RotatingFileHandler):
            handler.setLevel(lvl)


def halt(description="halt"):
    logging.error("Enter halt: %s" % description)

    raise Exception(description)


def setup_env(config_path='config/tunnelSync.ini'):
    global setup_env_done

    if not setup_env_done:
        logging.info("Setup env begin")
        get_configparser_inst(config_path=config_path)
        setup_logging()

        logging.info("Setup env done")

        setup_env_done = True


def get_service_host_list(service_name="haishen_redis"):
    result_ok = True
    err_msg = ""
    hosts = []

    cmd = "getent hosts tasks.%s | awk ' { print $1 }'" % service_name
    logging.debug("to execute: %s" % cmd)
    cmd_result = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE)
    if cmd_result.returncode != 0:
        logging.error("execute finished: %s, result %s : %s" % (cmd, cmd_result.returncode, cmd_result.stdout))
        result_ok = False
        err_msg = cmd_result.stdout
    else:
        logging.debug("execute finished: %s, result %s : %s" % (cmd, cmd_result.returncode, cmd_result.stdout))
        hosts = cmd_result.stdout.strip().split('\n')

    return result_ok, err_msg, hosts


def get_host_ip(host_name=None):
    result_ok = True
    err_msg = ""
    host_ip = None

    if host_name is None:
        cmd = "grep $HOSTNAME /etc/hosts | awk '{print $1;}'"
    else:
        cmd = "grep %s /etc/hosts | awk '{print $1;}'" % host_name
    logging.info("to execute: %s" % cmd)
    cmd_result = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE)
    if cmd_result.returncode != 0:
        logging.error("execute finished: %s, result %s : %s" % (cmd, cmd_result.returncode, cmd_result.stdout))
        result_ok = False
        err_msg = cmd_result.stdout
    else:
        logging.debug("execute finished: %s, result %s : %s" % (cmd, cmd_result.returncode, cmd_result.stdout))
        host_ip = cmd_result.stdout.strip().split('\n')[0]

    return result_ok, err_msg, host_ip

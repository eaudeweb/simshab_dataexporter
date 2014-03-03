from os import environ
import logging
import logging.config

from make_report import make_report

logger = logging.getLogger('ExportXML')


def zope(self):
    """ Call this function from ZOPE
    """
    args_form = self.REQUEST.form

    logger.info("Just started from ZOPE!")

    class RequestFormToArgs(object):
        def __init__(self, args_form):
            self.action = args_form['action']
            self.type = args_form['type']
            self.xml_path = environ.get(
                "SIMS_OUT_PATH", '/var/local/cdr/var/sims_out')

    args = RequestFormToArgs(args_form)
    return make_report(args)


def command_line():
    from argparse import ArgumentParser

    logging.config.fileConfig('etc/log.conf', disable_existing_loggers=False)

    logger.info("Just started from command line!")

    parser = ArgumentParser(description="export data to xml format")
    parser.add_argument("action", help=("action type; choise between"
                                        "report or checklist"),
                        choices=["report", "checklist"])
    parser.add_argument("type", help=("the type it applies to action"
                                      "choise between species or habitats"),
                        choices=["species", "habitats"])
    args = parser.parse_args()
    args.xml_path = environ.get("SIMS_OUT_PATH")
    return make_report(args)

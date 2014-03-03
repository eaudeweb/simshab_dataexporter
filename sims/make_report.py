import logging

from checklistgenerator import ChecklistGenerator
from configloader import ConfigLoader
from reportgenerator import ReportGenerator
from utils import generate_file_name

logger = logging.getLogger('utils')


def make_report(args):
    configLoader = ConfigLoader(args.action, args.type)

    if args.action == "report":
        action = ReportGenerator(args.type, configLoader)
    elif args.action == "checklist":
        action = ChecklistGenerator(args.type, configLoader)
    else:
        assert False
    xml_string = action()
    return xml_string

    logger.info("Generated filename: {0} with success".format(fileNameExport))

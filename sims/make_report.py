import logging

from checklistgenerator import ChecklistGenerator
from configloader import ConfigLoader
from reportgenerator import ReportGenerator
from utils import generate_file_name

logger = logging.getLogger('utils')


def make_report(args):
    configLoader = ConfigLoader(args.action, args.type)

    fileNameExport = generate_file_name(
        args.xml_path, configLoader.country, "_{0}".format(
            configLoader.file_name))

    with open(fileNameExport, "w") as xml_file:
        if args.action == "report":
            action = ReportGenerator(args.type, configLoader)
        elif args.action == "checklist":
            action = ChecklistGenerator(args.type, configLoader)
        else:
            assert False
        xml_string = action()
        xml_file.write(xml_string)

    logger.info("Generated filename: {0} with success".format(fileNameExport))

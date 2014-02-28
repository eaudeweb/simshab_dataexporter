import datetime
import logging
import os.path

from sims.checklistgenerator import ChecklistGenerator
from sims.configloader import ConfigLoader
from sims.reportgenerator import ReportGenerator

logger = logging.getLogger('utils')


def generate_file_name(folderName, CountryCode, xmlFileNameSpecies):
    """
    Generate file name export like in the VB program
    """
    filename = "{0}{1}-{2}.xml".format(
        CountryCode, xmlFileNameSpecies,
        datetime.datetime.now().strftime("%y%m%d-%H%M%S"))
    return os.path.join(folderName, filename)


def getValueFromGeneric(record, item):
    """Always return str
    """
    if type(record) is dict:
        value = record[item]
    else:
        value = getattr(record, item)

    return str(value) if value is not None else ""


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

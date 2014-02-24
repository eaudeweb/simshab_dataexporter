import logging
import logging.config

from configloader import ConfigLoader
from utils import generate_file_name
from checklistgenerator import ChecklistGenerator
from reportgenerator import ReportGenerator

logger = logging.getLogger('ExportXML')
logging.config.fileConfig('etc/log.conf', disable_existing_loggers=False)


def zope(self):
    """ Stuff
    """
    args = self.REQUEST.form
    #return generate_report(args)
    return args

if __name__ == "__main__":
    from argparse import ArgumentParser

    logger.info("Just started !")

    parser = ArgumentParser(description="export data to xml format")
    parser.add_argument("xml_path",
                        help="path to location for saving xml file")
    parser.add_argument("action", help=("action type; choise between"
                                        "report or checklist"),
                        choices=["report", "checklist"])
    parser.add_argument("type", help=("the type it applies to action"
                                      "choise between species or habitats"),
                        choices=["species", "habitats"])

    args = parser.parse_args()
    configLoader = ConfigLoader(args.action, args.type)

    fileNameExport = generate_file_name(
        args.xml_path, configLoader.country, "_{0}".format(
            configLoader.file_name))

    with open(fileNameExport, "w") as xml_file:
        if args.action == "report":
            action = ReportGenerator(args.type, configLoader)
        elif args.action == "checklist":
            action = ChecklistGenerator(configLoader)
        else:
            assert False
        xml_string = action()
        xml_file.write(xml_string)

    logger.info("Generated filename: {0} with success".format(fileNameExport))

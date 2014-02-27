
from sims.configloader import ConfigLoader
from sims.utils import generate_file_name
from sims.checklistgenerator import ChecklistGenerator
from sims.reportgenerator import ReportGenerator

#logger = logging.getLogger('ExportXML')
#logging.config.fileConfig('etc/log.conf', disable_existing_loggers=False)


def zope(self):
    """ Stuff
    """
    import os
    args_form = self.REQUEST.form
    class tmp(object):
        def __init__(self, args_form):
            self.action = args_form['action'] 
            self.type = args_form['type']
    args = tmp(args_form)
    configLoader = ConfigLoader(args.action, args.type)
    file_name = os.environ.get("SIMS_OUT_PATH", '/var/local/cdr/var/sims_out')
    fileNameExport = generate_file_name(
        file_name, configLoader.country, "_{0}".format(
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
    return "Generate with success {0}".format(fileNameExport)

if __name__ == "__main__":
    from argparse import ArgumentParser
    import logging
    import logging.config

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
            action = ChecklistGenerator(args.type, configLoader)
        else:
            assert False
        xml_string = action()
        xml_file.write(xml_string)

    logger.info("Generated filename: {0} with success".format(fileNameExport))

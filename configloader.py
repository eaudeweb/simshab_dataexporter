import ConfigParser


class ConfigLoader(object):
    """ Load all configuration from etc/cnf.ini
    """
    def __init__(self, action, action_type):
        """ action_type can be species or habitats
        """
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read('etc/cnf.ini')

        if action == "report":
            if action_type == "species":
                section = "SPECIES_REPORT"
            elif action_type == "habitats":
                section = "HABITATS_REPORT"
            else:
                assert False
            self.xml_report_tag = self.parser.get(section, "XML_REPORT_TAG")
            self.table_name = self.parser.get(section, "TABLE_NAME")
        elif action == "checklist":
            if action_type == "species":
                section = "SPECIES_CHECKLIST"
            elif action_type == "habitats":
                section = "HABITATS_CHECKLIST"
            else:
                assert False

        self.file_name = self.parser.get(section, "XML_FILE_NAME")
        self.xml_root_tag = self.parser.get(section, "XML_ROOT_TAG")
        self.xml_schema = self.parser.get(section, "XML_SCHEMA")

        self.xml_lang = self.parser.get("GENERAL", "XML_LANG")
        self.country = self.parser.get("GENERAL", "COUNTRY")

        self.dialect = self.parser.get("SQLALCHEMY", "dialect")
        self.username = self.parser.get("SQLALCHEMY", "username")
        self.password = self.parser.get("SQLALCHEMY", "password")
        self.hostname = self.parser.get("SQLALCHEMY", "hostname")

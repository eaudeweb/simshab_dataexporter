import ConfigParser


class ConfigLoader(object):
    """ Load all configuration from etc/cnf.ini
    """
    def __init__(self):
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read('etc/cnf.ini')

        self.xml_root_tag_species = self.parser.get("GENERAL",
                                                    "XML_ROOT_TAG_SPECIES")
        self.xml_root_tag_habitats = self.parser.get("GENERAL",
                                                     "XML_ROOT_TAG_HABITATS")
        self.xml_schema_species = self.parser.get("GENERAL",
                                                  "XML_SCHEMA_SPECIES")
        self.xml_lang = self.parser.get("GENERAL", "XML_LANG")
        self.xml_report_tag_species = self.parser.get("GENERAL",
                                                      "XML_REPORT_TAG_SPECIES")
        self.xml_report_tag_habitats = self.parser.get(
            "GENERAL", "XML_REPORT_TAG_HABITATS")
        self.table_name_species = self.parser.get("GENERAL",
                                                  "TABLE_NAME_SPECIES")
        self.table_names_habitats = self.parser.get("GENERAL",
                                                    "TABLE_NAME_HABITATS")

        self.dialect = self.parser.get("SQLALCHEMY", "dialect")
        self.username = self.parser.get("SQLALCHEMY", "username")
        self.password = self.parser.get("SQLALCHEMY", "password")
        self.hostname = self.parser.get("SQLALCHEMY", "hostname")


configLoader = ConfigLoader()

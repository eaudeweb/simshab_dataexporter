from configloader import configLoader


class ReportAttributes(object):
    """Return specific attributes for report: habitat or species
    """
    def __init__(self, report_type):
        def make_attributes(table_name, xml_root_tag, xml_report_tag):
            """Create all attributes to the object
            """
            self.table_name = table_name
            self.xml_root_tag = xml_root_tag
            self.xml_report_tag = xml_report_tag

        if report_type == "species":
            make_attributes(configLoader.table_name_species,
                            configLoader.xml_root_tag_species,
                            configLoader.xml_report_tag_species)
        elif report_type == "habitats":
            make_attributes(configLoader.table_names_habitats,
                            configLoader.xml_root_tag_habitats,
                            configLoader.xml_report_tag_habitats)

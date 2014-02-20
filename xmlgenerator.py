from lxml import etree


class XMLGenerator(object):
    def __init__(self, xml_root_tag, xml_schema_species):
        NS = 'http://www.w3.org/2001/XMLSchema-instance'
        location_attribute = '{%s}noNameSpaceSchemaLocation' % NS

        self.export_xml = etree.Element(
            xml_root_tag, attrib={location_attribute: xml_schema_species})
        """
        set the language
        """
        self.export_xml.attrib['{http://www.w3.org/XML/1998/namespace}lang'] =\
            "en"

    def append(self, node):
        self.export_xml.append(node)

    def __str__(self):
        return etree.tostring(self.export_xml, pretty_print=True,
                              xml_declaration=True, encoding='UTF-8')

from lxml import etree
from simshab_schemes import engine


def generateNewNode(root, node_name, node_text=None, attrib={}):
    """
    root: the parent node. Can be None
    node_name: the name of the node
    node_text: the text of the node. Can be None.
    attrib: node's attrib. Can be None
    """
    new_node = etree.Element(node_name)
    if node_text is not None:
        new_node.text = str(node_text)

    new_node.attrib.update(attrib)
    if root is not None:
        root.append(new_node)

    return new_node


def xmlDescAttributeValue(fieldValue, descRelation):
    if descRelation is None:
        return ""
    try:
        return str(engine.execute(
            "SELECT {0}'{1}'".format(descRelation, fieldValue)).first()[0])
    except TypeError as ex:
        if "'NoneType' object has no attribute" in ex.message:
            """
            Is happend when select has no records. Should return ""
            """
            return ""
        raise ex


def getCountryISOCode(countryCode):
    return str(engine.execute((
        "select isocode from lu_country_code where"
        " code='{0}'".format(countryCode))).first()[0])


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


class ChecklistGenerator(XMLGenerator):
    """Callable class. It knows how to generate check list xml.
    """
    def __init__(self, configLoader):
        super(ChecklistGenerator, self).__init__(configLoader.xml_root_tag,
                                                 configLoader.xml_schema)
        self.country = configLoader.country

    def __call__(self):
        rs = engine.execute(("select * from data_species_check_list where"
                            " member_state='{0}' order by species_name,"
                            " bio_region").format(self.country))
        rs_lines = [dict(rs_line) for rs_line in rs]

        country_node = generateNewNode(
            None, "country", self.country,
            {"desc": xmlDescAttributeValue(
                rs_lines[0]["member_state"],
                "name from lu_country_code where code="),
             "isocode": getCountryISOCode(self.country)})
        self.export_xml.append(country_node)

        species_list_node = generateNewNode(None, "species_list")
        self.export_xml.append(species_list_node)

        previous_species_code = None

        for rs_line in rs_lines:
            if previous_species_code != rs_line["natura_2000_code"]:
                species_node = generateNewNode(species_list_node, "species")
                generateNewNode(species_node, "code",
                                rs_line["natura_2000_code"])
                generateNewNode(species_node, "eunis_code",
                                rs_line["eunis_code"])
                generateNewNode(species_node, "name", rs_line["species_name"])
                generateNewNode(species_node, "hd_name", rs_line["hd_name"])
                regional_node = generateNewNode(species_node, "regional")

                previous_species_code = rs_line["natura_2000_code"]

            region_node = generateNewNode(regional_node, "region")
            generateNewNode(region_node, "code", rs_line["bio_region"],
                            {"desc": xmlDescAttributeValue(
                                rs_line["bio_region"],
                                "name from lu_biogeoreg where code=")}
                            )
            generateNewNode(region_node, "presence", rs_line["presence"],
                            {"desc": xmlDescAttributeValue(
                                rs_line["presence"],
                                "name from lu_presence where code=")})
            generateNewNode(region_node, "comments", rs_line["comment_"])
            generateNewNode(region_node, "annex_ii", rs_line["annex_ii"])
            generateNewNode(region_node, "ms_added",
                            "true" if rs_line["ms_added"] else "false")
            generateNewNode(region_node, "predefined",
                            "true" if rs_line["predefined"] else "false")

        return self.__str__()

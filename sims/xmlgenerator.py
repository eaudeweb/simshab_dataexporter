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
        location_attribute = '{http://www.w3.org/2001/XMLSchema-instance}noNameSpaceSchemaLocation'
        self.export_xml = etree.Element(
                            xml_root_tag,
                            attrib={
                                location_attribute: xml_schema_species
                            }
                        )
        self.export_xml.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = "en"

    def append(self, node):
        self.export_xml.append(node)

    def __str__(self):
        return etree.tostring(self.export_xml, pretty_print=True,
                              xml_declaration=True, encoding='UTF-8')

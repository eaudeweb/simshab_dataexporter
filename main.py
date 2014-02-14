from lxml import etree
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker
import argparse
import datetime
import logging
import logging.config
import os.path

from configloader import configLoader
from simshab_schemes import DataSpecies
from simshab_schemes import LuCountryCode
from simshab_schemes import ValidateFields
from simshab_schemes import engine


logger = logging.getLogger('ExportXML')
logging.config.fileConfig('etc/log.conf', disable_existing_loggers=False)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


def generateFilename(folderName, CountryCode, xmlFileNameSpecies):
    """
    Generate file name export like in the VB program
    """
    filename = "{0}{1}-{2}.xml".format(
        CountryCode, xmlFileNameSpecies,
        datetime.datetime.now().strftime("%y%m%d-%H%M%S"))
    return os.path.join(folderName, filename)


def xmlAdditionalAttributeValue(tableName, elementName, record):
    if (tableName in ("data_species", "data_greintroduction_of_species")
            and elementName == "speciescode"):
        return {"desc": "", "euniscode": ""}
    elif (tableName in ("data_habitats", "data_species", "data_greport")
            and elementName == "country"):
        return {"isocode": '"{0}"'.format(
            session.query(LuCountryCode).filter(
                LuCountryCode.code == record.country).first().isocode)}
    return {}


def xmlDescAttributeValue(fieldValue, descRelation):
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


def xmlCalculateField(record, fieldName):
    if fieldName == "species_name":
        try:
            return str(
                engine.execute(
                    "select species_name from data_species_check_list where "
                    "member_state='{0}' and natura_2000_code='{1}'".format(
                        record.country, record.speciescode)).first()[0])
        except TypeError as ex:
            if "'NoneType' object has no attribute" in ex.message:
                """
                Is happend when select has no records. Should return ""
                """
                return ""
            raise ex

    return ""


def getTagItems(tableName):
    """
    generate validate fields
    """
    return session.query(ValidateFields).filter(
        ValidateFields.table_name == tableName).order_by(
        ValidateFields.table_name, ValidateFields.xml_order).all()


def convertLinkTableToXML(rootNode, foreign_key, value, table_name,
                          groupElementName, elementName, tableType):
    related_values = engine.execute(
        "select * from {0} where {1}={2}".format(
            table_name, foreign_key, value))
    logger.debug("------select * from {0} where {1}={2}".format(
        table_name, foreign_key, value))

    for related_value in related_values:
        newRootNode = etree.Element(groupElementName)

        tableTagItems = getTagItems(table_name)

        convertRecordToXML(newRootNode, dict(related_value),
                           table_name, tableTagItems)
        rootNode.append(newRootNode)


def getValueFromGeneric(record, item):
    if type(record) is dict:
        value = record[item]
    else:
        value = getattr(record, item)
    return value


def convertRecordToXML(rootNode, record, tableName, tableTagItems):
    """
    rootNode: the root node for all nodes generated by convertRecordToXML
    record: record to get values
    tableName: tableName to get additional attributes
    tableTagItems: xml generator
    """
    previousTagGroup = None

    for idx in range(len(tableTagItems)):
        item = tableTagItems[idx]

        if item.xml_tag_section != previousTagGroup:
            if previousTagGroup is not None:
                return
            if item.xml_tag_section is not None:
                newRootNode = etree.Element(item.xml_tag_section)
                convertRecordToXML(newRootNode, record, tableName,
                                   tableTagItems[idx + 1:])
                rootNode.append(newRootNode)

        #print "*************", item.table_name, "$->", item.field_name
        #if item.table_name == "data_pressures_threats" and \
        #        item.field_name == "data_pressures_threats_pol":
            #import ipdb;ipdb.set_trace()
        if item.is_related_table:
            value = getValueFromGeneric(record, item.primary_key_field)

            convertLinkTableToXML(
                rootNode,
                item.foreign_key_field,
                value,
                item.field_name,
                item.xml_tag,
                item.xml_tag,
                item.table_filter)
        else:
            try:
                fieldValue = getValueFromGeneric(record, item.field_name)
            except (AttributeError, KeyError):
                fieldValue = xmlCalculateField(record, item.field_name)

            additionalAttributesValue = xmlAdditionalAttributeValue(
                tableName, item.field_name, record)
            descValue = None
            if item.xml_desc_relation is not None:
                descValue = xmlDescAttributeValue(fieldValue,
                                                  item.xml_desc_relation)

            el = etree.Element(item.field_name,
                               desc=descValue if descValue is not None else "")
            el.attrib.update(additionalAttributesValue)
            el.text = str(fieldValue) if fieldValue is not None else ""
            rootNode.append(el)

if __name__ == "__main__":
    logger.info("Just started !")

    parser = argparse.ArgumentParser(description="export data to xml format")
    parser.add_argument("xml_path",
                        help="path to location for saving xml file")
    args = parser.parse_args()

    try:
        tableTagItems = getTagItems('data_species')

        speciesRs = session.query(DataSpecies).filter(
            DataSpecies.export == 1).all()

        export_xml = etree.Element(
            configLoader.xml_root_tag_species,
            xml_lang=configLoader.xml_lang,
            xsi_noNamespaceSchemaLocation=configLoader.xml_schema_species)
        for specie in speciesRs:
            specie_tag = etree.Element(configLoader.xml_report_tag_species)
            xml_nodes = convertRecordToXML(specie_tag, specie, "data_species",
                                           tableTagItems)
            export_xml.append(specie_tag)

        fileNameExport = generateFilename(
            args.xml_path, "RO", "_species_reports")
        with open(fileNameExport, "w") as xml_file:
            xml_file.write(etree.tostring(export_xml, pretty_print=True))
        logger.info("Generated filename: {0} with success".format(
            fileNameExport))

    except DatabaseError as ex:
        logger.critical("{0}".format(ex))

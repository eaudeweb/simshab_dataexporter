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
    return str(engine.execute(
        "SELECT {0}'{1}'".format(descRelation, fieldValue)).first()[0])


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


def convertRecordToXML(record, elementName, tableName, tableTagItems):
    xml_nodes = []
    for item in tableTagItems:
        try:
            fieldValue = getattr(record, item.field_name)
        except AttributeError:
            fieldValue = xmlCalculateField(record, item.field_name)

        descRelation = item.xml_desc_relation
        additonalAttributesValue = xmlAdditionalAttributeValue(
            tableName, item.field_name, record)
        if descRelation is not None:
            descValue = xmlDescAttributeValue(fieldValue, descRelation)

        el = etree.Element(item.field_name,
                           desc=descValue if descValue is not None else "")
        el.attrib.update(additonalAttributesValue)
        el.text = str(fieldValue) if fieldValue is not None else ""
        #logger.debug("{0}".format(etree.tostring(el, pretty_print=True)))
        xml_nodes.append(el)
    return xml_nodes

if __name__ == "__main__":
    logger.info("Just started !")

    parser = argparse.ArgumentParser(description="export data to xml format")
    parser.add_argument("xml_path",
                        help="path to location for saving xml file")
    args = parser.parse_args()

    try:
        tableTagItems = session.query(ValidateFields).filter(
            ValidateFields.table_name == 'data_species').order_by(
            ValidateFields.table_name, ValidateFields.xml_order).all()
        speciesRs = session.query(DataSpecies).filter(
            DataSpecies.export == 1).all()

        export_xml = etree.Element(
            configLoader.xml_root_tag_species,
            xml_lang=configLoader.xml_lang,
            xsi_noNamespaceSchemaLocation=configLoader.xml_schema_species)
        for specie in speciesRs:
            specie_tag = etree.Element(configLoader.xml_report_tag_species)
            xml_nodes = convertRecordToXML(specie, "species", "data_species",
                                           tableTagItems)
            for xml_node in xml_nodes:
                specie_tag.append(xml_node)
            export_xml.append(specie_tag)

        fileNameExport = generateFilename(
            args.xml_path, "RO", "_species_reports")
        with open(fileNameExport, "w") as xml_file:
            xml_file.write(etree.tostring(export_xml, pretty_print=True))
        logger.info("Generated filename: {0} with success".format(
            fileNameExport))

    except DatabaseError as ex:
        logger.critical("{0}".format(ex))

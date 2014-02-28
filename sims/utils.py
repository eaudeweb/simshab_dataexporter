import datetime
import os.path


def generate_file_name(folderName, CountryCode, xmlFileNameSpecies):
    """
    Generate file name export like in the VB program
    """
    filename = "{0}{1}-{2}.xml".format(
        CountryCode, xmlFileNameSpecies,
        datetime.datetime.now().strftime("%y%m%d-%H%M%S"))
    return os.path.join(folderName, filename)


def getValueFromGeneric(record, item):
    """Always return str
    """
    if type(record) is dict:
        value = record[item]
    else:
        value = getattr(record, item)

    return str(value) if value is not None else ""

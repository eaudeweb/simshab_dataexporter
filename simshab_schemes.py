from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine(
    'oracle+cx_oracle://reportdata_owner:simshab@power.edw.ro')


class ValidateFields(Base):
    __tablename__ = u'validate_fields'

    id = Column('objectid', Integer, primary_key=True)
    table_name = Column(String)
    field_name = Column(String)
    table_filter = Column(String)
    label = Column(String)
    field_type = Column(String)
    mask = Column(String)
    optional = Column(Integer)
    rule = Column(String)
    xml_tag = Column(String)
    xml_tag_section = Column(String)
    xml_desc_relation = Column(String)
    xml_import = Column('import', Integer)
    xml_order = Column(Integer)
    is_related_table = Column(Integer)
    foreign_key_field = Column(String)
    primary_key_field = Column(String)

    def __repr__(self):
        return "<ValidateFields(id: {0}, table_name: {1},field_name: {2},"\
            "table_filter: {3}, label: {4}, field_type: {5}, mask: {6}, "\
            "optional: {7}, rule: {8}, xml_tag: {9}, xml_tag_section: {10}, "\
            "xml_desc_relation: {11}, xml_import: {12}, xml_order: {13}, "\
            "is_related_table: {14}, foreign_key_field: {15},"\
            "primary_key_field: {16}"\
            "".format(
                self.id, self.table_name, self.field_name, self.table_filter,
                self.label, self.field_type, self.mask, self.optional,
                self.rule, self.xml_tag, self.xml_tag_section,
                self.xml_desc_relation, self.xml_import, self.xml_order,
                self.is_related_table, self.foreign_key_field,
                self.primary_key_field)


class DataSpecies(Base):
    __tablename__ = u'data_species'

    species_id = Column("objectid", Integer, primary_key=True)
    country = Column(String)
    speciescode = Column(Integer)
    alternative_speciesname = Column(String)
    common_speciesname = Column(String)
    distribution_map = Column(Integer)
    sensitive_species = Column(Integer)
    distribution_method = Column(String)
    distribution_date = Column(String)
    additional_distribution_map = Column(Integer)
    range_map = Column(Integer)
    validated = Column(Integer)
    validation_date = Column(Date)
    sys_date_created = Column(Date)
    sys_date_modified = Column(Date)
    sys_date_imported = Column(Date)
    sys_creator_id = Column(String)
    sys_modifier_id = Column(String)
    export = Column(Integer)
    import_id = Column(Integer)

    def __repr__(self):
        return "<DataSpecies(id: {0}, country: {1}, speciescode: {2}, "\
            "alternative_speciesname: {3}, common_speciesname: {4}, "\
            "distribution_map: {5}, sensitive_species: {6}, "\
            "distribution_method: {7}, distribution_date: {8}, "\
            "additional_distribution_map{9}, range_map {10}, "\
            "validated: {11}, validation_date: {12}, "\
            "sys_date_created: {13}, sys_date_modified: {14}"\
            "sys_date_imported: {15}, sys_creator_id: {16}"\
            "sys_modifier_id: {17}, export: {18}, import_id: {19}"\
            "".format(
                self.species_id,
                self.country,
                self.speciescode,
                self.alternative_speciesname,
                self.common_speciesname,
                self.distribution_map,
                self.sensitive_species,
                self.distribution_method,
                self.distribution_date,
                self.additional_distribution_map,
                self.range_map,
                self.validated,
                self.validation_date,
                self.sys_date_created,
                self.sys_date_modified,
                self.sys_date_imported,
                self.sys_creator_id,
                self.sys_modifier_id,
                self.export,
                self.import_id
            )


class LuRanking(Base):
    __tablename__ = u'lu_ranking'

    id = Column("objectid", Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    note = Column(String)
    order = Column(Integer)

    def __repr__(self):
        return "<LuRanking (id: {0}, code: {1}, name: {2}, "\
               "note: {3}, order: {4}"\
               "".format(
                   self.id,
                   self.code,
                   self.name,
                   self.note,
                   self.order
               )


class LuCountryCode(Base):
    __tablename__ = u'lu_country_code'

    id = Column("objectid", Integer, primary_key=True)
    isocode = Column(String)
    code = Column(String)
    name = Column(String)
    order_ = Column(Integer)

    def __repr__(self):
        return "<LuCountryCode(id: {0}, isocode: {1}, code: {2}, "\
               "name: {3}, order_: {4}"\
               "".format(
                   self.id,
                   self.isocode,
                   self.code,
                   self.name,
                   self.order_
               )


class DataHabitats(Base):
    __tablename__ = u"data_habitats"

    habitat_id = Column("objectid", Integer, primary_key=True)

    country = Column(String)
    habitatcode = Column(String)
    distribution_map = Column(Integer)
    distribution_method = Column(String)
    distribution_date = Column(String)
    additional_distribution_map = Column(Integer)
    range_map = Column(Integer)
    sys_date_created = Column(Date)
    sys_date_modified = Column(Date)
    sys_date_imported = Column(Date)
    sys_creator_id = Column(String)
    sys_modifier_id = Column(String)
    validated = Column(Integer)
    validation_date = Column(Date)
    export = Column(Integer)
    import_id = Column(Integer)
    globalid = Column(String)

#    def __repr__(self):
#        return "<DataHabitats(id: {0},
#country: {1}
#habitatcode: {2}
#distribution_map {3}
#distribution_method {4}
#distribution_date {5}
#additional_distribution_map
#range_map
#sys_date_created
#sys_date_modified
#sys_date_imported
#sys_creator_id
#sys_modifier_id
#validated
#validation_date
#export
#import_id
#globalid

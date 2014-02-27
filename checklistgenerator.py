from sims.xmlgenerator import XMLGenerator
from sims.simshab_schemes import engine
from sims.xmlgenerator import generateNewNode
from sims.xmlgenerator import xmlDescAttributeValue
from sims.xmlgenerator import getCountryISOCode


class ChecklistGenerator(XMLGenerator):
    """Callable class. It knows how to generate check list xml.
    """
    def __init__(self, report_type, configLoader):
        super(ChecklistGenerator, self).__init__(configLoader.xml_root_tag,
                                                 configLoader.xml_schema)
        self.country = configLoader.country
        self.table_name = configLoader.table_name
        self.report_type =  report_type

    def __call__(self):
        if self.report_type == "species":
            rs = engine.execute(("select * from {0} where"
                                " member_state='{1}' order by species_name,"
                                " bio_region").format(self.table_name,
                                                    self.country))
        elif self.report_type == "habitats":
            rs = engine.execute(("select * from {0} where"
                                " ms='{1}' order by natura_2000_code,"
                                " bio_region").format(self.table_name,
                                                    self.country))
        rs_lines = [dict(rs_line) for rs_line in rs]

        if self.report_type == "species":
            country_node = generateNewNode(
                None, "country", self.country,
                {"desc": xmlDescAttributeValue(
                    rs_lines[0]["member_state"],
                    "name from lu_country_code where code="),
                "isocode": getCountryISOCode(self.country)})
        elif self.report_type == "habitats":
            country_node = generateNewNode(
                None, "country", self.country,
                {"desc": xmlDescAttributeValue(
                    rs_lines[0]["ms"],
                    "name from lu_country_code where code="),
                "isocode": getCountryISOCode(self.country)})

        self.export_xml.append(country_node)

        list_node = generateNewNode(
            None, "species_list" if self.report_type == "species"\
            else "habitats")
        self.export_xml.append(list_node)

        previous_species_code = None

        for rs_line in rs_lines:
            if previous_species_code != rs_line["natura_2000_code"]:
                if self.report_type == "species":
                    species_node = generateNewNode(list_node, "species")
                    generateNewNode(species_node, "code",
                                    rs_line["natura_2000_code"])
                    generateNewNode(species_node, "eunis_code",
                                    rs_line["eunis_code"])
                    generateNewNode(species_node, "name", rs_line["species_name"])
                    generateNewNode(species_node, "hd_name", rs_line["hd_name"])
                    regional_node = generateNewNode(species_node, "regional")
                elif self.report_type == "habitats":
                    habitats_node = generateNewNode(list_node, "habitat")
                    generateNewNode(habitats_node, "code",
                                    rs_line["natura_2000_code"])
                    generateNewNode(habitats_node, "name",
                                    rs_line["valid_name"])
                    generateNewNode(habitats_node, "legal_name",
                                    rs_line["hd_name"])
                    regional_node = generateNewNode(habitats_node, "regional")

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
            generateNewNode(region_node, "comments", rs_line[
                "comment_" if self.report_type == "species" \
                else "ms_feedback_etcbd_comments"])
            if self.report_type == "species":
                generateNewNode(region_node, "annex_ii", rs_line["annex_ii"])
            generateNewNode(region_node, "ms_added",
                            "true" if rs_line["ms_added"] else "false")
            generateNewNode(region_node, "predefined",
                            "true" if rs_line["predefined"] else "false")

        return self.__str__()

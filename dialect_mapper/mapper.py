import csv
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from . import mapping_data

# A bunch of methods that makes querying dialectal relationships easier
# Code created by Phoebe Parsons on Jan 14 2022
# the CSV file was created by Phoebe Parsons via reading dialectal maps,
# scraping Wikipedia, and manual correction (with feedback from Per Erik Solberg)

# Many of these methods could be improved via the use of Pandas. But, I 
# didn't want to force any other potential users to install Pandas as well

class mapper_methods:
    # ----------------- NAMED dialect methods -----------------
    def get_old_municipalities_from_named_dialect(self, named_dialect: str) -> list:
        return sorted(list(set([x[0] for x in self.raw_csv_data if x[4].lower().strip() == named_dialect.lower().strip()])))
    def get_new_municipalities_from_named_dialect(self, named_dialect: str) -> list:
        return sorted(list(set([x[1] for x in self.raw_csv_data if x[4].lower().strip() == named_dialect.lower().strip()])))
    def get_old_counties_from_named_dialect(self, named_dialect: str) -> list:
        return sorted(list(set([x[2] for x in self.raw_csv_data if x[4].lower().strip() == named_dialect.lower().strip()])))
    def get_new_counties_from_named_dialect(self, named_dialect: str) -> list:
        return sorted(list(set([x[3] for x in self.raw_csv_data if x[4].lower().strip() == named_dialect.lower().strip()])))

    def get_named_dialect_by_old_municipality(self, old_municipality) -> list:
        return sorted(list(set([x[4] for x in self.raw_csv_data if x[0].lower().strip() == old_municipality.lower().strip()])))
    def get_named_dialect_by_new_municipality(self, new_municipality) -> list:
        return sorted(list(set([x[4] for x in self.raw_csv_data if x[1].lower().strip() == new_municipality.lower().strip()])))
    def get_named_dialect_by_old_county(self, old_county) -> list:
        return sorted(list(set([x[4] for x in self.raw_csv_data if x[2].lower().strip() == old_county.lower().strip()])))
    def get_named_dialect_by_new_county(self, new_county) -> list:
        return sorted(list(set([x[4] for x in self.raw_csv_data if x[3].lower().strip() == new_county.lower().strip()])))
    
    def get_named_dialect(self, lookup_by: str):
        # by looking up by old municipality first we're prioritizing it. I don't have a super strong arguement as to the why,
        # presumably old municipalities will have fewer one to many mappings. But, if we feel like going with the new municipalities
        # is better this can easily be changed
        dialects = self.get_named_dialect_by_old_municipality(lookup_by)
        if len(dialects) > 0:
            return dialects[0] if len(dialects) == 1 else dialects
        else:
            dialects = self.get_named_dialect_by_new_municipality(lookup_by)
            if len(dialects) > 0:
                return dialects[0] if len(dialects) == 1 else dialects
            else:
                dialects = self.get_named_dialect_by_old_county(lookup_by)
                if len(dialects) > 0:
                    return dialects[0] if len(dialects) == 1 else dialects
                else:
                    dialects = self.get_named_dialect_by_new_county(lookup_by)
                    if len(dialects) > 0:
                        return dialects[0] if len(dialects) == 1 else dialects
                    else:
                        print("ERROR: cannot find named dialect for: {}".format(lookup_by))
                        return None

    # ----------------- NUMERIC dialect methods -----------------
    def get_old_municipalities_from_numeric_dialect(self, named_dialect: str) -> list:
        return sorted(list(set([x[0] for x in self.raw_csv_data if int(x[5]) == int(named_dialect)])))
    def get_new_municipalities_from_numeric_dialect(self, named_dialect: str) -> list:
        return sorted(list(set([x[1] for x in self.raw_csv_data if int(x[5]) == int(named_dialect)])))
    def get_old_counties_from_numeric_dialect(self, named_dialect: str) -> list:
        return sorted(list(set([x[2] for x in self.raw_csv_data if int(x[5]) == int(named_dialect)])))
    def get_new_counties_from_numeric_dialect(self, named_dialect: str) -> list:
        return sorted(list(set([x[3] for x in self.raw_csv_data if int(x[5]) == int(named_dialect)])))

    def get_numeric_dialect_by_old_municipality(self, old_municipality) -> list:
        return sorted(list(set([x[5] for x in self.raw_csv_data if x[0].lower().strip() == old_municipality.lower().strip()])))
    def get_numeric_dialect_by_new_municipality(self, new_municipality) -> list:
        return sorted(list(set([x[5] for x in self.raw_csv_data if x[1].lower().strip() == new_municipality.lower().strip()])))
    def get_numeric_dialect_by_old_county(self, old_county) -> list:
        return sorted(list(set([x[5] for x in self.raw_csv_data if x[2].lower().strip() == old_county.lower().strip()])))
    def get_numeric_dialect_by_new_county(self, new_county) -> list:
        return sorted(list(set([x[5] for x in self.raw_csv_data if x[3].lower().strip() == new_county.lower().strip()])))
    
    def get_numeric_dialect(self, lookup_by: str):
        # by looking up by old municipality first we're prioritizing it. I don't have a super strong arguement as to the why,
        # presumably old municipalities will have fewer one to many mappings. But, if we feel like going with the new municipalities
        # is better this can easily be changed
        dialects = self.get_numeric_dialect_by_old_municipality(lookup_by)
        if len(dialects) > 0:
            return dialects[0] if len(dialects) == 1 else dialects
        else:
            dialects = self.get_numeric_dialect_by_new_municipality(lookup_by)
            if len(dialects) > 0:
                return dialects[0] if len(dialects) == 1 else dialects
            else:
                dialects = self.get_numeric_dialect_by_old_county(lookup_by)
                if len(dialects) > 0:
                    return dialects[0] if len(dialects) == 1 else dialects
                else:
                    dialects = self.get_numeric_dialect_by_new_county(lookup_by)
                    if len(dialects) > 0:
                        return dialects[0] if len(dialects) == 1 else dialects
                    else:
                        print("ERROR: cannot find numeric dialect for: {}".format(lookup_by))
                        return None

    def __init__(self) -> None:
        self.raw_csv_data = []
        # with open(
        #     pkg_resources.read_text(mapping_data, 'muni_county_namedDialect_numericDialect_mapping_manual_additions_renamed.csv'), # './dialect_mapper/muni_county_namedDialect_numericDialect_mapping_manual_additions_renamed.csv',
        #     'r'
        # ) as f_open:
        cReader = csv.reader(
            StringIO(
                pkg_resources.read_text(
                    mapping_data, 
                    'muni_county_namedDialect_numericDialect_mapping_manual_additions_renamed.csv'
                )
            )
        )
        for row in cReader:
            self.raw_csv_data.append(row)
        headers = self.raw_csv_data.pop(0)

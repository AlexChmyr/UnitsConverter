import json
import re
from pathlib import Path


CATALOG_FILE = "catalog.json"


class Failure(Exception):
    pass


def parse_input(s):
    """Parse a string entered by user"""
    data = {"count": 0,
            "base_unit": "",
            "target_unit": "",
            "base_unit_str": "",
            "target_unit_str": "",
            "base_unit_domain": "",
            "target_unit_domain": "",
            "base_unit_coef": 0,
            "target_unit_coef": 0
            }

    pattern = re.compile(r"""[С|с]колько\s+(?P<bus>.*)\s+в\s+(?P<count>\d+[.|,]?\d*)\s+(?P<tus>.*)""", re.VERBOSE)
    match = pattern.match(s)

    data["base_unit_str"] = match.group("bus")
    data["target_unit_str"] = match.group("tus").replace("?", "")
    data["count"] = float(match.group("count").replace(",", "."))

    if data["base_unit_str"] == "" or data["target_unit_str"] == "" or data["count"] == 0:
        raise Failure("Не понимаю")

    return data


def find_units(data):
    """Looks for units and its coefficient in catalog"""
    catalog = json.loads(Path(CATALOG_FILE).read_text(encoding="utf-8"))

    for d_key, domain in catalog.items():
        for u_key, unit in domain.items():
            for word in unit["thesaurus"]:
                if word == data["base_unit_str"]:
                    data["base_unit"] = u_key
                    data["base_unit_domain"] = d_key
                    data["base_unit_coef"] = unit["coefficient"]
                if word == data["target_unit_str"]:
                    data["target_unit"] = u_key
                    data["target_unit_domain"] = d_key
                    data["target_unit_coef"] = unit["coefficient"]

    if data["base_unit"] == "":
        raise Failure("Неизместная единица \"" + data["base_unit_str"] + "\"")
    if data["target_unit"] == "":
        raise Failure("Неизместная единица \"" + data["target_unit_str"] + "\"")
    if data["base_unit_domain"] != data["target_unit_domain"]:
        raise Failure("Не сравнимо")

    return data


def calculate(inp):
    try:
        data = parse_input(inp)
        data = find_units(data)

        val = data["count"] * data["target_unit_coef"] / data["base_unit_coef"]
        return round(val, 3)

    except Failure as f:
        return str(f)

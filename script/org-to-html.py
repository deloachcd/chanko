from pathlib import Path
import re

import bs4
import orgparse

def normalize_orgl(org_list):
    # TODO replace with a "parse list" function that takes item matching regex as an arg
    "Remove excessive white space from raw org lists"
    return [re.sub("\s+", " ", i) for i in org_list if i != ""]

def parse_orgnode(node):
    "Take an OrgNode object from orgparse and recursively parse it, returning a JSON object"
    def parse_as_list(body, entry_regex):
        list_raw = re.split(entry_regex, body)[1:]
        return [re.sub("\s+", " ", i) for i in list_raw if i != ""]

    n_header = node.get_heading()
    n_body = node.get_body()
    if re.search("^\-\s", n_body):
        body_parsed = parse_as_list(n_body, "\-\s")
        body_format = "UnorderedList"
    elif re.search("^\d*\.\s", n_body):
        body_parsed = parse_as_list(n_body, "\d*\.\s")
        body_format = "OrderedList"
    else:
        body_parsed = n_body.replace("\n", "")
        body_format = "Paragraph"

    children = ([parse_orgnode(child) for child in node.children]
                if node.children != []
                else None)
    r_dict = {
        "Header": n_header,
        "Body": body_parsed,
        "Format": body_format
    }
    if children:
        r_dict["Children"] = children

    return r_dict

for orgfile in Path("recipes/").glob("*.org"):
    root = orgparse.load(orgfile)
    img_path = re.search("\[\[.*\]\]", root.get_body(format="raw")).group()[2:-2]
    level1 = root.children[0]
    page = {
        "ImagePath": img_path,
        "RecipeName": level1.get_heading(),
        "Properties": level1.properties,
        "Content": []
    }
    for level2 in level1.children:
        page["Content"].append(parse_orgnode(level2))
    print(page)

# TODO generate the webpage from the JSON object with BeautifulSoup

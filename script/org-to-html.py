from pathlib import Path
import re
import json

import bs4
import orgparse

from Templates import (
    RecipeBox,
    RecipeBoxTag,
    RecipeInstructionsPage,
    RecipeDetailSection,
)


def parse_orgnode(node):
    "Take an OrgNode object from orgparse and recursively parse it, returning a JSON object"

    def parse_as_list(body, entry_regex):
        list_raw = re.split(entry_regex, body)[1:]
        return [re.sub("\s+", " ", i) for i in list_raw if i != ""]

    n_body = node.get_body()
    if re.search("^\-\s", n_body):
        body_parsed = parse_as_list(n_body, "\-\s")
        body_format = "UnorderedList"
    elif re.search("^\d*\.\s", n_body):
        body_parsed = parse_as_list(n_body, "\d*\.\s")
        body_format = "OrderedList"
    else:
        body_parsed = n_body.replace("\n", " ")
        body_format = "Paragraph"

    children = (
        [parse_orgnode(child) for child in node.children]
        if node.children != []
        else None
    )
    r_dict = {"Header": node.get_heading(), "Body": body_parsed, "Format": body_format}
    if children:
        r_dict["Children"] = children

    return r_dict


index = {"Recipes": [], "Tags": []}
for orgfile in Path("recipes/").glob("*.org"):
    root = orgparse.load(orgfile)
    img_path = re.search("\[\[.*\]\]", root.get_body(format="raw")).group()[2:-2]
    level1 = root.children[0]
    page = {
        "ImagePath": img_path,
        "RecipeName": level1.get_heading(),
        "Properties": level1.properties,
        "FileName": str(orgfile).replace(".org", ".html"),
        "Content": [],
    }
    taglist = []
    # build a list of tags for rendering index page
    for tag in page["Properties"]["Tags"].split(","):
        if tag not in index["Tags"]:
            index["Tags"].append(tag)
        taglist.append(tag)
    # make tag properties into a list for easier parsing
    page["Properties"]["Tags"] = taglist
    for level2 in level1.children:
        page["Content"].append(parse_orgnode(level2))
    # add entry to list for index.json, ignoring page content
    index["Recipes"].append(
        {key: value for key, value in page.items() if key not in ["Content"]}
    )

    detail_sections = [RecipeDetailSection(section) for section in page["Content"]]
    page_html = RecipeInstructionsPage(
        RecipeBox(
            img_path=page["ImagePath"],
            recipe_name=page["RecipeName"],
            prep_time=page["Properties"]["PrepTime"],
            cook_time=page["Properties"]["CookTime"],
            tags=[RecipeBoxTag(tag) for tag in page["Properties"]["Tags"]],
        ),
        [RecipeDetailSection(section) for section in page["Content"]],
    )
    soup = bs4.BeautifulSoup(page_html.render(), "html.parser")
    with open(f"site/{page['FileName']}", "w") as outfile:
        outfile.write(soup.prettify())
        print(f"Successfully converted {orgfile} to {page['FileName']}")
with open("site/recipes/index.json", "w") as outfile:
    outfile.write(json.dumps(index, indent=4))
    print(f"Successfully generated index.json from recipes")

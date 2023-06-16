from pathlib import Path
import re
import json

import bs4
import orgparse

import Templates


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

    detail_sections = [
        Templates.RecipeDetailSection(section) for section in page["Content"]
    ]
    page_html = Templates.RecipeInstructionsPage(
        Templates.RecipeBox(
            img_path=page["ImagePath"],
            recipe_name=page["RecipeName"],
            prep_time=page["Properties"]["PrepTime"],
            cook_time=page["Properties"]["CookTime"],
            tags=[Templates.RecipeBoxTag(tag) for tag in page["Properties"]["Tags"]],
        ),
        [Templates.RecipeDetailSection(section) for section in page["Content"]],
    )
    soup = bs4.BeautifulSoup(page_html.render(), "html.parser")
    with open(f"site/{page['FileName']}", "w") as outfile:
        outfile.write(soup.prettify())
        print(f"Successfully converted {orgfile} to {page['FileName']}")

# build index.html
recipe_boxes = []
for recipe in index["Recipes"]:
    recipe_boxes.append(
        Templates.RecipeBoxLink(
            recipe_name=recipe["RecipeName"],
            img_path=recipe["ImagePath"],
            prep_time=recipe["Properties"]["PrepTime"],
            cook_time=recipe["Properties"]["CookTime"],
            tags=[Templates.RecipeBoxTag(tag) for tag in recipe["Properties"]["Tags"]],
        )
    )
# build columns divs from list of recipe box objects
columns_divs = []
for i in range(0, len(recipe_boxes), 3):
    recipebox_links = []
    recipebox_links.append(recipe_boxes[i])
    if i + 1 < len(recipe_boxes):
        recipebox_links.append(recipe_boxes[i + 1])
    if i + 2 < len(recipe_boxes):
        recipebox_links.append(recipe_boxes[i + 2])
    columns_divs.append(Templates.RecipeBoxColumnsDiv(recipebox_divs=recipebox_links))
# build clickable buttons from list of tags
tag_buttons = []
for tag in index["Tags"]:
    tag_buttons.append(Templates.TagFilterButton(tag))
# finally, build index
index = Templates.Index(
    recipebox_column_divs=columns_divs, tag_filter_buttons=tag_buttons
)
soup = bs4.BeautifulSoup(index.render(), "html.parser")
with open("site/index.html", "w") as outfile:
    outfile.write(soup.prettify())
    print(f"Successfully generated index.html from recipes")

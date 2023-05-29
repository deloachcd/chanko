import bs4
import orgparse

# NOTE loop through relevant tags
#for tag in filter(lambda x: type(x) is bs4.element.Tag, soup.children)
# 1. expect image -> drill down into tags to get image
# 2. expect h1 and then non-heading tags -> RecipeNameSection 
# 3. expect sets of h2 and then non-heading tags -> RecipeDetailSection

# NOTE implement org parser
# root = orgparse.load("recipes/recipe.org")
# level0_rawbody = root.get_body(format="raw")
# img_path = re.search("\[\[.*\]\]", level0_rawbody).group()[2:-2]
# level1 = root.children[0]
# recipe_name = level1.get_heading()
# level1.properties ->
# {'PrepTime': '30 minutes', 'CookTime': '35 minutes', 'Tags': 'american,comfort_food'}
# recipe_props = level1.properties
# recipe_props['Tags'] = recipe_props['Tags'].replace(" ","").split(",") # NOTE modify tags str -> list
# for level2 in level1.children:
#   section_header = level2.get_heading()
#   NOTE process as unordered list
#   if re.search("^\-\s", level2.get_body()):
#     steps_raw = re.split("\-\s", level2.get_body())[1:]
#   elif re.search("^\d*\.\s", level2.get_body()):
#     steps_raw = re.split("\d*\.\s", level2.get_body())[1:]
#   NOTE process as paragraph
#   else:
#     steps_raw = level2.get_body.replace("\n", "")

import bs4

# NOTE loop through relevant tags
#for tag in filter(lambda x: type(x) is bs4.element.Tag, soup.children)
# 1. expect image -> drill down into tags to get image
# 2. expect h1 and then non-heading tags -> RecipeNameSection 
# 3. expect sets of h2 and then non-heading tags -> RecipeDetailSection

# TODO implement

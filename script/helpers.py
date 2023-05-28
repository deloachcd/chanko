from dataclasses import dataclass
from pathlib import Path

import bs4

from FileTemplateHTML import FileTemplateHTML

@dataclass
class RecipeBox(FileTemplateHTML):
    img_path: str
    recipe_name: str
    prep_time: str
    cook_time: str
    html_template: str = Path("templates/RecipeBox.html").read_text()

if __name__ == "__main__":
    recipe_box = RecipeBox("./sample/img.png", "Buffalo Wings", "30 min", "30 min")
    target = f"<body>{recipe_box.render()}</body>"
    soup = bs4.BeautifulSoup(target, "html.parser")
    print(soup.prettify())

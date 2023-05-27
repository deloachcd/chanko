from pathlib import Path

from attrs import define
import bs4 

@define
class RecipeBox:
    img_path: str = ""
    recipe_name: str = ""
    prep_time: str = ""
    cook_time: str = ""
    html_template: str = Path("templates/RecipeBox.html").read_text()

    def render(self):
        # evil f-string hacking with eval()
        return eval(f'f"""{self.html_template}"""')

if __name__ == "__main__":
    recipe_box = RecipeBox("./sample/img.png", "Buffalo Wings", "30 min", "30 min")
    target = f"<body>{recipe_box.render()}</body>"
    soup = bs4.BeautifulSoup(target, "html.parser")
    print(soup.prettify())

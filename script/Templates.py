import bs4

from dataclasses import dataclass
from pathlib import Path


class FileTemplateHTML:
    def render(self):
        # evil f-string hacking with eval() to populate f-string
        # template from class attributes
        return eval(f'f"""{self.html_template}"""')


@dataclass
class RecipeBoxTags(FileTemplateHTML):
    taglist: list
    html_template: str = Path("templates/RecipeBoxTags.html").read_text()

    def render(self):
        self._tags_html = ""
        for tag in self.taglist:
            tag_html = f'<span class="tag">{tag}</span>'
            self._tags_html += tag_html
        return super().render()


@dataclass
class RecipeBox(FileTemplateHTML):
    img_path: str
    recipe_name: str
    prep_time: str
    cook_time: str
    tags: RecipeBoxTags
    html_template: str = Path("templates/RecipeBox.html").read_text()


@dataclass
class RecipeBoxSmall(FileTemplateHTML):
    img_path: str
    recipe_name: str
    prep_time: str
    cook_time: str
    tags: RecipeBoxTags
    html_template: str = Path("templates/RecipeBox.html").read_text()


if __name__ == "__main__":
    # Use this block to run some basic sanity checks
    soup = bs4.BeautifulSoup(
        RecipeBoxSmall(
            "path/to/img.jpg",
            "Buffalo Buttz",
            "10 hours",
            "1 minute",
            RecipeBoxTags(["horrifying", "do_not_eat"]),
        ).render(),
        "html.parser",
    )
    print(soup.prettify())

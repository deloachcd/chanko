import bs4

from dataclasses import dataclass
from pathlib import Path
import html


class TemplateHelpers:
    @staticmethod
    def render_all(collection):
        return "".join([item.render() for item in collection])


class FileTemplateHTML:
    def render(self):
        # evil f-string hacking with eval() to populate f-string
        # template from class attributes
        return eval(f'f"""{self.html_template}"""')


@dataclass
class RecipeBoxTag(FileTemplateHTML):
    tagname: str
    html_template: str = Path("templates/RecipeBoxTag.html").read_text()


@dataclass
class RecipeBox(FileTemplateHTML):
    img_path: str
    recipe_name: str
    prep_time: str
    cook_time: str
    tags: list
    html_template: str = Path("templates/RecipeBox.html").read_text()


@dataclass
class RecipeBoxSmall(FileTemplateHTML):
    img_path: str
    recipe_name: str
    prep_time: str
    cook_time: str
    tags: list
    html_template: str = Path("templates/RecipeBox.html").read_text()


@dataclass
class RecipeDetailSection(FileTemplateHTML):
    content: dict
    html_template: str = Path("templates/RecipeDetailSection.html").read_text()

    def render(self):
        def build_section(entry, depth):
            header = (
                f'<h{depth} class="title is-{depth*2}">{entry["Header"]}</h{depth}>'
            )
            if entry["Format"] == "Paragraph":
                body = f'<p>{entry["Body"]}</p>'
            elif entry["Format"] == "OrderedList":
                body = (
                    "<ol>"
                    + "".join([f"<li>{html.escape(li)}</li>" for li in entry["Body"]])
                    + "</ol>"
                )
            elif entry["Format"] == "UnorderedList":
                body = (
                    "<ul>"
                    + "".join([f"<li>{html.escape(li)}</li>" for li in entry["Body"]])
                    + "</ul>"
                )

            rval = f"{header}\n{body}\n"
            if "children" in entry.keys():
                for child in entry["children"]:
                    rval += build_section(child, depth + 1)

            return rval

        self._body = build_section(self.content, 2)
        return super().render()


@dataclass
class RecipeInstructionsPage(FileTemplateHTML):
    recipe_box: RecipeBox
    detail_sections: list
    html_template: str = Path("templates/RecipeInstructionsPage.html").read_text()


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

# NOTE this class never gets used directly - it just provides the render()
# method for the subclasses which inherit it, all of which should be simple
# dataclasses which specify mandatory arguments for attributes referenced
# in the file template, and a default argument for html_template that loads
# the content of that file
#
# just take a look at any of the subclasses and you'll get it
class FileTemplateHTML:
    def render(self):
        # evil f-string hacking with eval() to populate f-string
        # template from class attributes
        return eval(f'f"""{self.html_template}"""')

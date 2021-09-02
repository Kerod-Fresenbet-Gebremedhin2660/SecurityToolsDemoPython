from dominate import tags
from flask_nav.renderers import Renderer


class JustDivRenderer(Renderer):
    def visit_Navbar(self, node):
        sub = []
        for item in node.items:
            sub.append(self.visit(item))

        return tags.div('Navigation:', *sub)
    @staticmethod
    def visit_View(self, node):
        return tags.div('{} ({})'.format(node.title, node.get_url()))
    
    def visit_Subgroup(self, node):
        return tags.div(node.title,
                        *[self.visit(item) for item in node.items])
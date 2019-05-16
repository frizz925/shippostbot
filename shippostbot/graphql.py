class Schema(object):
    def __init__(self,
                 name: str,
                 alias=None):
        self.name = name
        self.alias = alias

    def render_indent(self, level) -> str:
        return ''.join('  ' for x in range(level))

class Field(Schema):
    def pre_render(self, level=0) -> str:
        result = self.render_indent(level)
        if self.alias:
            result += '%s: ' % self.alias
        return result

    def render(self, level=0) -> str:
        result = self.pre_render(level)
        result += self.name
        return result

    def __str__(self):
        return self.render()

class Fields(Field):
    def __init__(self,
                 name: str,
                 children=[],
                 alias=None):
        Field.__init__(self, name, alias)
        self.children = []
        if isinstance(children, list):
            for child in children:
                self.add(child)
        else:
            self.add(children)
    
    def add(self, field: Field):
        if isinstance(field, str):
            field = Field(field)
        self.children.append(field)

    def render(self, level=0) -> str:
        result = self.pre_render(level)
        if self.name is not None:
            result += '%s ' % self.name
        result += '{\n%s\n%s}' % (self.render_children(level), self.render_indent(level))
        return result

    def render_children(self, level) -> str:
        return '\n'.join(c.render(level + 1) for c in self.children)

class Query(Fields):
    def __init__(self,
                 name: str,
                 params: dict,
                 children=[],
                 alias=None):
        Fields.__init__(self, name, children, alias)
        self.params = params

    def render(self, level=0) -> str:
        result = self.pre_render(level)
        result += '%s(%s)' % (self.name, self.render_params())
        result += ' {\n%s\n%s}' % (self.render_children(level), self.render_indent(level))
        return result

    def render_params(self) -> str:
        return ', '.join(self.render_param(k, v) for k, v in self.params.items())

    def render_param(self, key: str, value: str) -> str:
        return '%s: %s' % (key, value)

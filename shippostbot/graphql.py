from typing import List


class Schema(object):
    def pre_render(self, level=0) -> str:
        return self.render_indent(level)

    def render(self, level=0) -> str:
        return self.render_indent(level)

    def render_indent(self, level=0) -> str:
        return ''.join('  ' for x in range(level))

    def __str__(self):
        return self.render()


class Root(Schema):
    def __init__(self, children=[]):
        self.children = normalize_children(children)

    def add(self, schema):
        attach_schema(self.children, schema)

    def render(self, level=0) -> str:
        return self.pre_render(level) + self.render_block(level)

    def render_block(self, level=0) -> str:
        return '{\n%s\n%s}' % (self.render_children(level), self.render_indent(level))

    def render_children(self, level=0) -> str:
        return '\n'.join(c.render(level + 1) for c in self.children)


class Field(Schema):
    def __init__(self, name: str, alias=None):
        self.name = name
        self.alias = alias

    def render(self, level=0) -> str:
        return self.pre_render(level) + self.render_name(level)

    def render_name(self, level=0) -> str:
        if self.alias is None:
            return self.name
        else:
            return '%s: %s' % (self.alias, self.name)


class Fields(Root):
    def __init__(self,
                 name: str,
                 children=[],
                 alias=None):
        Root.__init__(self, children)
        self.name = name
        self.alias = alias

    def render(self, level=0) -> str:
        return self.pre_render(level) + self.render_name(level) + self.render_block(level)

    def render_name(self, level=0) -> str:
        if self.alias is None:
            return '%s ' % self.name
        else:
            return '%s: %s ' % (self.alias, self.name)


class Query(Fields):
    def __init__(self,
                 name: str,
                 params: dict,
                 children=[],
                 alias=None):
        Fields.__init__(self, name, children, alias)
        self.params = params

    def render_name(self, level=0) -> str:
        result = '%s(%s) ' % (self.name, self.render_params())
        if self.alias is not None:
            result = '%s: %s' % (self.alias, result)
        return result

    def render_params(self) -> str:
        return ', '.join(self.render_param(k, v) for k, v in self.params.items())

    def render_param(self, key: str, value: str) -> str:
        return '%s: %s' % (key, value)


def normalize_children(children: any) -> List[Schema]:
    result = []
    if isinstance(children, list):
        for child in children:
            attach_schema(result, child)
    else:
        attach_schema(result, children)
    return result


def attach_schema(children: List[Schema], schema: any):
    if isinstance(schema, str):
        schema = Field(schema)
    children.append(schema)

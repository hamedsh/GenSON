import warnings
from . import base


class TestType(base.SchemaTestCase):

    def test_single_type(self):
        schema = {'type': 'string'}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_single_type_unicode(self):
        schema = {u'type': u'string'}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_no_type(self):
        schema = {}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.add_schema(schema)
        self.assertResult(schema)

    def test_array_type_no_items(self):
        schema = {'type': 'array'}
        self.add_schema(schema)
        self.assertResult(schema)


class TestAnyOf(base.SchemaTestCase):

    def test_multi_type(self):
        schema = {'type': ['boolean', 'null', 'number', 'string']}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_multi_type_with_extra_keywords(self):
        schema = {'type': ['boolean', 'null', 'number', 'string'],
                  'title': 'this will be duplicated'}
        self.add_schema(schema)
        self.assertResult({'anyOf': [
            {'type': 'boolean', 'title': 'this will be duplicated'},
            {'type': 'null', 'title': 'this will be duplicated'},
            {'type': 'number', 'title': 'this will be duplicated'},
            {'type': 'string', 'title': 'this will be duplicated'}
        ]})

    def test_anyof(self):
        schema = {"anyOf": [
            {"type": "null"},
            {"type": "boolean", "title": "Gruyere"}
        ]}
        self.add_schema(schema)
        self.assertResult(schema)


class TestPreserveExtraKeywords(base.SchemaTestCase):

    def test_basic_type(self):
        schema = {'type': 'boolean', 'const': False, 'myKeyword': True}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_number(self):
        schema = {'type': 'number', 'const': 5, 'myKeyword': True}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_list(self):
        schema = {'type': 'array', 'items': {"type": "null"},
                  'const': [], 'myKeyword': True}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_tuple(self):
        schema = {'type': 'array', 'items': [{"type": "null"}],
                  'const': [], 'myKeyword': True}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_object(self):
        schema = {'type': 'object', 'properties': {},
                  'const': {}, 'myKeyword': True}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_no_type(self):
        schema = {'const': 5, 'myKeyword': True}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.add_schema(schema)
        self.assertResult(schema)


class TestSeedSchema(base.SchemaTestCase):

    def test_seed_tuple(self):
        self.add_schema({'type': 'array', 'items': []})
        self.add_object([None])
        self.assertResult({'type': 'array', 'items': [{'type': 'null'}]})

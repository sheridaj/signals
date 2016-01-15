import os
import shutil
from signals.logging import SignalsError


class BaseGenerator(object):
    BUILD_DIR = "signals_code"
    RESERVED_WORDS = []

    def __init__(self, schema):
        self.schema = schema

    # Check data model schema for reserved words in the language of the generated template.
    def check_reserved_words(self):
        for name, data_object in self.schema.data_objects.iteritems():
            for field in data_object.fields:
                if field.name in self.RESERVED_WORDS:
                    raise SignalsError(str.format("Cannot use reserved word '{0}' for object parameter",field.name))

    def process(self):
        pass

    @classmethod
    def clear_generated_code_files(cls):
        if os.path.isdir(cls.BUILD_DIR):
            shutil.rmtree(cls.BUILD_DIR)
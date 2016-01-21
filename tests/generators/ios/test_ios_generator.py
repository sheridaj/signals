import mock
import unittest
from signals.generators.ios.ios_generator import iOSGenerator, ObjectiveCGenerator
from signals.logging import SignalsError
from signals.parser.schema import Schema
from tests.utils import create_dynamic_schema

def good_app_delegate(var1, var2):
    return "./tests/files", "AppDelegate.swift"


def bad_app_delegate(var1, var2):
    return "./tests/files", "BadAppDelegate.swift"


class iOSGeneratorTestCase(unittest.TestCase):
    @mock.patch("signals.generators.ios.ios_generator.subprocess")
    def test_is_xcode_running(self, mock_subprocess):
        mock_subprocess.check_output.return_value = "Xcode.app"
        self.assertTrue(iOSGenerator.is_xcode_running())
        mock_subprocess.check_output.return_value = ""
        self.assertFalse(iOSGenerator.is_xcode_running())

    @mock.patch("signals.generators.ios.ios_generator.subprocess")
    def test_process_error(self, mock_subprocess):
        mock_subprocess.check_output.return_value = "Xcode.app"
        generator = ObjectiveCGenerator("objc",
                                        Schema("./tests/files/test_schema.json"),
                                        "./tests/files/",
                                        "./core/data/path",
                                        True,
                                        "YetiProject")
        with self.assertRaises(SignalsError) as e:
            generator.process()
        self.assertEqual(e.exception.msg, "Must quit Xcode before writing to core data")

    @mock.patch("signals.generators.ios.ios_generator.recursively_find_parent_containing_file", side_effect=good_app_delegate)
    def test_check_setup_called_success(self, mock_function):
        generator = ObjectiveCGenerator("objc",
                                        Schema("./tests/files/test_schema.json"),
                                        "./tests/files/",
                                        "./core/data/path",
                                        True,
                                        "YetiProject")
        self.assertTrue(generator.check_setup_called())

    @mock.patch("signals.generators.ios.ios_generator.recursively_find_parent_containing_file", side_effect=bad_app_delegate)
    def test_check_setup_called_failure(self, mock_function):
        generator = ObjectiveCGenerator("objc",
                                        Schema("./tests/files/test_schema.json"),
                                        "./tests/files/",
                                        "./core/data/path",
                                        False,
                                        "YetiProject")
        self.assertFalse(generator.check_setup_called())
        
    
    def test_check_reserved_words(self):
    	objects_json = {
            '$postRequest': {"int": "string", "title": "string"},
            '$postResponse': {"body": "string", "title": "string"}
        }
        urls_json = [
            {
                "url": "post/:id/favorites/",
                "patch": {
                    "request": "$postRequest",
                    "response": {
                        "200+": "$postResponse"
                    }
                }
            }
        ]
        schema = create_dynamic_schema(objects_json, urls_json)
    	generator = ObjectiveCGenerator("objc",
                                        schema,
                                        "./tests/files/",
                                        "./core/data/path",
                                        False,
                                        "YetiProject")
        with self.assertRaises(SignalsError) as e:
            generator.check_reserved_words()
		self.assertEqual(e.exception.msg, "Cannot use reserved word 'int' for object parameter")


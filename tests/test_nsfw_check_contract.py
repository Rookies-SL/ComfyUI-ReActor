import ast
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NODES_PATH = REPO_ROOT / "nodes.py"
NODES_SOURCE = NODES_PATH.read_text(encoding="utf-8")
NODES_TREE = ast.parse(NODES_SOURCE)


def get_class(name):
    for node in NODES_TREE.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    raise AssertionError(f"Class {name} not found")


def get_method(class_node, name):
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"Method {class_node.name}.{name} not found")


def get_returned_dict(function_node):
    for node in ast.walk(function_node):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict):
            return node.value
    raise AssertionError(f"No returned dict found in {function_node.name}")


def dict_value(dict_node, key):
    for key_node, value_node in zip(dict_node.keys, dict_node.values):
        if isinstance(key_node, ast.Constant) and key_node.value == key:
            return value_node
    raise AssertionError(f"Key {key!r} not found")


def dict_has_key(dict_node, key):
    return any(
        isinstance(key_node, ast.Constant) and key_node.value == key
        for key_node in dict_node.keys
    )


def boolean_default(tuple_node):
    if not isinstance(tuple_node, ast.Tuple) or len(tuple_node.elts) < 2:
        raise AssertionError("Expected ComfyUI input tuple")
    options = tuple_node.elts[1]
    if not isinstance(options, ast.Dict):
        raise AssertionError("Expected ComfyUI input options dict")
    default_node = dict_value(options, "default")
    if not isinstance(default_node, ast.Constant):
        raise AssertionError("Expected constant default")
    return default_node.value


class NsfwCheckContractTest(unittest.TestCase):
    def test_main_face_swap_node_exposes_nsfw_check_default_on(self):
        reactor_class = get_class("reactor")
        input_types = get_method(reactor_class, "INPUT_TYPES")
        returned = get_returned_dict(input_types)
        required = dict_value(returned, "required")

        self.assertTrue(dict_has_key(required, "nsfw_check"))
        self.assertIs(boolean_default(dict_value(required, "nsfw_check")), True)

    def test_options_node_exposes_nsfw_check_default_on(self):
        options_class = get_class("ReActorOptions")
        input_types = get_method(options_class, "INPUT_TYPES")
        returned = get_returned_dict(input_types)
        required = dict_value(returned, "required")

        self.assertTrue(dict_has_key(required, "nsfw_check"))
        self.assertIs(boolean_default(dict_value(required, "nsfw_check")), True)

    def test_nsfw_check_flows_through_options_node(self):
        reactor_execute = get_method(get_class("reactor"), "execute")
        reactor_args = [arg.arg for arg in reactor_execute.args.args]
        self.assertIn("nsfw_check", reactor_args)

        options_execute = get_method(get_class("ReActorOptions"), "execute")
        options_args = [arg.arg for arg in options_execute.args.args]
        self.assertIn("nsfw_check", options_args)

        options_source = ast.get_source_segment(NODES_SOURCE, options_execute)
        self.assertIn('"nsfw_check": nsfw_check', options_source)

        plus_execute = get_method(get_class("ReActorPlusOpt"), "execute")
        plus_source = ast.get_source_segment(NODES_SOURCE, plus_execute)
        self.assertIn('options["nsfw_check"]', plus_source)
        self.assertIn("self.nsfw_check", plus_source)

import builtins
import runpy
from pathlib import Path

import pytest

import generator


@pytest.fixture
def config(tmp_path):
    return generator.GeneratorConfig(
        project_name="test_project",
        output_directory=tmp_path,
        file_count=2,
        functions_per_file=2,
        classes_per_file=1,
        methods_per_class=2,
        file_prefix="module",
        function_prefix="test_function",
        class_prefix="TestClass",
        method_prefix="test_method",
        include_imports=True,
        include_docstrings=True,
        include_type_hints=True,
        include_main=True,
        include_init=True,
        custom_imports=list(generator.DEFAULT_IMPORTS),
        randomize_logic=True,
        random_seed=123,
    )


def feed_inputs(monkeypatch, values):
    iterator = iter(values)
    monkeypatch.setattr(builtins, "input", lambda _prompt="": next(iterator))


def test_ask_string_default_and_custom(monkeypatch):
    feed_inputs(monkeypatch, ["", "custom"])
    assert generator.ask_string("Name", "default") == "default"
    assert generator.ask_string("Name", "default") == "custom"


def test_ask_int_default_invalid_below_minimum_and_valid(monkeypatch, capsys):
    feed_inputs(monkeypatch, ["", "bad", "0", "4"])
    assert generator.ask_int("Count", 3, minimum=1) == 3
    assert generator.ask_int("Count", 3, minimum=1) == 4
    output = capsys.readouterr().out
    assert "Please enter a valid integer." in output
    assert "Value must be at least 1." in output


def test_ask_bool_all_paths(monkeypatch, capsys):
    feed_inputs(monkeypatch, ["", "", "maybe", "yes", "no"])
    assert generator.ask_bool("Enabled", True) is True
    assert generator.ask_bool("Enabled", False) is False
    assert generator.ask_bool("Enabled", False) is True
    assert generator.ask_bool("Enabled", True) is False
    assert "Please enter yes or no." in capsys.readouterr().out


@pytest.mark.parametrize(
    ("raw", "fallback", "expected"),
    [
        ("hello world", "fallback", "hello_world"),
        ("123name", "fallback", "_123name"),
        ("", "fallback", "fallback"),
        ("already_valid", "fallback", "already_valid"),
    ],
)
def test_sanitize_identifier(raw, fallback, expected):
    assert generator.sanitize_identifier(raw, fallback) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("my project", "my_project"),
        ("valid-name", "valid-name"),
        ("", "module"),
        ("weird/name.py", "weird_name_py"),
    ],
)
def test_sanitize_filename(raw, expected):
    assert generator.sanitize_filename(raw) == expected


def test_collect_custom_imports(monkeypatch, capsys):
    feed_inputs(monkeypatch, ["import os", "from sys import path", ""])
    assert generator.collect_custom_imports() == ["import os", "from sys import path"]
    assert "Custom imports" in capsys.readouterr().out


def test_collect_configuration_defaults(monkeypatch):
    # 10 strings/ints + 6 booleans + random seed + 2 import booleans
    feed_inputs(monkeypatch, [""] * 19)
    result = generator.collect_configuration()
    assert result.project_name == generator.DEFAULT_PROJECT_NAME
    assert result.output_directory == Path("./output")
    assert result.file_count == generator.DEFAULT_FILE_COUNT
    assert result.functions_per_file == generator.DEFAULT_FUNCTION_COUNT
    assert result.classes_per_file == generator.DEFAULT_CLASS_COUNT
    assert result.methods_per_class == generator.DEFAULT_METHOD_COUNT
    assert result.file_prefix == "module"
    assert result.function_prefix == generator.DEFAULT_FUNCTION_PREFIX
    assert result.class_prefix == generator.DEFAULT_CLASS_PREFIX
    assert result.method_prefix == generator.DEFAULT_METHOD_PREFIX
    assert result.include_imports is True
    assert result.include_docstrings is True
    assert result.include_type_hints is True
    assert result.include_init is True
    assert result.include_main is True
    assert result.randomize_logic is True
    assert result.random_seed is None
    assert result.custom_imports == generator.DEFAULT_IMPORTS


def test_collect_configuration_custom_with_imports(monkeypatch):
    feed_inputs(
        monkeypatch,
        [
            "custom_project", "/tmp/generated", "4", "5", "6", "7",
            "file", "fn", "Cls", "method",
            "yes", "no", "no", "no", "no", "no",
            "42",
            "no", "yes",
            "import json", "from math import sqrt", "",
        ],
    )
    result = generator.collect_configuration()
    assert result.project_name == "custom_project"
    assert result.output_directory == Path("/tmp/generated")
    assert result.file_count == 4
    assert result.functions_per_file == 5
    assert result.classes_per_file == 6
    assert result.methods_per_class == 7
    assert result.file_prefix == "file"
    assert result.function_prefix == "fn"
    assert result.class_prefix == "Cls"
    assert result.method_prefix == "method"
    assert result.include_imports is True
    assert result.include_docstrings is False
    assert result.include_type_hints is False
    assert result.include_init is False
    assert result.include_main is False
    assert result.randomize_logic is False
    assert result.random_seed == 42
    assert result.custom_imports == ["import json", "from math import sqrt"]


def test_collect_configuration_imports_disabled_and_invalid_seed(monkeypatch, capsys):
    feed_inputs(
        monkeypatch,
        [
            "", "", "", "", "", "", "", "", "", "",
            "no", "", "", "", "", "", "not-an-int",
        ],
    )
    result = generator.collect_configuration()
    assert result.include_imports is False
    assert result.custom_imports == []
    assert result.random_seed is None
    assert "Invalid random seed. Using random behavior." in capsys.readouterr().out


def test_generate_function_typed_docstring_randomized(config, monkeypatch):
    monkeypatch.setattr(generator.random, "choice", lambda seq: seq[5])
    source = generator.generate_function("123 bad name", config)
    assert "def _123_bad_name(values: list[float]) -> object:" in source
    assert '"""Automatically generated function: _123_bad_name."""' in source
    assert "        return None" in source
    compile(source, "<function>", "exec")


def test_generate_function_untyped_no_docstring_not_randomized(config):
    config.include_type_hints = False
    config.include_docstrings = False
    config.randomize_logic = False
    source = generator.generate_function("", config)
    assert f"def {generator.DEFAULT_FUNCTION_PREFIX}(values):" in source
    assert "Automatically generated" not in source
    assert "return sum(values)" in source
    compile(source, "<function>", "exec")


def test_generate_method_typed_and_untyped(config, monkeypatch):
    monkeypatch.setattr(generator.random, "choice", lambda seq: seq[0])
    typed = generator.generate_method("method", config)
    assert "def method(self) -> object:" in typed
    assert "Automatically generated method" in typed

    config.include_type_hints = False
    config.include_docstrings = False
    untyped = generator.generate_method("", config)
    assert f"def {generator.DEFAULT_METHOD_PREFIX}(self):" in untyped
    assert "Automatically generated" not in untyped


def test_generate_class_typed_and_untyped(config):
    typed = generator.generate_class("Example", 1, 1, config)
    assert "class Example:" in typed
    assert "def __init__(self, values: list[float]) -> None:" in typed
    compile(typed, "<class>", "exec")

    config.include_type_hints = False
    config.include_docstrings = False
    untyped = generator.generate_class("", 0, 1, config)
    assert f"class {generator.DEFAULT_CLASS_PREFIX}:" in untyped
    assert "def __init__(self, values):" in untyped
    compile(untyped, "<class>", "exec")


def test_generate_module_with_and_without_imports(config):
    with_imports = generator.generate_module(1, config)
    assert "from pathlib import Path" in with_imports
    assert "def test_function_1_1" in with_imports
    assert "class TestClass1_1" in with_imports
    compile(with_imports, "<module>", "exec")

    config.include_imports = False
    without_imports = generator.generate_module(2, config)
    assert "from pathlib import Path" not in without_imports
    compile(without_imports, "<module>", "exec")


def test_generate_module_imports_enabled_but_empty(config):
    config.custom_imports = []
    source = generator.generate_module(1, config)
    assert "from pathlib import Path" not in source


def test_generate_main_file_all_paths(config):
    with_module = generator.generate_main_file(["module_1"], config)
    assert '"""Automatically generated application entry point."""' in with_module
    assert "import module_1" in with_module
    assert 'if __name__ == "__main__":' in with_module

    config.include_docstrings = False
    without_module = generator.generate_main_file([], config)
    assert "Automatically generated application" not in without_module
    assert "import module_1" not in without_module
    compile(without_module, "<main>", "exec")


def test_generate_project_full(config):
    project_dir = generator.generate_project(config)
    expected = {"module_1.py", "module_2.py", "__init__.py", "main.py"}
    assert {p.name for p in project_dir.iterdir()} == expected
    for python_file in project_dir.glob("*.py"):
        compile(python_file.read_text(), str(python_file), "exec")


def test_generate_project_without_optional_files_and_seed_none(config):
    config.project_name = "project with spaces"
    config.include_init = False
    config.include_main = False
    config.random_seed = None
    project_dir = generator.generate_project(config)
    assert project_dir.name == "project_with_spaces"
    assert not (project_dir / "__init__.py").exists()
    assert not (project_dir / "main.py").exists()


def test_generation_is_deterministic_with_seed(tmp_path):
    common = dict(
        output_directory=tmp_path,
        file_count=1,
        functions_per_file=4,
        classes_per_file=0,
        methods_per_class=0,
        file_prefix="module",
        function_prefix="func",
        class_prefix="Class",
        method_prefix="method",
        include_imports=False,
        include_docstrings=True,
        include_type_hints=True,
        include_main=False,
        include_init=False,
        custom_imports=[],
        randomize_logic=True,
        random_seed=999,
    )
    first = generator.generate_project(generator.GeneratorConfig(project_name="one", **common))
    second = generator.generate_project(generator.GeneratorConfig(project_name="two", **common))
    assert (first / "module_1.py").read_text() == (second / "module_1.py").read_text()


def test_print_summary(config, tmp_path, capsys):
    generator.print_summary(config, tmp_path / "project")
    output = capsys.readouterr().out
    assert "GENERATION COMPLETE" in output
    assert "test_project" in output
    assert "Generated modules:" in output
    assert "Generated functions:" in output
    assert "Generated classes:" in output
    assert "Generated methods:" in output
    assert "123" in output


def test_main_orchestrates(monkeypatch, config, tmp_path):
    generated = tmp_path / "made"
    calls = []
    monkeypatch.setattr(generator, "collect_configuration", lambda: config)
    monkeypatch.setattr(generator, "generate_project", lambda cfg: calls.append(("generate", cfg)) or generated)
    monkeypatch.setattr(generator, "print_summary", lambda cfg, path: calls.append(("summary", cfg, path)))
    generator.main()
    assert calls == [("generate", config), ("summary", config, generated)]


def test_module_executes_as_script(monkeypatch, tmp_path):
    # Exercise the `if __name__ == "__main__"` statement using default CLI answers.
    monkeypatch.chdir(tmp_path)
    feed_inputs(monkeypatch, [""] * 19)
    runpy.run_path(str(Path(generator.__file__)), run_name="__main__")
    assert (tmp_path / "output" / generator.DEFAULT_PROJECT_NAME / "main.py").exists()

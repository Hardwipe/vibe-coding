from pathlib import Path
import py_compile

import pytest

import generator


@pytest.fixture
def basic_config(tmp_path):
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
        custom_imports=[
            "from pathlib import Path",
            "from typing import Any",
        ],
        randomize_logic=True,
        random_seed=123,
    )


def test_sanitize_identifier():
    assert generator.sanitize_identifier("hello world", "fallback") == "hello_world"
    assert generator.sanitize_identifier("123name", "fallback") == "_123name"
    assert generator.sanitize_identifier("", "fallback") == "fallback"


def test_sanitize_filename():
    assert generator.sanitize_filename("my project") == "my_project"
    assert generator.sanitize_filename("valid-name") == "valid-name"
    assert generator.sanitize_filename("") == "module"


def test_generate_function_has_valid_indentation(basic_config):
    source = generator.generate_function("example", basic_config)

    compile(source, "<generated_function>", "exec")


def test_generate_function_contains_expected_name(basic_config):
    source = generator.generate_function("example", basic_config)

    assert "def example(" in source
    assert "Automatically generated function: example." in source


def test_generate_class_is_valid_python(basic_config):
    source = generator.generate_class(
        name="ExampleClass",
        method_count=2,
        class_index=1,
        config=basic_config,
    )

    compile(source, "<generated_class>", "exec")


def test_generate_module_is_valid_python(basic_config):
    source = generator.generate_module(
        module_index=1,
        config=basic_config,
    )

    compile(source, "<generated_module>", "exec")


def test_generate_project_creates_expected_files(basic_config):
    project_dir = generator.generate_project(basic_config)

    assert project_dir.exists()
    assert (project_dir / "__init__.py").exists()
    assert (project_dir / "main.py").exists()
    assert (project_dir / "module_1.py").exists()
    assert (project_dir / "module_2.py").exists()


def test_every_generated_python_file_compiles(basic_config):
    project_dir = generator.generate_project(basic_config)

    python_files = list(project_dir.glob("*.py"))

    assert python_files

    for python_file in python_files:
        py_compile.compile(
            str(python_file),
            doraise=True,
        )


def test_expected_number_of_functions_and_classes(basic_config):
    source = generator.generate_module(
        module_index=1,
        config=basic_config,
    )

    assert source.count("def test_function_1_") == 2
    assert source.count("class TestClass1_") == 1

    # __init__ + configured methods
    assert source.count("    def ") == 3


def test_generation_is_deterministic_with_seed(tmp_path):
    config_one = generator.GeneratorConfig(
        project_name="project_one",
        output_directory=tmp_path,
        file_count=1,
        functions_per_file=5,
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

    config_two = generator.GeneratorConfig(
        **{
            **config_one.__dict__,
            "project_name": "project_two",
        }
    )

    project_one = generator.generate_project(config_one)
    project_two = generator.generate_project(config_two)

    source_one = (project_one / "module_1.py").read_text()
    source_two = (project_two / "module_1.py").read_text()

    assert source_one == source_two


def test_project_runs_main_file(basic_config, monkeypatch):
    project_dir = generator.generate_project(basic_config)

    main_source = (project_dir / "main.py").read_text()

    compile(main_source, str(project_dir / "main.py"), "exec")

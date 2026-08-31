from __future__ import annotations

import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


DEFAULT_PROJECT_NAME = "generated_project"
DEFAULT_FILE_COUNT = 3
DEFAULT_FUNCTION_COUNT = 3
DEFAULT_CLASS_COUNT = 2
DEFAULT_METHOD_COUNT = 3

DEFAULT_IMPORTS = [
    "from pathlib import Path",
    "from typing import Any",
]

DEFAULT_FUNCTION_PREFIX = "generated_function"
DEFAULT_CLASS_PREFIX = "GeneratedClass"
DEFAULT_METHOD_PREFIX = "generated_method"


@dataclass
class GeneratorConfig:
    project_name: str
    output_directory: Path

    file_count: int
    functions_per_file: int
    classes_per_file: int
    methods_per_class: int

    file_prefix: str
    function_prefix: str
    class_prefix: str
    method_prefix: str

    include_imports: bool
    include_docstrings: bool
    include_type_hints: bool
    include_main: bool
    include_init: bool

    custom_imports: list[str]

    randomize_logic: bool
    random_seed: Optional[int]


def ask_string(prompt: str, default: str) -> str:
    value = input(f"{prompt} [{default}]: ").strip()

    if not value:
        return default

    return value


def ask_int(prompt: str, default: int, minimum: int = 0) -> int:
    while True:
        value = input(f"{prompt} [{default}]: ").strip()

        if not value:
            return default

        try:
            number = int(value)

            if number < minimum:
                print(f"Value must be at least {minimum}.")
                continue

            return number

        except ValueError:
            print("Please enter a valid integer.")


def ask_bool(prompt: str, default: bool = True) -> bool:
    default_display = "Y/n" if default else "y/N"

    while True:
        value = input(f"{prompt} [{default_display}]: ").strip().lower()

        if not value:
            return default

        if value in {"y", "yes", "true", "1"}:
            return True

        if value in {"n", "no", "false", "0"}:
            return False

        print("Please enter yes or no.")


def sanitize_identifier(value: str, fallback: str) -> str:
    value = re.sub(r"\W+", "_", value)

    if not value:
        return fallback

    if value[0].isdigit():
        value = f"_{value}"

    return value


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_\-]", "_", value)

    return value or "module"


def collect_custom_imports() -> list[str]:
    imports = []

    print("\nCustom imports")
    print("Enter one import per line.")
    print("Press Enter on an empty line when finished.\n")

    while True:
        value = input("Import: ").strip()

        if not value:
            break

        imports.append(value)

    return imports


def collect_configuration() -> GeneratorConfig:
    print("=" * 60)
    print("PYTHON SYNTHETIC PROJECT GENERATOR")
    print("=" * 60)

    print("\nPress Enter to accept any default.\n")

    project_name = ask_string(
        "Project name",
        DEFAULT_PROJECT_NAME,
    )

    output_directory_string = ask_string(
        "Output directory",
        "./output",
    )

    file_count = ask_int(
        "Number of Python files",
        DEFAULT_FILE_COUNT,
        minimum=1,
    )

    functions_per_file = ask_int(
        "Functions per file",
        DEFAULT_FUNCTION_COUNT,
    )

    classes_per_file = ask_int(
        "Classes per file",
        DEFAULT_CLASS_COUNT,
    )

    methods_per_class = ask_int(
        "Methods per class",
        DEFAULT_METHOD_COUNT,
    )

    file_prefix = ask_string(
        "Generated file prefix",
        "module",
    )

    function_prefix = ask_string(
        "Function name prefix",
        DEFAULT_FUNCTION_PREFIX,
    )

    class_prefix = ask_string(
        "Class name prefix",
        DEFAULT_CLASS_PREFIX,
    )

    method_prefix = ask_string(
        "Method name prefix",
        DEFAULT_METHOD_PREFIX,
    )

    include_imports = ask_bool(
        "Include imports?",
        True,
    )

    include_docstrings = ask_bool(
        "Include docstrings?",
        True,
    )

    include_type_hints = ask_bool(
        "Include type hints?",
        True,
    )

    include_init = ask_bool(
        "Create __init__.py?",
        True,
    )

    include_main = ask_bool(
        "Create main.py?",
        True,
    )

    randomize_logic = ask_bool(
        "Randomize generated function logic?",
        True,
    )

    random_seed_input = input(
        "Random seed [leave blank for random]: "
    ).strip()

    random_seed = None

    if random_seed_input:
        try:
            random_seed = int(random_seed_input)
        except ValueError:
            print("Invalid random seed. Using random behavior.")

    custom_imports = []

    if include_imports:
        use_default_imports = ask_bool(
            "Use default imports?",
            True,
        )

        if use_default_imports:
            custom_imports.extend(DEFAULT_IMPORTS)

        add_custom_imports = ask_bool(
            "Add custom imports?",
            False,
        )

        if add_custom_imports:
            custom_imports.extend(
                collect_custom_imports()
            )

    return GeneratorConfig(
        project_name=project_name,
        output_directory=Path(output_directory_string),
        file_count=file_count,
        functions_per_file=functions_per_file,
        classes_per_file=classes_per_file,
        methods_per_class=methods_per_class,
        file_prefix=file_prefix,
        function_prefix=function_prefix,
        class_prefix=class_prefix,
        method_prefix=method_prefix,
        include_imports=include_imports,
        include_docstrings=include_docstrings,
        include_type_hints=include_type_hints,
        include_main=include_main,
        include_init=include_init,
        custom_imports=custom_imports,
        randomize_logic=randomize_logic,
        random_seed=random_seed,
    )


FUNCTION_LOGIC_TEMPLATES = [
    [
        "if not values:",
        "    return 0",
        "return sum(values)",
    ],
    [
        "if not values:",
        "    return 0",
        "return sum(values) / len(values)",
    ],
    [
        "return len(values)",
    ],
    [
        "return [value for value in values if value > 0]",
    ],
    [
        "return [value * 2 for value in values]",
    ],
    [
        "if not values:",
        "    return None",
        "return max(values)",
    ],
    [
        "if not values:",
        "    return None",
        "return min(values)",
    ],
    [
        "return sorted(values)",
    ],
    [
        "return list(reversed(values))",
    ],
    [
        "return list(set(values))",
    ],
]


def generate_function(
    name: str,
    config: GeneratorConfig,
) -> str:
    name = sanitize_identifier(
        name,
        DEFAULT_FUNCTION_PREFIX,
    )

    if config.include_type_hints:
        signature = f"def {name}(values: list[float]) -> object:"
    else:
        signature = f"def {name}(values):"

    lines = [signature]

    if config.include_docstrings:
        lines.append(
            f'    """Automatically generated function: {name}."""'
        )

    if config.randomize_logic:
        logic = random.choice(FUNCTION_LOGIC_TEMPLATES)
    else:
        logic = FUNCTION_LOGIC_TEMPLATES[0]

    for line in logic:
        lines.append(f"    {line}")

    return "\n".join(lines)


METHOD_LOGIC_TEMPLATES = [
    "return len(self.values)",
    "return sum(self.values)",
    "return list(self.values)",
    "return sorted(self.values)",
    "return bool(self.values)",
]


def generate_method(
    name: str,
    config: GeneratorConfig,
) -> str:
    name = sanitize_identifier(
        name,
        DEFAULT_METHOD_PREFIX,
    )

    if config.include_type_hints:
        signature = f"    def {name}(self) -> object:"
    else:
        signature = f"    def {name}(self):"

    lines = [signature]

    if config.include_docstrings:
        lines.append(
            f'        """Automatically generated method: {name}."""'
        )

    logic = random.choice(METHOD_LOGIC_TEMPLATES)

    lines.append(f"        {logic}")

    return "\n".join(lines)


def generate_class(
    name: str,
    method_count: int,
    class_index: int,
    config: GeneratorConfig,
) -> str:
    name = sanitize_identifier(
        name,
        DEFAULT_CLASS_PREFIX,
    )

    lines = [f"class {name}:"]

    if config.include_docstrings:
        lines.append(
            f'    """Automatically generated class: {name}."""'
        )

    if config.include_type_hints:
        lines.extend(
            [
                "",
                "    def __init__(self, values: list[float]) -> None:",
                "        self.values = values",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "    def __init__(self, values):",
                "        self.values = values",
            ]
        )

    for method_index in range(1, method_count + 1):
        method_name = (
            f"{config.method_prefix}_"
            f"{class_index}_"
            f"{method_index}"
        )

        lines.append("")
        lines.append(
            generate_method(
                method_name,
                config,
            )
        )

    return "\n".join(lines)


def generate_module(
    module_index: int,
    config: GeneratorConfig,
) -> str:
    sections = []

    if config.include_imports and config.custom_imports:
        sections.append(
            "\n".join(config.custom_imports)
        )

    for function_index in range(
        1,
        config.functions_per_file + 1,
    ):
        function_name = (
            f"{config.function_prefix}_"
            f"{module_index}_"
            f"{function_index}"
        )

        sections.append(
            generate_function(
                function_name,
                config,
            )
        )

    for class_index in range(
        1,
        config.classes_per_file + 1,
    ):
        class_name = (
            f"{config.class_prefix}"
            f"{module_index}_"
            f"{class_index}"
        )

        sections.append(
            generate_class(
                class_name,
                config.methods_per_class,
                class_index,
                config,
            )
        )

    return "\n\n\n".join(sections) + "\n"


def generate_main_file(
    module_names: list[str],
    config: GeneratorConfig,
) -> str:
    lines = []

    if config.include_docstrings:
        lines.append(
            '"""Automatically generated application entry point."""'
        )
        lines.append("")

    if module_names:
        lines.append(
            f"import {module_names[0]}"
        )
        lines.append("")

    lines.extend(
        [
            "",
            "def main():",
            '    print("Generated project is running.")',
            "",
            "",
            'if __name__ == "__main__":',
            "    main()",
            "",
        ]
    )

    return "\n".join(lines)


def generate_project(
    config: GeneratorConfig,
) -> Path:
    if config.random_seed is not None:
        random.seed(config.random_seed)

    safe_project_name = sanitize_filename(
        config.project_name
    )

    project_directory = (
        config.output_directory
        / safe_project_name
    )

    project_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("\n" + "=" * 60)
    print("GENERATING PROJECT")
    print("=" * 60)

    module_names = []

    for module_index in range(
        1,
        config.file_count + 1,
    ):
        module_name = (
            f"{sanitize_filename(config.file_prefix)}_"
            f"{module_index}"
        )

        module_names.append(module_name)

        module_path = (
            project_directory
            / f"{module_name}.py"
        )

        source_code = generate_module(
            module_index,
            config,
        )

        module_path.write_text(
            source_code,
            encoding="utf-8",
        )

        print(f"Created: {module_path}")

    if config.include_init:
        init_path = (
            project_directory
            / "__init__.py"
        )

        init_path.write_text(
            '"""Generated Python package."""\n',
            encoding="utf-8",
        )

        print(f"Created: {init_path}")

    if config.include_main:
        main_path = (
            project_directory
            / "main.py"
        )

        main_path.write_text(
            generate_main_file(
                module_names,
                config,
            ),
            encoding="utf-8",
        )

        print(f"Created: {main_path}")

    return project_directory


def print_summary(
    config: GeneratorConfig,
    project_directory: Path,
) -> None:
    total_functions = (
        config.file_count
        * config.functions_per_file
    )

    total_classes = (
        config.file_count
        * config.classes_per_file
    )

    total_methods = (
        total_classes
        * config.methods_per_class
    )

    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)

    print(
        f"""
Project:
    {config.project_name}

Location:
    {project_directory}

Generated modules:
    {config.file_count}

Generated functions:
    {total_functions}

Generated classes:
    {total_classes}

Generated methods:
    {total_methods}

Random seed:
    {config.random_seed}
"""
    )


def main() -> None:
    config = collect_configuration()

    project_directory = generate_project(
        config
    )

    print_summary(
        config,
        project_directory,
    )


if __name__ == "__main__":
    main()
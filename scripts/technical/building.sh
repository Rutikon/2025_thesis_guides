#!/bin/bash

directoryName="$1"

mkdir -p "$directoryName"/assets
touch "$directoryName"/assets/.gitkeep

mkdir -p "$directoryName"/data/forecasts
touch "$directoryName"/data/forecasts/.gitkeep
mkdir -p "$directoryName"/data/raw
touch "$directoryName"/data/raw/.gitkeep
mkdir -p "$directoryName"/data/preprocessed
touch "$directoryName"/data/preprocessed/.gitkeep
mkdir -p "$directoryName"/data/user_input
touch "$directoryName"/data/user_input/.gitkeep

mkdir -p "$directoryName"/docs
touch "$directoryName"/docs/.gitkeep

mkdir -p "$directoryName"/models
touch "$directoryName"/models/.gitkeep

mkdir -p "$directoryName"/notebooks/eda
touch "$directoryName"/notebooks/eda/.gitkeep
mkdir -p "$directoryName"/notebooks/modeling
touch "$directoryName"/notebooks/modeling/.gitkeep
mkdir -p "$directoryName"/notebooks/data_engineering
touch "$directoryName"/notebooks/data_engineering/.gitkeep

mkdir -p "$directoryName"/references
touch "$directoryName"/references/.gitkeep

mkdir -p "$directoryName"/reports/figures
touch "$directoryName"/reports/figures/.gitkeep

mkdir -p "$directoryName"/runs
touch "$directoryName"/runs/.gitkeep

mkdir -p "$directoryName"/scripts/usage
touch "$directoryName"/scripts/usage/.gitkeep
mkdir -p "$directoryName"/scripts/technical
touch "$directoryName"/scripts/technical/.gitkeep

mkdir -p "$directoryName"/src/"$directoryName"/utils
touch "$directoryName"/src/"$directoryName"/utils/.gitkeep
mkdir -p "$directoryName"/src/"$directoryName"/data_engineering
touch "$directoryName"/src/"$directoryName"/data_engineering/.gitkeep
touch "$directoryName"/src/"$directoryName"/py.typed
touch "$directoryName"/src/"$directoryName"/__init__.py

mkdir -p "$directoryName"/submodules
touch "$directoryName"/submodules/.gitkeep

mkdir -p "$directoryName"/tests
touch "$directoryName"/tests/__init__.py

touch "$derictoryName"/LICENSE
touch "$derictoryName"/README.md
touch "$derictoryName"/requirements.txt

echo "from setuptools import setup

if __name__ == \"__main__\":
    setup()
" > "$directoryName"/setup.py

echo "[metadata]
name = $directoryName
description = ...
author = <name>
license = MIT
license_file = LICENSE
platforms = linux
classifiers =
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9

[options]
package =
    $directoryName
install-requires =
    ...
python_requires = >=3.7
package_dir = =src
zip_safe = no

[options.extras_require]
testing =
    pytest>=6
    pytest-cov>=2.0
    mypy>=0.910
    flake8>=3.9

[options.package_data]
"$directoryName" = py.typed

[flake8]
max-line-length = 80
extend-ignore = E266
exclude = .git,.venv,data
" > "$directoryName"/setup.cfg

echo "[build-system]
requires = [\"setuptools>=42.0\", \"wheel\"]
build-backend = \"setuptools.build_meta\"

[tool.pytest.ini_options]
addopts = \"--cov=$directoryName\"
testpaths = [
    \"tests\",
]

[tool.mypy]
mypy_path = \"src\"
allow_redefinition = true
check_untyped_defs = true
disallow_any_generics = true
ignore_missing_imports = true
no_implicit_optional = true
show_error_codes = true
strict_equality = true
warn_redundant_casts = true
warn_return_any = true
warn_unreachable = true
warn_unused_configs = true
no_implicit_reexports = true

[tool.autopep8]
max_line_length = 80
in-place = true
recursive = true
agressive = 2" > "$directoryName"/pyproject.toml

echo "# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

.trash
" > "$derictoryName"/.gitignore


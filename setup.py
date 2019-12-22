# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import shutil
from sys import argv

from setuptools import setup, find_packages, Command

from compiler.api import compiler as api_compiler
from compiler.docs import compiler as docs_compiler
from compiler.error import compiler as error_compiler

with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

with open("pyrogram/__init__.py", encoding="utf-8") as f:
    version = 1

with open("README.md", encoding="utf-8") as f:
    readme = f.read()


class Clean(Command):
    DIST = ["./build", "./dist", "./Pyrogram.egg-info"]
    API = ["pyrogram/errors/exceptions", "pyrogram/api/functions", "pyrogram/api/types", "pyrogram/api/all.py"]
    DOCS = [
        "docs/source/telegram", "docs/build", "docs/source/api/methods", "docs/source/api/types",
        "docs/source/api/bound-methods"
    ]

    ALL = DIST + API + DOCS

    description = "Clean generated files"

    user_options = [
        ("dist", None, "Clean distribution files"),
        ("api", None, "Clean generated API files"),
        ("docs", None, "Clean generated docs files"),
        ("all", None, "Clean all generated files"),
    ]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)

        self.dist = None
        self.api = None
        self.docs = None
        self.all = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        paths = set()

        if self.dist:
            paths.update(Clean.DIST)

        if self.api:
            paths.update(Clean.API)

        if self.docs:
            paths.update(Clean.DOCS)

        if self.all or not paths:
            paths.update(Clean.ALL)

        for path in sorted(list(paths)):
            try:
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            except OSError:
                print("skipping {}".format(path))
            else:
                print("removing {}".format(path))


class Generate(Command):
    description = "Generate Pyrogram files"

    user_options = [
        ("api", None, "Generate API files"),
        ("docs", None, "Generate docs files")
    ]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)

        self.api = None
        self.docs = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if self.api:
            error_compiler.start()
            api_compiler.start()

        if self.docs:
            docs_compiler.start()


if len(argv) > 1 and argv[1] in ["bdist_wheel", "install", "develop"]:
    api_compiler.start()
    error_compiler.start()

setup(
    name="Pyrogram",
    version=version,
    description="Telegram MTProto API Client Library and Framework for Python",
    url="https://github.com/pyrogram",
    download_url="https://github.com/pyrogram/pyrogram/releases/latest",
    author="Dan",
    author_email="dan@pyrogram.org",
    license="LGPLv3+",
    project_urls={
        "Tracker": "https://github.com/pyrogram/pyrogram/issues",
        "Community": "https://t.me/Pyrogram",
        "Source": "https://github.com/pyrogram/pyrogram",
        "Documentation": "https://docs.pyrogram.org",
    },
    python_requires="~=3.5",
    packages=find_packages(exclude=["compiler*"]),
    package_data={
        "pyrogram.client.ext": ["mime.types"],
        "pyrogram.client.storage": ["schema.sql"]
    },
    zip_safe=False,
    install_requires=requires,
    extras_require={
        "fast": ["tgcrypto==1.2.0"]
    },
    cmdclass={
        "clean": Clean,
        "generate": Generate
    }
)

# XKeyboard setup script
# Copyright (C) 2018  Matthias Gazzari
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""An X Window System keylogger based on Xlib using the RECORD extension."""

import setuptools

def read_file(file_name):
    """Return the content of a file."""
    with open(file_name) as file_obj:
        return file_obj.read()

setuptools.setup(
    name="XKeyboard",
    use_scm_version=True,
    description=__doc__,
    long_description=read_file("README.rst"),
    author="Matthias Gazzari",
    author_email="mail@qtux.eu",
    url="https://github.com/qtux/XKeyboard",
    packages=setuptools.find_packages(),
    # requirements
    install_requires=["python-xlib>=0.23",],
    setup_requires=["setuptools_scm",],
    python_requires=">=3.6",
    # further description
    keywords="X Window System X11 RECORD xlib python-xlib keylogger keycode keysym",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: X11 Applications",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
    ],
)

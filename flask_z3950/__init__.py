# -*- coding: utf8 -*-
"""Main package for Flask-Z3950."""

from .z3950 import Z3950Manager, Z3950Database
from .dataset import Dataset
from PyZ3950.zoom import ZoomError

__author__ = "Alexander Mendes"
__license__ = "BSD License"
__version__ = "0.2.5"

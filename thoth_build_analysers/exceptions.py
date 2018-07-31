#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   thoth-build-analysers
#   Copyright(C) 2018 Christoph Görn
#
#   This program is free software: you can redistribute it and / or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Exceptions used by Build Analysers."""


class ThothBuildAnalyserException(Exception):
    """A base exception for Thoth Build Analyser exception hierarchy."""


class BuildLogAnalysisException(ThothBuildAnalyserException):
    """The Analyser did not conclude anything."""


class EmptyBuildLogException(ThothBuildAnalyserException):
    """The Analyser does not work on en empty build log."""

# Copyright (c) 2011 Florian Mounier
# Copyright (c) 2012, 2014-2015 Tycho Andersen
# Copyright (c) 2013 Mattias Svala
# Copyright (c) 2013 Craig Barnes
# Copyright (c) 2014 ramnes
# Copyright (c) 2014 Sean Vig
# Copyright (c) 2014 Adi Sieker
# Copyright (c) 2014 Chris Wesseling
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest

from liblavinder import layout
import liblavinder.config
from .layout_utils import assert_dimensions
from ..conftest import no_xinerama
from .layout_utils import assert_focused, assert_focus_path


class VerticalTileConfig:
    auto_fullscreen = True
    main = None
    groups = [
        liblavinder.config.Group("a"),
        liblavinder.config.Group("b"),
        liblavinder.config.Group("c"),
        liblavinder.config.Group("d")
    ]
    layouts = [
        layout.VerticalTile(columns=2)
    ]
    floating_layout = liblavinder.layout.floating.Floating()
    keys = []
    mouse = []
    screens = []


def verticaltile_config(x):
    return no_xinerama(pytest.mark.parametrize("lavinder", [VerticalTileConfig], indirect=True)(x))


@verticaltile_config
def test_verticaltile_simple(lavinder):
    lavinder.test_window("one")
    assert_dimensions(lavinder, 0, 0, 800, 600)
    lavinder.test_window("two")
    assert_dimensions(lavinder, 0, 300, 798, 298)
    lavinder.test_window("three")
    assert_dimensions(lavinder, 0, 400, 798, 198)


@verticaltile_config
def test_verticaltile_maximize(lavinder):
    lavinder.test_window("one")
    assert_dimensions(lavinder, 0, 0, 800, 600)
    lavinder.test_window("two")
    assert_dimensions(lavinder, 0, 300, 798, 298)
    # Maximize the bottom layout, taking 75% of space
    lavinder.c.layout.maximize()
    assert_dimensions(lavinder, 0, 150, 798, 448)


@verticaltile_config
def test_verticaltile_window_focus_cycle(lavinder):
    # setup 3 tiled and two floating clients
    lavinder.test_window("one")
    lavinder.test_window("two")
    lavinder.test_window("float1")
    lavinder.c.window.toggle_floating()
    lavinder.test_window("float2")
    lavinder.c.window.toggle_floating()
    lavinder.test_window("three")

    # test preconditions
    assert lavinder.c.layout.info()['clients'] == ['one', 'two', 'three']
    # last added window has focus
    assert_focused(lavinder, "three")

    # assert window focus cycle, according to order in layout
    assert_focus_path(lavinder, 'float1', 'float2', 'one', 'two', 'three')

=============
Configuration
=============

Lavinder is configured in Python. A script (``~/.config/lavinder/config.py`` by
default) is evaluated, and a small set of configuration variables are pulled
from its global namespace.

Configuration lookup order
==========================

Lavinder looks in the following places for a configuration file, in order:

* The location specified by the ``-c`` argument.
* ``$XDG_CONFIG_HOME/lavinder/config.py``, if it is set
* ``~/.config/lavinder/config.py``
* It reads the module ``liblavinder.resources.default_config``, included by
  default with every Lavinder installation.

Default Configuration
=====================

The `default configuration
<https://github.com/lavinder/lavinder/blob/develop/liblavinder/resources/default_config.py>`_
is invoked when lavinder cannot find a configuration file. In addition, if lavinder
is restarted via qshell, lavinder will load the default configuration if the
config file it finds has some kind of error in it. The documentation below
describes the configuration lookup process, as well as what the key bindings
are in the default config.

The default config is not intended to be suitable for all users; it's mostly
just there so lavinder does /something/ when fired up, and so that it doesn't
crash and cause you to lose all your work if you reload a bad config.

Key Bindings
------------

The mod key for the default config is ``mod4``, which is typically bound to
the "Super" keys, which are things like the windows key and the mac command
key. The basic operation is:

* ``mod + k`` or ``mod + j``: switch windows on the current stack
* ``mod + <space>``: put focus on the other pane of the stack (when in stack
  layout)
* ``mod + <tab>``: switch layouts
* ``mod + w``: close window
* ``mod + <ctrl> + r``: restart lavinder with new config
* ``mod + <group name>``: switch to that group
* ``mod + <shift> + <group name>``: send a window to that group
* ``mod + <enter>``: start xterm
* ``mod + r``: start a little prompt in the bar so users can run arbitrary
  commands

The default config defines one screen and 8 groups, one for each letter in
``asdfuiop``. It has a basic bottom bar that includes a group box, the current
window name, a little text reminder that you're using the default config,
a system tray, and a clock.

The default configuration has several more advanced key combinations, but the
above should be enough for basic usage of lavinder.

Mouse Bindings
--------------

By default, holding your ``mod`` key and clicking (and holding) a window will
allow you to drag it around as a floating window.


Configuration variables
=======================

A Lavinder configuration consists of a file with a bunch of variables in it, which
lavinder imports and then runs as a python file to derive its final configuration.
The documentation below describes the most common configuration variables; more
advanced configuration can be found in the `lavinder-examples
<https://github.com/lavinder/lavinder-examples>`_ repository, which includes a number
of real-world configurations that demonstrate how you can tune Lavinder to your
liking. (Feel free to issue a pull request to add your own configuration to the
mix!)

.. toctree::
    :maxdepth: 1

    lazy
    groups
    keys
    layouts
    mouse
    screens
    hooks

In addition to the above variables, there are several other boolean
configuration variables that control specific aspects of Lavinder's behavior:

.. list-table::
    :widths: 10 10 80
    :header-rows: 1

    * - variable
      - default
      - description
    * - auto_fullscreen
      - True
      - If a window requests to be fullscreen, it is automatically
        fullscreened. Set this to false if you only want windows to be
        fullscreen if you ask them to be.
    * - bring_front_click
      - False
      - When clicked, should the window be brought to the front or not. (This
        sets the X Stack Mode to Above.)
    * - cursor_warp
      - False
      - If true, the cursor follows the focus as directed by the keyboard,
        warping to the center of the focused window.
    * - dgroups_key_binder
      - None
      - TODO
    * - dgroups_app_rules
      - []
      - TODO
    * - extension_defaults
      - same as `widget_defaults`
      - Default settings for extensions.
    * - floating_layout
      - layout.Floating(float_rules=[...])
      - TODO

        See the configuration file for the default `float_rules`.
    * - focus_on_window_activation
      - smart
      - Behavior of the _NET_ACTIVATE_WINDOW message sent by applications

        - urgent: urgent flag is set for the window

        - focus: automatically focus the window

        - smart: automatically focus if the window is in the current group
    * - follow_mouse_focus
      - True
      - Controls whether or not focus follows the mouse around as it moves
        across windows in a layout.
    * - main
      - None
      - TODO
    * - widget_defaults
      - dict(font='sans',
             fontsize=12,
             padding=3)
      - Default settings for bar widgets.
    * - wmname
      - "LG3D"
      - TODO

Testing your configuration
==========================

The best way to test changes to your configuration is with the provided Xephyr
script. This will run Lavinder with your ``config.py`` inside a nested X server
and prevent your running instance of Lavinder from crashing if something goes
wrong.

See :doc:`Hacking Lavinder </manual/hacking>` for more information on using
Xephyr.

Starting Lavinder
=================

There are several ways to start Lavinder. The most common way is via an entry in
your X session manager's menu. The default Lavinder behavior can be invoked by
creating a `lavinder.desktop
<https://github.com/lavinder/lavinder/blob/master/resources/lavinder.desktop>`_ file in
``/usr/share/xsessions``.

A second way to start Lavinder is a custom X session. This way allows you to
invoke Lavinder with custom arguments, and also allows you to do any setup you
want (e.g. special keyboard bindings like mapping caps lock to control, setting
your desktop background, etc.) before Lavinder starts. If you're using an X
session manager, you still may need to create a ``custom.desktop`` file similar
to the ``lavinder.desktop`` file above, but with ``Exec=/etc/X11/xsession``. Then,
create your own ``~/.xsession``. There are several examples of user defined
``xsession`` s in the `lavinder-examples
<https://github.com/lavinder/lavinder-examples>`_ repository.

Finally, if you're a gnome user, you can start integrate Lavinder into Gnome's
session manager and use gnome as usual:

.. toctree::
    :maxdepth: 1

    gnome

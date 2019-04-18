====================
Running Inside Gnome
====================

Add the following snippet to your Lavinder configuration. As per `this
page <https://wiki.gnome.org/Projects/SessionManagement/GnomeSession#A3._Register>`_,
it registers Lavinder with gnome-session. Without it, a "Something has gone
wrong!" message shows up a short while after logging in. dbus-send must
be on your $PATH.

.. code-block:: python

    import subprocess
    import os
    from liblavinder import hook

    @hook.subscribe.startup
    def dbus_register():
        id = os.environ.get('DESKTOP_AUTOSTART_ID')
        if not id:
            return
        subprocess.Popen(['dbus-send',
                          '--session',
                          '--print-reply',
                          '--dest=org.gnome.SessionManager',
                          '/org/gnome/SessionManager',
                          'org.gnome.SessionManager.RegisterClient',
                          'string:lavinder',
                          'string:' + id])

This adds a new entry "Lavinder GNOME" to GDM's login screen.

::

    $ cat /usr/share/xsessions/lavinder_gnome.desktop
    [Desktop Entry]
    Name=Lavinder GNOME
    Comment=Tiling window manager
    TryExec=/usr/bin/gnome-session
    Exec=gnome-session --session=lavinder
    Type=XSession

The custom session for gnome-session.

::

    $ cat /usr/share/gnome-session/sessions/lavinder.session
    [GNOME Session]
    Name=Lavinder session
    RequiredComponents=lavinder;gnome-settings-daemon;

So that Lavinder starts automatically on login.

::

    $ cat /usr/share/applications/lavinder.desktop
    [Desktop Entry]
    Type=Application
    Encoding=UTF-8
    Name=Lavinder
    Exec=lavinder
    NoDisplay=true
    X-GNOME-WMName=Lavinder
    X-GNOME-Autostart-Phase=WindowManager
    X-GNOME-Provides=windowmanager
    X-GNOME-Autostart-Notify=false

The above does not start gnome-panel. Getting gnome-panel to work
requires some extra Lavinder configuration, mainly making the top and
bottom panels static on panel startup and leaving a gap at the top (and
bottom) for the panel window.

You might want to add keybindings to log out of the GNOME session.

.. code-block:: python

    Key([mod, 'control'], 'l', lazy.spawn('gnome-screensaver-command -l')),
    Key([mod, 'control'], 'q', lazy.spawn('gnome-session-quit --logout --no-prompt')),
    Key([mod, 'shift', 'control'], 'q', lazy.spawn('gnome-session-quit --power-off')),

The above apps need to be in your path (though they are typically
installed in ``/usr/bin``, so they probably are if they're installed
at all).

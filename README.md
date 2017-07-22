gnome-presence
==============

This is a little Python script which runs scripts in your home directory
when your computer becomes idle (e.g. when screensaver is about to
kick in), when it becomes active again (when you move the mouse or
otherwise stop the screensaver and/or unlock it), and in either
of these cases.

This was written because of GNOME's perplexing decision to remove the
very useful `gnome-screensaver-command` program which could be used
in shell scripts to perform actions when the computer was becoming
idle, such as pausing music, or in my case, telling BOINC that it can
go crazy with my GPUs, and pause the GPU jobs when I return to my
computer again (a feature which is part of BOINC, but broken for me).


Installing
-----------
This software assumes you're running a new-ish version of GNOME 3, on a
UNIX OS which has Python installed and the requisite dbus and GObject
introspection Python libraries already installed -- Fedora 26, the
distro I tested this on, comes with all these out of the box, and I assume
so do all other Linux distributions which come with the GNOME 3
desktop environment.

Run the command:

    sudo python setup.py install

Now you'll have `gnome-presence` globally installed to `/usr/bin` on your
system.


Running
-------
By default, `gnome-presence` runs silently and indefinitely:

    $ gnome-presence

To make it chattier:

    $ gnome-presence -v

You can also get it to wait for an idle/active event and then quit
("one-shot" mode):

    $ gnome-presence -o

Combining this with `--no-scripts`/`-n`, you can use it simply to wait for
an event to happen:

    $ gnome-presence -o -n

If you wanted to wait until a user comes back in a shell script:

    $ gnome-presence -o -n -e active

If you want it to tell you what event it's received, you can set
`--output-format`/`-f`:

    $ gnome-presence -f '{state}: {state_id}'

Which would give you output like:

    active: 0
    idle: 3
    active: 0
    idle: 3


Script directories
------------------

By default, it will look in these directories:
* `~/.local/gnome-presence/idle.d`
* `~/.local/gnome-presence/active.d`
* `~/.local/gnome-presence/both.d`

Any files you put in those directories need to be made executable in order
for it to run them.

You can make it look in different directories with command line arguments:
`--idle-dir`, `--active-dir` and `--both-dir`.

If you want it to run your `active` scripts when you first start the
program, pass it `--active-on-start`.


Script environment
------------------

The running scripts are given an extra environment variable,
 `PRESENCED_STATE`. That describes what state the session is in. It will be
 one of `active`, `idle` or `both`.

`gnome-presence` spawns the processes but does not wait for them, nor does
it kill them if itself quits. If you have any long running processes you
should make sure to stop them yourself. You can make it wait for the
spawned processes to end upon exit with `--wait-on-exit`.

If you want it to stop or kill processes spawned at the previous event, you
can pass it `--stop-processes` and `--kill-processes`. It tries to stop
them normally first, and then if `--kill-processes` is specified it waits
a number of seconds specified by `--kill-timeout` (default: 5 seconds) and
then sends them the KILL signal.


Behind the scenes
-----------------

It's using the Python DBus interface to listen to signals from
`org.gnome.SessionManager.Presence`. When Gnome starts to fade your screen
to black, and when you do something to come back from screensaver like moving
your mouse, it emits a DBus signal at
`org.gnome.SessionManager.Presence.StatusChanged`, with an integer value.
A value of `0` is `active` (user is present), any other value is `idle`
(session is idle). So far I've only seen it alternate between `0` and `3` but
possibly other values exist for other states like user switching or screen
locking.
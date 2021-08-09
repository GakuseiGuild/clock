import numpy as np
import math
import cairo
import datetime
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf  # nopep8


def rotation2d(theta):
    cos = np.cos(theta)
    sin = np.sin(theta)
    return np.array([[cos, -sin],
                     [sin,  cos]])


class clock_area(Gtk.DrawingArea):
    def __init__(self, css=None, border_width=0):
        super().__init__()
        self.vexpand = True
        self.hexpand = True
        self.surface = None

        self.connect("draw", self.on_draw)

        def tick_callback(self, ptr):
            self.queue_draw()
            return True
        self.add_tick_callback(tick_callback)

    def on_draw(self, area, cr):
        aw = area.get_allocated_width()
        ah = area.get_allocated_height()

        line_width = 5.0
        rad = 100.0
        field_width = 2.0 * (rad + line_width)
        field_height = 2.0 * (rad + line_width)

        img = cairo.ImageSurface.create_from_png("clock.png")
        coef = min(aw / (img.get_width() + 2.0 * line_width),
                   ah / (img.get_height() + 2.0 * line_width))
        cr.identity_matrix()
        cr.scale(coef, coef)
        cr.translate(line_width, line_width)
        cr.set_source_surface(img)
        cr.paint()

        cr.identity_matrix()
        coef = min(aw / field_width, ah / field_height)
        cr.transform(cairo.Matrix(coef, 0, 0, -coef, coef *
                     field_width / 2.0, coef * field_height / 2.0))

        # cr.set_source_rgb(1.0, 1.0, 1.0)
        # cr.arc(0.0, 0.0, rad, 0.0, 2.0 * math.pi)
        # cr.fill()

        cr.set_source_rgb(0.0, 0.0, 0.0)

        # circle
        cr.set_line_width(line_width)
        cr.arc(0.0, 0.0, rad, 0.0, 2.0 * math.pi)
        cr.stroke()

        now = datetime.datetime.now()

        # long hand
        target = np.dot(rotation2d(- (now.minute / 60.0) *
                        2.0 * math.pi), np.array([0.0, 0.9 * rad]))
        cr.set_line_width(0.25 * line_width)
        cr.move_to(0, 0)
        cr.line_to(target[0], target[1])
        cr.stroke()

        # short hand
        target = np.dot(rotation2d(-((now.hour % 12) / 12) *
                        2.0 * math.pi - (now.minute / 60.0) * math.pi / 12.0), np.array([0.0, 0.5 * rad]))
        cr.set_line_width(0.5 * line_width)
        cr.move_to(0, 0)
        cr.line_to(target[0], target[1])
        cr.stroke()
        return False


class window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("clock")
        self.set_default_size(800, 600)
        self.connect("destroy", Gtk.main_quit)

        ca = clock_area()
        self.add(ca)


window = window()
window.show_all()
Gtk.main()

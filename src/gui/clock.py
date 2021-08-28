import numpy as np
import math
import os
import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # nopep8


class ClockArea(Gtk.DrawingArea):
    def __init__(self, clk):
        super().__init__()
        self.connect("draw", self.on_draw)

        def tick_callback(self, ptr):
            self.queue_draw()
            return True
        self.add_tick_callback(tick_callback)

        self.__clk = clk

    def on_draw(self, area, cr):
        aw = area.get_allocated_width()
        ah = area.get_allocated_height()

        line_width = 5.0
        rad = 100.0
        field_width = 2.0 * (rad + line_width)
        field_height = 2.0 * (rad + line_width)

        cr.identity_matrix()
        coef = min(aw / field_width, ah / field_height)
        offset_x = (aw - coef * field_width) / 2.0
        offset_y = (ah - coef * field_height) / 2.0
        cr.translate(offset_x, offset_y)
        cr.transform(cairo.Matrix(coef, 0, 0, -coef, coef *
                     field_width / 2.0, coef * field_height / 2.0))

        cr.set_source_rgb(1.0, 1.0, 1.0)

        # circle
        cr.set_line_width(line_width)
        cr.arc(0.0, 0.0, rad, 0.0, 2.0 * math.pi)
        cr.fill()

        dial_path = os.path.dirname(
            __file__) + "/../assets/" + self.__clk.dial_name()
        if os.path.isfile(dial_path):
            try:
                img = cairo.ImageSurface.create_from_png(dial_path)
                prev_coef = coef
                coef = min((aw - 2.0 * line_width * coef) / img.get_width(),
                           (ah - 2.0 * line_width * coef) / img.get_height())
                cr.identity_matrix()
                cr.translate(offset_x, offset_y)
                cr.scale(coef, coef)
                cr.translate(line_width * prev_coef / coef,
                             line_width * prev_coef / coef)
                cr.set_source_surface(img)
                cr.paint()
            except:
                pass

        cr.identity_matrix()
        coef = min(aw / field_width, ah / field_height)
        cr.translate(offset_x, offset_y)
        cr.transform(cairo.Matrix(coef, 0, 0, -coef, coef *
                     field_width / 2.0, coef * field_height / 2.0))

        def rotation2d(dir):
            cos = np.cos(dir)
            sin = np.sin(dir)
            return np.array([[cos, -sin],
                             [sin,  cos]])

        target_long = np.dot(rotation2d(self.__clk.dir().long),
                             np.array([0.9 * rad, 0.0]))
        target_short = np.dot(rotation2d(self.__clk.dir().short),
                              np.array([0.5 * rad, 0.0]))

        cr.set_source_rgb(0.0, 0.0, 0.0)

        # title
        text = "GakuseiGuild"
        font_size = 2.0 * line_width
        cr.set_font_size(font_size)
        cr.select_font_face("Courier", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_matrix(cairo.Matrix(
            font_size, 0.0, 0.0, -font_size, 0.0, 0.0))
        cr.move_to(-font_size * 14 / 4.0, font_size)
        cr.text_path(text)
        cr.fill()

        # long hand
        cr.set_line_width(0.25 * line_width)
        cr.move_to(0, 0)
        cr.line_to(target_long[0], target_long[1])
        cr.stroke()

        # short hand
        cr.set_line_width(0.5 * line_width)
        cr.move_to(0, 0)
        cr.line_to(target_short[0], target_short[1])
        cr.stroke()

        # circle
        cr.set_line_width(line_width)
        cr.arc(0.0, 0.0, 0.035 * rad, 0.0, 2.0 * math.pi)
        cr.fill()
        return False


class Window(Gtk.Window):
    def __init__(self, __clk):
        Gtk.Window.__init__(self)
        self.set_title("GakuseiGuild Magic clock")
        self.set_default_size(800, 600)
        self.connect("destroy", Gtk.main_quit)

        ca = ClockArea(__clk)
        self.add(ca)
        self.show_all()

    def main(self):
        Gtk.main()

import os
import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # nopep8


class EpaperArea(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.connect("draw", self.on_draw)

        def tick_callback(self, ptr):
            self.queue_draw()
            return True
        self.add_tick_callback(tick_callback)

    def on_draw(self, area, cr):
        aw = area.get_allocated_width()
        ah = area.get_allocated_height()
        MARGIN = 5

        for i in range(1, 5):
            file_path = os.path.dirname(
                __file__) + "/../.out/" + str(i) + ".png"
            if os.path.isfile(file_path):
                try:
                    img = cairo.ImageSurface.create_from_png(file_path)
                    coef = min(aw / (img.get_width() * 2 + MARGIN),
                               ah / (img.get_height() * 2 + MARGIN))
                    offset_x = (
                        aw - coef * (img.get_width() * 2.0 + MARGIN)) / 2.0
                    offset_y = (
                        ah - coef * (img.get_height() * 2.0 + MARGIN)) / 2.0
                    x = (0 if i % 2 == 1 else img.get_width() + MARGIN)
                    y = (0 if 2 < i else img.get_height() + MARGIN)
                    cr.identity_matrix()
                    cr.translate(offset_x, offset_y)
                    cr.scale(coef, coef)
                    cr.translate(x, y)
                    cr.set_source_rgb(1.0, 1.0, 1.0)
                    cr.rectangle(0.0, 0.0, img.get_width(), img.get_height())
                    cr.fill()
                    cr.set_source_surface(img)
                    cr.paint()
                except:
                    pass
        return False


class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("GakuseiGuild Magic clock epaper simulator")
        self.set_default_size(800, 600)
        self.connect("destroy", Gtk.main_quit)

        ea = EpaperArea()
        self.add(ea)
        self.show_all()

    def main(self):
        Gtk.main()


if __name__ == "__main__":
    win = Window()
    win.main()

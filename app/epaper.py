import fcntl
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

        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.rectangle(0.0, 0.0, aw, ah)
        cr.fill()

        for i in range(1, 5):
            file_path = os.path.dirname(
                __file__) + "/../.out/" + str(i) + ".png"
            if os.path.isfile(file_path):
                with open(file_path, "r+") as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    img = cairo.ImageSurface.create_from_png(file_path)
                    coef = min(aw / (img.get_width() * 2),
                               ah / (img.get_height() * 2))
                    x = 0 if i % 2 == 1 else img.get_width()
                    y = 0 if 2 < i else img.get_height()
                    cr.identity_matrix()
                    cr.scale(coef, coef)
                    cr.translate(x, y)
                    cr.set_source_surface(img)
                    cr.paint()
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

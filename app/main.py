import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src.app.ui import MainUI


if __name__ == "__main__":
    """
    punto de inicio del programa
    """
    MainUI()
    Gtk.main()

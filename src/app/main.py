import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src.app.vista.MainUI import MainUI

if __name__ == "__main__":
    MainUI()
    Gtk.main()

import gi

from app.ui import MainUI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def main():
    MainUI()
    Gtk.main()


if __name__ == "__main__":
    """
    punto de inicio del programa
    """
    main()

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import subprocess


class AppWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Hello World")
        self.mode = ''
        self.power_save_btn = Gtk.Button(label="Power Save")
        self.performance_btn = Gtk.Button(label="Performance")
        self.balanced_btn = Gtk.Button(label="Balanced")
        self.get_mode_btn = Gtk.Button(label="Get Current Mode")
        self.set_border_width(10)
        self.set_default_size(200, 100)
        self.set_title("Power Mode Switcher")
        self.set_resizable(False)
        self.set_icon_name("system-run")

        # Connect button signals
        self.power_save_btn.connect("clicked", self.power_save_btn_clicked)
        self.performance_btn.connect("clicked", self.performance_btn_clicked)
        self.balanced_btn.connect("clicked", self.balanced_btn_clicked)
        self.get_mode_btn.connect("clicked", self.get_mode_btn_clicked)

        # Create a grid and add buttons to it
        self.grid = Gtk.Grid()
        self.grid.add(self.power_save_btn)
        self.grid.add(self.balanced_btn)
        self.grid.add(self.performance_btn)
        self.grid.add(self.get_mode_btn)

        # Connect key-press-event signal
        self.connect("key-press-event", self.on_key_press)

        self.set_position(Gtk.WindowPosition.CENTER)  # Устанавливаем положение окна в центре экрана

        # Add the grid to the window
        self.add(self.grid)

    def power_save_btn_clicked(self, widget):
        cmd_out = subprocess.run(["bash", "-c", "powerprofilesctl set power-saver"], capture_output=True, text=True)
        self.mode = cmd_out.stdout.strip()
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Current Mode")
        dialog.format_secondary_text(self.mode)
        dialog.run()
        dialog.destroy()
        
    def balanced_btn_clicked(self, widget):
        cmd_out = subprocess.run(["bash", "-c", "powerprofilesctl set balanced"], capture_output=True, text=True)
        self.mode = cmd_out.stdout.strip()
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Current Mode")
        dialog.format_secondary_text(self.mode)
        dialog.run()
        dialog.destroy()
    def performance_btn_clicked(self, widget):
        cmd_out = subprocess.run(["bash", "-c", "powerprofilesctl set performance"], capture_output=True, text=True)
        self.mode = cmd_out.stdout.strip()
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Current Mode")
        dialog.format_secondary_text(self.mode)
        dialog.run()
        dialog.destroy()

    def get_mode_btn_clicked(self, widget):
        cmd_out = subprocess.run(["bash", "-c", "powerprofilesctl get"], capture_output=True, text=True)
        self.mode = cmd_out.stdout.strip()
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Current Mode")
        dialog.format_secondary_text(self.mode)
        dialog.run()
        dialog.destroy()

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.close()




win = AppWindow()

win.connect("destroy", Gtk.main_quit)

win.show_all()

Gtk.main()
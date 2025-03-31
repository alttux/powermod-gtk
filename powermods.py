import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import subprocess


class AppWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Power Mode Switcher")

        self.set_border_width(10)
        self.set_default_size(200, 90)  # Оставил ваш размер окна
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name("system-run")

        self.mode = ""

        # Создаем кнопки
        self.power_save_btn = Gtk.Button(label="Power Save")
        self.performance_btn = Gtk.Button(label="Performance")
        self.balanced_btn = Gtk.Button(label="Balanced")
        self.get_mode_btn = Gtk.Button(label="Get Current Mode")

        # Привязываем события к кнопкам
        self.power_save_btn.connect("clicked", lambda _: self.set_power_mode("power-saver"))
        self.performance_btn.connect("clicked", lambda _: self.set_power_mode("performance"))
        self.balanced_btn.connect("clicked", lambda _: self.set_power_mode("balanced"))
        self.get_mode_btn.connect("clicked", self.get_power_mode)

        # Создаем сетку и добавляем кнопки
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)
        self.grid.attach(self.power_save_btn, 0, 0, 1, 1)
        self.grid.attach(self.balanced_btn, 1, 0, 1, 1)
        self.grid.attach(self.performance_btn, 0, 1, 1, 1)
        self.grid.attach(self.get_mode_btn, 1, 1, 1, 1)

        self.add(self.grid)

        # Подключаем обработчик клавиш
        self.connect("key-press-event", self.on_key_press)

    def set_power_mode(self, mode: str):
        """ Устанавливает режим энергопотребления и показывает диалог с результатом. """
        try:
            subprocess.run(["powerprofilesctl", "set", mode], check=True, capture_output=True, text=True)
            self.show_dialog("Power mode switched", f"Current mode: {mode}")
        except FileNotFoundError:
            self.show_dialog("Error", "powerprofilesctl не найден. Убедитесь, что он установлен.", error=True)
        except subprocess.CalledProcessError as e:
            self.show_dialog("Error", f"Ошибка при выполнении команды: {e.stderr}", error=True)

    def get_power_mode(self, _):
        """ Получает текущий режим энергопотребления и отображает его. """
        try:
            cmd_out = subprocess.run(["powerprofilesctl", "get"], check=True, capture_output=True, text=True)
            mode = cmd_out.stdout.strip()
            self.show_dialog("Current Mode", f"Current power mode: {mode}")
        except FileNotFoundError:
            self.show_dialog("Error", "powerprofilesctl не найден. Убедитесь, что он установлен.", error=True)
        except subprocess.CalledProcessError as e:
            self.show_dialog("Error", f"Ошибка при выполнении команды: {e.stderr}", error=True)

    def show_dialog(self, title: str, message: str, error: bool = False):
        """ Универсальный метод для показа диалогового окна. """
        dialog = Gtk.MessageDialog(
            self, 0, Gtk.MessageType.ERROR if error else Gtk.MessageType.INFO, Gtk.ButtonsType.OK, title
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def on_key_press(self, _, event):
        """ Закрывает окно при нажатии Escape. """
        if event.keyval == Gdk.KEY_Escape:
            self.close()


# Запуск приложения
win = AppWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

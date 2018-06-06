class DialogWidget(object):
    def __init__(self, widget, dialog_widget):
        self.dialog = False
        self.widget = widget
        self.dialog_widget = dialog_widget

    def draw(self, stdscr, is_selected, x, y, width, height):
        if self.dialog:
            self.dialog_widget.draw(stdscr, is_selected, x, y, width, height)
        else:
            self.widget.draw(stdscr, is_selected, x, y, width, height)

    def cursor_loc(self, stdscr, x, y, width, height):
        return self._get_widget().cursor_loc(stdscr, x, y, width, height)

    def key(self, key):
        if key == '\x0e':
            self.dialog = True
            return True

        if key == '\x1b':
            self.dialog = False
            return True

        self._get_widget().key(key)

    def _get_widget(self):
        if self.dialog:
            return self.dialog_widget
        return self.widget

    def hide_dialog(self):
        self.dialog = False

    def show_dialog(self):
        self.dialog = True

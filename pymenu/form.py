import curses
import string

class FormWidget(object):
    def __init__(self, fields, on_enter):

        # ensure all keys exist
        for field in fields:

            # optional keys:
            if 'name' not in field:
                field['name'] = field['label']
            if 'value' not in field:
                field['value'] = ''

            # required keys:
            field['label']

        self.fields = fields
        self.on_enter = on_enter
        self.selected_i = 0
        self.label_width = max(len(x['label']) for x in fields)
        self.cursor_loc_x = 0
        self.cursor_loc_y = 0

    def clear(self):
        for field in self.fields:
            field['value'] = ''
        self.selected_i = 0

    def draw(self, stdscr, is_selected, x, y, width, height):
        yy = 0

        for i, field in enumerate(self.fields):
            stdscr.addstr(y+yy, x, field['label'])
            text = field['value']
            stdscr.addstr(y+yy, x+self.label_width+1, text)
            if i == self.selected_i:
                self.cursor_loc_x = self.label_width+1+len(text)
                self.cursor_loc_y = yy

            yy += field.get('height', 1)

        style = 0
        if self.selected_i == len(self.fields):
            style = curses.A_REVERSE
        stdscr.addstr(y+yy, x+self.label_width+1, '<OK>', style)

    def cursor_loc(self, stdscr, x, y, width, height):
        if self.selected_i == len(self.fields):
            # button is selected
            return False
        stdscr.addstr(y + self.cursor_loc_y, x + self.cursor_loc_x, '')
        return True

    def key(self, key):
        if key in ('KEY_UP',):
            if self.selected_i > 0:
                self.selected_i -= 1
            return True

        if key in ('KEY_DOWN',):
            if self.selected_i < (len(self.fields)):
                self.selected_i += 1
            return True

        if key in ('\t',):
            self.selected_i += 1
            if self.selected_i > len(self.fields):
                self.selected_i = 0
            return True

        if self.selected_i == len(self.fields):
            if key == '\n':
                self.on_enter({x['name']: x['value'] for x in self.fields})
            return True

        field = self.fields[self.selected_i]
        if key == 'KEY_BACKSPACE':
            field['value'] = field['value'][:-1]
            return True

        if key in ('\t', '\n'):
            return True

        if key in string.printable:
            field['value'] = field['value'] + key
            return True

        return True


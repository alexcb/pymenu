import curses
import string

def _pad_cols(rows, width):
    if not rows:
        return []

    num_cols = max(len(x) for x in rows)
    assert num_cols == min(len(x) for x in rows)

    width = [0] * num_cols
    for i in range(num_cols):
        width[i] = max(len(x[i]) for x in rows)

    padded = []
    for row in rows:
        padded.append(' '.join(x.ljust(w) for x, w in zip(row, width)))
    return padded


class TableWidget(object):
    def __init__(self, items, callback=None, search=False):
        self.items = items
        self.selected_i = 0
        self.first_displayed = 0
        self.callback = callback
        self.search = search
        self.search_active = False
        self.search_text = ''
        self.visible_items = items

    def _fix_first_displayed(self, height):
        if self.first_displayed > self.selected_i:
            self.first_displayed = self.selected_i
            return

        d = self.selected_i - self.first_displayed
        if d >= height:
            self.first_displayed = self.selected_i - height + 1

    def draw(self, stdscr, is_selected, x, y, width, height):
        if not self.visible_items:
            stdscr.addstr(y, x, '<no data>')

        items = _pad_cols(self.visible_items, width)
        self._fix_first_displayed(height)
        if self.search_active:
            height -= 1
        for i in range(height):
            ii = i + self.first_displayed
            if ii >= len(items):
                break
            style = 0
            if (ii == self.selected_i and is_selected):
                style |= curses.A_REVERSE
            stdscr.addstr(y+i, x, items[ii], style)
        if self.search_active:
            stdscr.addstr(y+height-1, x, 'search: %s' % (self.search_text,))


    def cursor_loc(self, stdscr, x, y, width, height):
        pass

    def _set_visible_items(self):
        def is_match(x):
            for xx in x:
                if self.search_text in xx:
                    return True
            return False

        try:
            last_selected = self.visible_items[self.selected_i]
        except IndexError:
            last_selected = None

        self.visible_items = [x for x in self.items if is_match(x)]

        try:
            self.selected_i = self.visible_items.index(last_selected)
        except ValueError:
            self.selected_i = 0

    def key(self, key):
        import logging
        logging.info('got %s' % key)
        if self.search_active:
            if key in string.printable and key not in ('\n', '\t'):
                self.search_text += key
                self._set_visible_items()
                return
            if key == 'KEY_BACKSPACE':
                self.search_text = self.search_text[:-1]
                self._set_visible_items()
                return
            if key == '\x1b':
                self.search_text = ''
                self._set_visible_items()
                return

        if key in ('k', 'KEY_UP'):
            if self.selected_i > 0:
                self.selected_i -= 1
            return

        if key in ('j', 'KEY_DOWN'):
            if self.selected_i < (len(self.visible_items)-1):
                self.selected_i += 1
            return

        if key == '\n':
            if self.callback:
                i = self.items.index(self.visible_items[self.selected_i])
                self.callback(i)
            return

        if key == '/' and self.search and not self.search_active:
            self.search_active = True



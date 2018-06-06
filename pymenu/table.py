import curses

def _pad_cols(rows, width):
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
    def __init__(self, items, callback=None):
        self.items = items
        self.selected_i = 0
        self.first_displayed = 0
        self.callback = callback

    def _fix_first_displayed(self, height):
        if self.first_displayed > self.selected_i:
            self.first_displayed = self.selected_i
            return

        d = self.selected_i - self.first_displayed
        if d >= height:
            self.first_displayed = self.selected_i - height + 1

    def draw(self, stdscr, is_selected, x, y, width, height):
        items = _pad_cols(self.items, width)
        self._fix_first_displayed(height)
        for i in range(height):
            ii = i + self.first_displayed
            if ii >= len(items):
                break
            style = 0
            if (ii == self.selected_i and is_selected):
                style |= curses.A_REVERSE
            stdscr.addstr(y+i, x, items[ii], style)

    def cursor_loc(self, stdscr, x, y, width, height):
        pass

    def key(self, key):
        if key in ('k', 'KEY_UP'):
            if self.selected_i > 0:
                self.selected_i -= 1
        elif key in ('j', 'KEY_DOWN'):
            if self.selected_i < (len(self.items)-1):
                self.selected_i += 1
        elif key == '\n':
            if self.callback:
                self.callback(self.selected_i)

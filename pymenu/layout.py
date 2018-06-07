import curses

def _get_loc(percentages, height):
    w = []

    y = 0
    remaining = height
    for p in percentages:
        if p.endswith('%'):
            p = int(float(p[:-1]) / 100.0 * float(height))
            if p == 0:
                p = 1
            if p > remaining:
                p = remaining
            remaining -= p
            w.append(p)
        else:
            assert 0, 'not supported'

    if remaining:
        w[-1] += remaining
    return w



def _run(stdscr, widget):
    curses.halfdelay(2)
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        widget.draw(stdscr, True, 0, 0, width, height)
        display = widget.cursor_loc(stdscr, 0, 0, width, height)
        if display:
            curses.curs_set(2)
        else:
            curses.curs_set(0)
        stdscr.refresh()
        try:
            k = stdscr.getkey()
        except KeyboardInterrupt:
            raise
        except:
            pass
        else:
            widget.key(k)


def run(widget):
    curses.wrapper(_run, widget)


class LayoutWidget(object):
    def __init__(self, widgets):
        self.widgets = widgets
        self.window_move = False
        self.selected_i = 0
        self.selected_widget = None
        self.selected_args = None

    def draw(self, stdscr, is_selected, x, y, width, height):
        height, width = stdscr.getmaxyx()

        self.selected_widget = None
        self.selected_args = None

        heights = _get_loc((x[0] for x in self.widgets), height)
        y = 0
        for i, (h, widget) in enumerate(zip(heights, (x[1] for x in self.widgets))):
            selected = bool(i == self.selected_i)
            widget.draw(stdscr, selected, 0, y, width, h)
            if selected:
                self.selected_widget = widget
                self.selected_args = (0, y, width, h)
            y += h


    def cursor_loc(self, stdscr, x, y, width, height):
        if self.selected_widget:
            return self.selected_widget.cursor_loc(stdscr, *self.selected_args)
        return False

    def key(self, key):
        if self.window_move:
            if key in ('KEY_UP', 'k'):
                if self.selected_i > 0:
                    self.selected_i -= 1
            elif key in ('KEY_DOWN', 'j'):
                if self.selected_i < (len(self.widgets)-1):
                    self.selected_i += 1
            self.window_move = False
            return True

        if key == '\x17':
            self.window_move = True
        else:
            self.widgets[self.selected_i][1].key(key)

        return True

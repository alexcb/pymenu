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



kk = None
def _run(stdscr, widgets):
    window_move = False
    selected_i = 0
    while True:
        stdscr.clear()

        height, width = stdscr.getmaxyx()

        heights = _get_loc((x[0] for x in widgets), height)
        y = 0
        for i, (h, widget) in enumerate(zip(heights, (x[1] for x in widgets))):
            selected = bool(i == selected_i)
            widget.draw(stdscr, selected, 0, y, width, h)
            y += h

        stdscr.refresh()
        k = stdscr.getkey()
        if window_move:
            if k in ('KEY_UP', 'k'):
                if selected_i > 0:
                    selected_i -= 1
            elif k in ('KEY_DOWN', 'j'):
                if selected_i < (len(widgets)-1):
                    selected_i += 1
            window_move = False
        else:
            if k == '\x17':
                window_move = True
            else:
                widgets[selected_i][1].key(k)

def run(widgets):
    curses.wrapper(_run, widgets)


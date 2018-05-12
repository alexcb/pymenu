from blessed import Terminal
import sys

def format_cols(rows, total_width):
    if not rows:
        return rows

    cols = max(len(r) for r in rows)
    if cols != min(len(r) for r in rows):
        raise ValueError("not all rows have the same number of columns")

    widths = [
        max(len(r[i]) for r in rows)
        for i in range(cols)
        ]

    rows = [
        [x.ljust(w) for (x, w) in zip(row, widths)]
        for row in rows]

    rows = [' '.join(row) for row in rows]

    return rows

def menu(items, callback_func, selected = 0):
    t = Terminal()

    items = format_cols(items, t.width)

    func = None
    with t.fullscreen():
        while True:
            sys.stdout.write(t.clear() + t.move(0,0))
            num_rows = t.height - 1
            first_displayed_i = max(min(selected - 5, len(items) - num_rows), 0)
            for y in range(0, num_rows):
                i = y + first_displayed_i
                if i == selected:
                    sys.stdout.write(t.reverse)
                if i < len(items):
                    print(items[i])
                sys.stdout.write(t.normal)
            with t.cbreak():
                x = t.inkey()
                if repr(x) == 'KEY_UP':
                    selected = max(selected - 1, 0)
                elif repr(x) == 'KEY_DOWN':
                    selected = min(selected + 1, len(items) - 1)
                elif repr(x) == 'KEY_ENTER':
                    done = callback_func(selected)
                    if done:
                        return

def tabmenu(items, selected_tab = 0, selected_items = None):
    t = Terminal()

    if selected_items is None:
        selected_items = [0] * len(items)

    func = None
    with t.fullscreen():
        while True:
            sys.stdout.write(t.clear() + t.move(0,0))
            print(t.bold + items[selected_tab][0] + t.normal)

            tab_items = items[selected_tab][1]

            num_rows = t.height - 3
            first_displayed_i = max(min(selected_items[selected_tab] - 5, len(tab_items) - num_rows), 0)
            for y in range(0, num_rows):
                i = y + first_displayed_i
                if i == selected_items[selected_tab]:
                    sys.stdout.write(t.reverse)
                if i < len(tab_items):
                    print("%d. %s" % (y + first_displayed_i, tab_items[i]))
                sys.stdout.write(t.normal)
            with t.cbreak():
                x = t.inkey()
                if repr(x) == 'KEY_UP':
                    selected_items[selected_tab] = max(selected_items[selected_tab] - 1, 0)
                elif repr(x) == 'KEY_DOWN':
                    selected_items[selected_tab] = min(selected_items[selected_tab] + 1, len(tab_items) - 1)
                if repr(x) == 'KEY_LEFT':
                    selected_tab = max(selected_tab - 1, 0)
                elif repr(x) == 'KEY_RIGHT':
                    selected_tab = min(selected_tab + 1, len(items) - 1)
                elif repr(x) == 'KEY_ENTER':
                    return selected_tab, selected_items[selected_tab]


import os
import logging
import curses
import string

import pymenu.layout
import pymenu.table
import pymenu.dialog
import pymenu.form


class widget(object):
    def __init__(self, s):
        self.s = s
        self.k = ''

    def draw(self, stdscr, is_selected, x, y, width, height):
        for i in range(height):
            stdscr.addstr(y+i, x, '%s-%d-%s-%s' % (self.s, i, repr(self.k), is_selected))

    def cursor_loc(self, stdscr, x, y, width, height):
        return False

    def key(self, key):
        self.k = key


def cb(item):
    assert 0, str(item)

if __name__ == '__main__':
    logging.basicConfig(
        filename=os.path.expanduser('dialog.log'),
        level=logging.DEBUG,
        format="%(asctime)-15s %(message)s",
        )

    table1 = pymenu.table.TableWidget([
        (str(x), str(x*x), str(x*x*x)) for x in range(100)
        ], cb)

    layout = pymenu.layout.LayoutWidget((
        ('10%', table1),
        ('90%', widget('bottom')),
        ))

    form_widget = None
    dialog_widget = None
    def on_enter(vals):
        logging.info(repr(vals))
        form_widget.clear()
        dialog_widget.hide_dialog()

    form_widget = pymenu.form.FormWidget((
        {'label': 'title', 'value': 'hello'},
        {'label': 'description'},
        ), on_enter)

    dialog_widget = pymenu.dialog.DialogWidget(layout, dialog_widget=form_widget)

    pymenu.layout.run(dialog_widget)


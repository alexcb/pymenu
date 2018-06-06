import pymenu.layout
import pymenu.table

class widget(object):
    def __init__(self, s):
        self.s = s
        self.k = ''

    def draw(self, stdscr, is_selected, x, y, width, height):
        for i in range(height):
            stdscr.addstr(y+i, x, '%s-%d-%s-%s' % (self.s, i, repr(self.k), is_selected))

    def key(self, key):
        self.k = key


def cb(item):
    assert 0, str(item)

table1 = pymenu.table.TableWidget([
    (str(x), str(x*x), str(x*x*x)) for x in range(100)
    ], cb)

widget = pymenu.layout.LayoutWidget((
    ('10%', table1),
    ('90%', widget('bottom')),
    ))

pymenu.layout.run(widget)

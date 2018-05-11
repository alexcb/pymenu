from pymenu.menu import menu

# Press left/right to navigate between foo/bar menus
# up/down between items
x = [
    ('foo', [1,2,3,4]),
    ('bar', ['aa', 'bb', 'cc']),
    ]

foo = None
def on_enter(selected):
    global foo
    foo =  selected
    return True
menu(x, on_enter)

print(foo)


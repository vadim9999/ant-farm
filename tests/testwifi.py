from wifi import Cell, Scheme

cell = Cell.all('wlan0')[3]
scheme = Scheme.for_cell('wlan0', 'home', cell, 'Loader$5')
scheme.save()
scheme.activate()

print(list(cell))
import os
import django 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hecs.settings")
django.setup()
from themes.models import *
import csv

def write_theme(name, x, y, color):
    if not name:
        return 0
    theme = Theme(name=name, x=x, y=y, color=color)
    theme.save()
    return 1
    
def fill(csv_filename):
 
    csvfile = open(csv_filename)
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    data = {}
    color = [[None] * 40 for i in range(40)]
    text = [[None] * 40 for i in range(40)]

    X_OFFSET = 12
    Y_OFFSET = 9 

    for row in csvreader:
        if row[14]:
            color[int(row[14]) - X_OFFSET][int(row[15]) - Y_OFFSET] = row[17]
            text[int(row[14]) - X_OFFSET][int(row[15]) - Y_OFFSET] = row[1]
        if row[0] and row[0] != '-':
            if row[0] not in data:
                data[row[0]] = {1: [], 2: [], 3:[]}
            if row[2]:
                data[row[0]][1] += [(1, row[2], row[3] or row[1])]
            if row[4]:
                data[row[0]][3] += [(2, row[4], row[5] or row[1])]
            if row[7]:
                data[row[0]][3] += [(3, row[7], row[8] or row[1])]
            if row[9]:
                data[row[0]][2] += [(3, row[9], row[10] or row[1])]
            if row[12]:
                data[row[0]][2] += [(4, row[12], row[13] or row[1])]
            if row[18]:
                data[row[0]][3] += [(5, row[18], row[19] or row[1])]

            if row[14]:
                data[row[0]]['id'] = (int(row[14]) - X_OFFSET, int(row[15]) - Y_OFFSET)
    
    print('Filling themes')
    
    ctr = 0
    Theme.objects.all().delete()
    Reference.objects.all().delete()
    for x in range(10):
        for y in range(16):
            ctr += write_theme(text[x][y], x, y, color[x][y])
            
    print(ctr, 'themes filled')
    print('Filling references')
    ctr = 0
    for key, value in data.items():
        if 'id' not in data[key]:
            continue
        theme = Theme.objects.filter(x=data[key]['id'][0]).filter(y=data[key]['id'][1]).get()
        for section in [1, 2, 3]:
            if data[key][section]:
                for line in data[key][section]:
                    ref = Reference(theme=theme, group_id=section, target_id=line[0], name=line[2], href=line[1])
                    ref.save()
                    ctr += 1
    
    print(ctr, 'references filled')
            
if __name__ == '__main__':
    fill('hecs.csv')
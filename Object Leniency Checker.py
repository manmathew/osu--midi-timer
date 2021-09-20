# Import modules needed
import math
from guizero import App, Text, PushButton, TextBox, Picture

# Input the OD value so the map can be checked for leniency problems
#accuracy = float(input("Please enter the OD that will be primarily played (if DT then calculate the OD after applying DT): "))

done = 0

# Calculating the ms leniency of a hitobject
def equation(od):
    acc = float(79.5 - 6 * od)
    return acc

# .osu file list
def file_create(path):
    file_list = []
    f = open(path, 'r')
    a = 0
    data = f.readlines()
    num_lines = sum(1 for line in open(path))
    while a < num_lines:
        data1 = data[a].split(',')
        b = 0
        data2 = []
        while b < len(data1):
            data2.append(data1[b])
            b += 1
        file_list.append(data2)
        a += 1
    #print(file_list)
    f.close()
    return file_list

# Getting the start and end points of sections
def list_nums(bound1, bound2, bound3, bound4):
    
    # the A numbers are for the start and end of the "Timing Point" Section
    # the B numbers are for the start and end of the "Hit Object" Section
    a1 = bound1
    a2 = bound2
    b1 = bound3
    b2 = bound4
    a2 = a2 - 4
    return [a1, a2, b1, b2]

# Creating a list of all the object timing point locations that need attention
def find_bad(list1, list2, od):
    combine = []
    temp = []
    o = 0
    while o < len(list2):
        t = 0
        e = 0
        while e < 1:
            if list2[o] > list1[t][0]:
                t += 1
            else:
                t -= 1
                e = 2
        temp = [list2[o], list1[t][0], (60000 / (list1[t][1] * 4))]
        combine.append(temp)
        o += 1
    
    bad = []
    a = 0
    while a < len(combine):
        dif = combine[a][0] - combine[a][1]
        a1 = 0
        e1 = 0
        while e1 < 1:
            mat = combine[a][2] * a1
            if mat < dif:
                a1 += 1
            else:
                e1 = 2
        if abs(mat - dif) < od:
            a += 1
        else:
            bad.append(combine[a][0])
            a += 1
    return bad

# Create the list that gets input into the find_bad function
def list_create(file_list, bounds):
    time_points = []
    object = []
    a1 = bounds[0]
    a2 = bounds[2]
    while a1 < bounds[1]:
        line = file_list[a1]
        if len(line) > 4:
            if line[6] == '1':
                temp = [float(line[0]), round((60000 / float(line[1])), 3)]
                time_points.append(temp)
                a1 += 1
            else:
                a1 += 1
        else:
            a1 += 1
    while a2 < bounds[3]:
        line = file_list[a2]
        object.append(float(line[2]))
        a2 += 1
    return time_points, object

# Write to a file the object locations that have objects with leniency problems
def write_points(bad, path):
    file_path = path + 'export.txt'
    f = open(file_path, 'w')
    i = 0
    sec = 0
    min = 0
    f.write('[Locations with questionable leniency]\n')
    while i < len(bad):
        stri = bad[i] / 1000
        if stri >= 60:
            sec = stri % 60
            min = round(stri/60)
        else:
            sec = stri
        stri = str(min) + ':' + str(sec)
        strin = stri + "'\n"
        f.write(strin)
        i += 1
    text.show()
    message.show()

# Spliting list_create into 2 outputs
def list_fix1(couple):
    output = couple[0]
    return output

def list_fix2(couple):
    output = couple[1]
    return output

def strip(path):
    data = path.split('/')
    data.pop()
    a = 0
    new_path = ''
    while a < len(data):
        new_path = new_path + str(data[a]) + '/'
        a += 1
    return new_path

def execute(path, accuracy, bound1, bound2, bound3, bound4):
    stripped_path = strip(path)
    cup = list_create(file_create(path), list_nums(bound1, bound2, bound3, bound4))
    write_points(find_bad(list_fix1(cup), list_fix2(cup), accuracy), stripped_path)

#execute(8, 54, 3230, 3236, 5220)

# GUI APPLICATION CODE
app = App(title="Object Leniency Checker", height=500, width=500, bg="white")
app.icon = '/Users/constantin/Documents/visual/(midi timing) src/full_icon_len.png'

message = Text(app, text="")
message = Text(app, text="Make a copy of the '.osu' file and rename the extension to '.txt'")

def start():
    path = str(input_box_file.value)

    number0 = 0
    try:
        number0 = int(input_box_acc.value)
    except ValueError:
        print('invalid number')

    number1 = 0
    try:
        number1 = int(input_box_time.value)
    except ValueError:
        print('invalid number')

    number2 = 0
    try:
        number2 = int(input_box_colours.value)
    except ValueError:
        print('invalid number')

    number3 = 0
    try:
        number3 = int(input_box_hit.value)
    except ValueError:
        print('invalid number')

    number4 = 0
    try:
        number4 = int(input_box_last.value)
    except ValueError:
        print('invalid number')
    
    execute(path, number0, number1, number2, number3, number4)

message = Text(app, text="Enter the path of the '.txt' file")
input_box_file = TextBox(app, width=50)
input_box_file.text_color = 'black'

message = Text(app, text="Enter the OD of the beatmap")
input_box_acc = TextBox(app)
input_box_acc.text_color = 'black'

message = Text(app, text="Enter the line number that [TimingPoints] is on")
input_box_time = TextBox(app)
input_box_time.text_color = 'black'

message = Text(app, text="Enter the line number that [Colours] is on")
input_box_colours = TextBox(app)
input_box_colours.text_color = 'black'

message = Text(app, text="Enter the line number that [HitObjects] is on")
input_box_hit = TextBox(app)
input_box_hit.text_color = 'black'

message = Text(app, text="Enter the line number with the last hit object")
input_box_last = TextBox(app)
input_box_last.text_color = 'black'

#execute(number1, 0, 0, 0, 0)

message = Text(app, text="Press the button to start the program")
button = PushButton(app, text="Start!", command=start, args=[])

text = Text(app, text="Done!", size=24)
text.hide()
message = Text(app, text="The output file will be called 'export.txt' and is in the same folder as the imported file")
message.hide()

app.display()

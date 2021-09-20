# Modules to import
from mido import MidiFile
from guizero import App, Text, PushButton, TextBox, Picture

# Reads the midi files and returns a list of strings with each being a midi event
def readAndPrint(path):
    mid = MidiFile(path)
    list = []
    for i, track in enumerate(mid.tracks):
        #print('Track {}: {}'.format(i, track.name))
        for msg in track:
            #print(msg)
            list.append(str(msg))
    list_final = []
    a = 4
    f = len(list)
    f -= 1
    while a < f:
        list_final.append(list[a])
        a += 1
    return list_final

# Class for the notes to make creating the final list easier
class note:
    def __init__(self):
        self.time = 0
        self.type = 0

# Creates a list of class objects with the integer values needed
def list_create(string_list):
    temp_string = ''
    temp_list = []
    final_list = []
    a = 0
    temp_time = 0
    temps = []
    i = 0
    while i < len(string_list):
        str = ''
        str = note()
        temps.append(str)
        i += 1
    while a < len(string_list):
        temp_list.append(string_list[a].split('time=')[-1])
        temp_time = int(temp_list[-1])
        temps[a].time = temp_time
        if string_list[a][6] == 'n':
            temps[a].type = 0
        else:
            temps[a].type = 1
        final_list.append(temps[a])
        a += 1
    return final_list

# Creates a list of all the ticks with notes (when the notes start only)
def final_list_create(input_list):
    overall = 0
    a = 0
    final = []

    while a < len(input_list):
        if input_list[a].type == 0:
            overall = overall + input_list[a].time
            final.append(overall)
            a += 1
        else:
            overall = overall + input_list[a].time
            a += 1
    
    return final

# Removes all the duplicate points
def remove_dupes(list):
    res = []
    [res.append(x) for x in list if x not in res]
    return res

# Converts ticks to milliseconds
def tick_ms(list, bpm):
    ms = []
    bpm_tick = (6 * 10**7) / bpm
    temp_tick = 0
    temp_ms = 0
    a = 0
    while a < len(list):
        temp_tick = list[a]
        temp_ms = temp_tick * bpm_tick / 96000
        ms.append(temp_ms)
        a += 1
    return ms

# Function importing two time stamps and calculating BPM.
def point2(p1, p2, bpm_old, pOriginal, s2, s4):
    diff = p2 - p1
    bpm_new = 0
    snap = 0

    # If statement for 1/4s
    if diff < 100:
        bpm_new = round(15 * (1 / (diff / 1000)), 3)
        snap = 4
    
    # If statement for 1/2s
    else:
        bpm_new = round(30 * (1 / (diff / 1000)), 3)
        snap = 2
    
    # If statement increasing old bpm snaps
    if snap == 2:
        s2 += 1
    else:
        s4 += 1

    # Comparing BPMs to decide if it's necessary and returning tuple with offset, bpm, and true/false
    if compare_BPM(bpm_old, pOriginal, p2, s2, s4) == 'false':
        return (p1, bpm_old, 'false', pOriginal, s2, s4)
    else:
        pOriginal = p1
        if snap == 2:
            s2 = 1
            s4 = 0
        else:
            s2 = 0
            s4 = 1
        return (p1, bpm_new, 'true', pOriginal, s2, s4)
    
def compare_BPM(bpm1, pOriginal, p2, s2, s4):
    len2 = p2 - pOriginal

    len1 = (round(1000 * (60 / bpm1 * 4)) * s4) + (round(1000 * (60 / bpm1 * 2)) * s2)
    
    diff = len2 - len1

    # False is no need for a new timing point
    # True is yes create a new timing point
    if diff in range(-10, 11):
        return 'false'
    else:
        return 'true'

# Class that is for the timing points in the final list
class Point:
    def __init__(self):
        self.offset = 0
        self.bpm = float(0)
        self.num = 'None'

# Function using the list from midi import and creating a list with all the BPMs and offsets
def createList(lis, first):
    final = []
    i = 0
    old = 1
    pOriginal = first
    s2 = 0
    s4 = 0

    while i < (len(lis) - 1):
        apps = Point()
        tup = point2(lis[i] + first, lis[i + 1] + first, old, pOriginal, s2, s4)
        pOriginal = tup[3]
        s2 = tup[4]
        s4 = tup[5]
        if tup[2] == 'true':
            apps.offset = tup[0]
            apps.bpm = tup[1]
            apps.num = str(i)
            final.append(apps)
            i += 1

        else:
            i += 1

        old = tup[1]

    return final

# Function calculating the bpm number for the .osu file
def calc(bpm):
    num = round((60000 / bpm), 12)
    return num

# Function writing to the .txt file
def writeFile(lis, path):
    path_final = path + 'points.txt'
    f = open(path_final, 'w')
    i = 0
    f.write('[TimingPoints]\n')
    while i < len(lis):
        bpm = calc(lis[i].bpm)
        temp = ''
        temp = temp + str(lis[i].offset) + ',' + str(bpm) + ',4,2,1,100,1,0\n'
        f.write(temp)
        i += 1

def strip(path):
    data = path.split('/')
    data.pop()
    a = 0
    new_path = ''
    while a < len(data):
        new_path = new_path + str(data[a]) + '/'
        a += 1
    return new_path

# Executing the actual program
def run_file(first, path, bpm):
    list = tick_ms(remove_dupes(final_list_create(list_create(readAndPrint(path)))), bpm)
    writeFile(createList(list, first), strip(path))
    message.show()
    text.show()

#run_file()

# GUI CODE
# CAN BE MOVED TO ANOTHER .PY FILE EVENTUALLY
# TOO LAZY TO USE MULTIPLE .PY FILES RIGHT NOW

app = App(title="midi osu! timer", height=500, width=500, bg="white")
app.icon = '/Users/constantin/Documents/visual/(midi timing) src/full_icon_time.png'

message = Text(app, text="")
message = Text(app, text="Enter below the full path of the .midi file")
input_box_midi = TextBox(app, width=50)
input_box_midi.text_color = 'black'

message = Text(app, text="Enter below the offset of the first timing point")
input_box_first = TextBox(app)
input_box_first.text_color = 'black'

message = Text(app, text="")

message = Text(app, text="Enter below the bpm that the midii file was recorded at")
input_box_bpm = TextBox(app)
input_box_bpm.text_color = 'black'

message = Text(app, text="")

picture = Picture(app, image="/Users/constantin/Documents/visual/(midi timing) src/midi_pic.png")

def start():
    path = str(input_box_midi.value)

    number0 = 0
    try:
        number0 = int(input_box_first.value)
    except ValueError:
        print('invalid number')
    
    number1 = 0
    try:
        number1 = int(input_box_bpm.value)
    except ValueError:
        print('invalid number')

    run_file(number0, path, number1)

message = Text(app, text="Click 'Start' to start the timing process")
message = Text(app, text="")
button = PushButton(app, text="Start", command=start, args=[])

text = Text(app, text="Done!", size=24)
text.hide()
message = Text(app, text="The output file will be called 'points.txt' and is in the same folder as the imported file")
message.hide()

app.display()

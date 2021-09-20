#import mido
from mido import MidiFile

# Reads the midi files and returns a list of strings with each being a midi event
def readAndPrint():
    name = input("Enter the name of the .midi file: ")
    mid = MidiFile(name)
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

print(remove_dupes(final_list_create(list_create(readAndPrint()))))

# Python file that has the timing algorithm
'''
take first two points calculate bpm
then see if it still lines up with the next note within 10ms
if yes then repeat for next note
if no then set that as the bpm and start over with the next pair (point 2 becomes point 1 and the 3rd point beocmes point 2)
if it is no after it has been yes then we set the last yes point as point 1 and the no index as point 2

to make sure that we don't have a problem with searching for notes that don't exist at the end of the list
have the following variables:

i for the index of point1
n for the index of the furthest point being looked at CURRENTLY (so all the i+1s are just going to be n)
a for the difference between the length of the list and the index of n

if n becomes 1 before searching for the index then start over with the next i
if length - i becomes zero then exit the loop and return the list of bpms and their respective time
'''
def calculate_bpm(difference, snap):
    bpm = float(60000 / (difference * snap))
    return bpm

def snapping(difference):
    if difference < 101:
        snap = 4
    elif difference < 201:
        snap = 2
    else:
        snap = 1
    return snap

def differing(point_a, point_b):
    difference = point_b - point_a
    return difference

def multiple(point_a, point_b, difference):
    coef = 1
    diff1 = difference
    diff2 = differing(point_a, point_b)
    coef = round(diff2/diff1)
    return coef

def check_close(diff_initial, diff_current, coef):
    diff1 = diff_initial * coef
    diff_of_diffs = differing(diff1, diff_current)
    if abs(diff_of_diffs) < 11:
        return True
    else:
        return False

def snap4_point_check(list, index):
    i = index
    n = i + 1
    diff1 = differing(list[i], list[n])
    snap = 4
    bpm = calculate_bpm(diff1, snap)
    n += 1
    a = len(list) - n

    while a > 0:
        # enter snap diff stuff for other functions
        coef = multiple(list[i], list[n], diff1)
        diff2 = differing(list[i], list[n])
        if check_close(diff1, diff2, coef) == True:
            n += 1
            a = len(list) - n
        else:
            break
    n -= 1

    return (bpm, index, n) #return bpm, index of first point maybe, index of last point bpm is a yes for

def snap2_point_check(list, index):
    i = index
    n = i + 1
    diff1 = differing(list[i], list[n])
    snap = 2
    bpm = calculate_bpm(diff1, snap)
    n += 1
    a = len(list) - n
    diff2 = diff1 / 2

    while a > 0:
        # enter snap diff stuff for other functions
        coef = multiple(list[i], list[n], diff2)
        diff3 = differing(list[i], list[n])
        if check_close(diff2, diff3, coef) == True:
            n += 1
            a = len(list) - n
        else:
            break
    n -= 1

    return (bpm, index, n) #return bpm, index of first point maybe, index of last point bpm is a yes for

def snap1_point_check(list, index):
    i = index
    n = i + 1
    diff1 = differing(list[i], list[n])
    snap = 1
    bpm = calculate_bpm(diff1, snap)
    n += 1
    a = len(list) - n
    diff2 = diff1 / 4

    while a > 0:
        # enter snap diff stuff for other functions
        coef = multiple(list[i], list[n], diff2)
        diff3 = differing(list[i], list[n])
        if check_close(diff2, diff3, coef) == True:
            n += 1
            a = len(list) - n
        else:
            break
    n -= 1

    return (bpm, index, n) #return bpm, index of first point maybe, index of last point bpm is a yes for

def go_through_list(list):
    i = 0
    list2 = []

    while (i + 1) < len(list):
        point_a = list[i]
        point_b = list[i+1]
        snap = snapping(differing(point_a, point_b))
        
        if snap == 4:
            couple1 = snap4_point_check(list, i)
        elif snap == 2:
            couple1 = snap2_point_check(list, i)
        else:
            couple1 = snap1_point_check(list, i)
       
        couple2 = (couple1[0], list[couple1[1]])
        list2.append(couple2)
        i = couple1[2]

    return list2

# midi osu timer
 
 An application that will time mp3's based on the .midi file that is recorded along-side the audio.

 ## How to use it
-Open the .midi file you want to time

-Enter the offset of the first note (yes you have to find that yourself in the osu! editor)

-Enter the bpm that the .midi file was recorded at

-If you don't know, the default is 120bpm

-Save a .txt file you want the timing points to be saved in.

-Click the start button and wait for the text "Done!" to appear.

### Requirements
If you are executing the .py file, you will need to install [mido](https://mido.readthedocs.io/) and [guizero](https://lawsie.github.io/guizero/).

Guizero is only used for the graphical interface, so if you don't want to install guizero, you can change the start() function so that it gets input from the terminal. 

Note that the .py file is currently set up to accept file paths for MacOS and Linux.

If you want to use full file paths in windows, change lines 196 and 201 to have '\\' instead of '/'

## Installation
Either download the executable or download the source code and run the 'midi osu! timer.py' file after installing the mido and guizero modules.

If you download the source code, don't download from release (it's outdated and I can't fix it).

### Executables
Windows Executable has been made!

Debian and Mac binaries will come eventually.

### Future Updates
I plan on continuing to work on this program to get all the executables compiled, to use more beat snapping dividers, and also to reduce unnecessary timing points.

I'll write here if I ever stop working on this project, and you are free to make your own branch of this repository.

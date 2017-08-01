# QuickAccess for Python
Convenient program that makes launching personal programs super quick.
### How to Use
Using this is very easy. If you have a Python program that can be launched from the command line, a program that cmd can launch by "start", or an executable,
it can be added to QuickAccess! All you must do is make a copy of `exampleConfig.yaml`, rename it as `config.yaml` and add the
entry you would like. For example, if you have a program called "Hey There", and it is
usually run by going to your documents and running `hey_there.py`, just do
`Hey There: C:\Users\username\Documents\hey_there.py` in the yaml file. This will tell
QuickAccess to add a button to the GUI titled "Hey There", and when clicked, run `hey_there.py` in
the documents folder.

Sometimes, I get frustrated when I accidently close a command prompt when I want to restart a program,
or having to open multiple command prompt tabs or windows to run different programs. That's why I
made this simple program, so that all of the programs I want to run are laid out in front of me as
buttons that, when clicked, runs the program right away.

If you think of anything else to add, feel free to contribute. I want to make it so it can do any
program that is executable from the command prompt. I could easily make it so that in the yaml, you
put the necessary command but that takes away from the user friendly aspect.

I will probably make it look nicer in the future, this is just a small idea I had.
I might make it so that you can add programs to QuickAccess via the GUI rather than having
to manually add them into the yaml file. This obviously would make it much easier to use for
people who aren't familiar with configuration files and stuff like that.

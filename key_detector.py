# KeyLogger_tk2.py
# show a character key when pressed without using Enter key
# hide the Tkinter GUI window, only console shows
# KeyLogger_tk2.py taken from DaniWeb forum and addapted


class moving_by_keys():
    '''Object which detects a key press.'''

    def __init__(self):
        '''Initializes a global variable to detect and store the key
        pressed.'''
        self.temp = None
        import Tkinter as tk

        def key(event):
            '''Helper function which detects the key pressed by the user.'''
            if event.char == event.keysym:
                self.temp = event.char
                root.destroy()
            elif len(event.char) == 1:
                self.temp = (event.keysym, event.char)
                root.destroy()
            else:
                self.temp = (event.keysym)
                root.destroy()

        root = tk.Tk()
        root.focus_force()
        root.bind('<Key>', key)
        # don't show the tk window
        root.mainloop()
        self.key = self.temp


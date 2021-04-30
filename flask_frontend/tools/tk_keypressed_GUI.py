import tkinter as tk
import time

print("### Start listening to press event ###")

fo = open("press.txt", "a")
def onKeyPress(event):
    text.insert('end', 'You pressed %s\n' % (event.char, ))
    print('%s\tYou pressed %s\n' % (time.time(),event.char, ))
    fo.write(str(time.time()))

root = tk.Tk()
root.geometry('300x200')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', onKeyPress)
root.mainloop()

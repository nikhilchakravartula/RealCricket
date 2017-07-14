import tkinter as tk
import threading
import _thread
# class Application(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.pack()
#         self.create_widgets()

#     def create_widgets(self):
#         self.hi_there = tk.Button(self)
#         self.hi_there["text"] = "Hello World\n(click me)"
#         self.hi_there["command"] = self.say_hi
#         self.hi_there.pack(side="top")

#         self.quit = tk.Button(self, text="QUIT", fg="red",
#                               command=root.destroy)
#         self.quit.pack(side="bottom")

#     def say_hi(self):
#         print("hi there, everyone!")


def parallel_display(thread_name, window_object):
    try:
        print(type(window_object))
        window_object.mainloop()
    except Exception as e:
        var = e.__traceback__
        print(var)


class notification_list():
    def __init__(self):
        self._list = []
        self._display_list = []
        self._nw_width = 350
        self._nw_height = 60

    def generate_notification(self, title, message):
        window = self._create_notification_window(title, message)
        self._list.append(window)
        if len(self._display_list) < 3:
            self._display_notification()


    def _display_control(self):
        flag = True
        displayref_x = -1
        displayref_y = -1
        for idx, window in enumerate(self._display_list):
            print("index ",idx)
            if flag:
                displayref_x = window[0].winfo_screenwidth() - (self._nw_width + 30)
                displayref_y = window[0].winfo_screenheight() - (self._nw_height + 100)
                flag = False
            #window[0].setposition()
            window[0].geometry("%dx%d+%d+%d" % (self._nw_width, self._nw_height, displayref_x, displayref_y))
            if not window[1]:
                # th = threading.Thread(target=parallel_display(window[0]))
                # th.start()
                try:
                    _thread.start_new_thread(parallel_display, ("Thread", window[0]))
                except:
                    print("Exception in Thread")
                self._display_list[idx] = (window[0], True)
            displayref_y -= (displayref_y + 10)
    
    def _display_notification(self):
        while len(self._list) > 0:
            if len(self._display_list) >= 2:
                continue
            self._display_list.append((self._list[0], False))
            self._display_control()
            del self._list[0]


    def _create_notification_window(self, title, message):
        window = tk.Tk()
        window.attributes("-toolwindow", 1)
        window.title(title)
        label = tk.Label(window, text=message)
        label.pack()
        label.place(x=10, y=10)
        window.resizable(False, False)
        return window


if __name__ == "__main__":
    # app = create_notification_window("title", "message")
    # app.mainloop()
    nl = notification_list()
    nl.generate_notification("title", "message")
    nl.generate_notification("title1", "message1")
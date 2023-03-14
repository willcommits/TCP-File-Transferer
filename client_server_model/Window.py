import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
import socket
import hashlib

IP = socket.gethostname()

Port = 7700
ADDR = (IP, Port)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
folder_path = ""


class MainWindow(tk.Tk):
    response = ""
    file_name = ""
    email = ""
    password = ""
    command = ""
    filepath = ""
    file_list = []
    listbox = ""
    folder_path = ""
    selected_file = ""
    combo_items = ""
    logged_email = ""
    logged_data = 0

    # create constructor and setting values to the instance variables creating the initial screen
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title('Main Window')
        self.geometry('200x200')

        # Add a button to switch to window 1
        self.button1 = tk.Button(self, text='UPLOAD', command=self.open_window1)
        self.button1.pack(pady=10)
        # Add a button to switch to window 3
        self.button3 = tk.Button(self, text='DELETE', command=self.open_window3)
        self.button3.pack()
        # Add a button to switch to window 2
        self.button2 = tk.Button(self, text='DOWNLOAD', command=self.open_window2)
        self.button2.pack(pady=10)

        self.button4 = tk.Button(self, text='Help', command=self.Client_Help)
        self.button4.pack(pady=10)

    # creates the Uploader window
    def open_window1(self):
        self.withdraw()  # Hide the main window

        # Create window 1
        self.window1 = tk.Toplevel(self)
        self.window1.title('File Uploader')
        self.window1.geometry('500x300')

        # Add a button to switch back to the main window

        panelframe = tk.Frame(self.window1)
        panelframe.columnconfigure(0, weight=1)
        panelframe.columnconfigure(1, weight=1)

        label_email = tk.Label(panelframe, text="Email: ", font=("Times New Roman", 16))
        label_email.grid(row=0, column=0, padx=10, pady=10, sticky="wn")
        textbox_email = tk.Entry(panelframe, font=("Times New Roman", 16))
        textbox_email.grid(row=0, column=1, padx=10, pady=10, sticky="wn")
        MainWindow.email = textbox_email

        label_password = tk.Label(panelframe, text="Password: ", font=("Times New Roman", 16))
        label_password.grid(row=1, column=0, padx=10, pady=10, sticky="wn")
        textbox_password = tk.Entry(panelframe, font=("Times New Roman", 16))
        textbox_password.grid(row=1, column=1, padx=10, pady=10, sticky="wn")
        MainWindow.password = textbox_password

        options = ["N/A", "Encrypt"]

        # Create a Combobox widget
        label_password = tk.Label(panelframe, text="Format File: ", font=("Times New Roman", 16))
        label_password.grid(row=2, column=0, padx=10, pady=10, sticky="wn")
        combo_box = ttk.Combobox(panelframe, values=options)
        combo_box.current(0)
        combo_box.grid(row=2, column=1, padx=10, pady=10)
        MainWindow.combo_items = combo_box

        label_Command = tk.Label(panelframe, text="Section to Upload: ", font=("Times New Roman", 16))
        label_Command.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

        btn_upload = tk.Button(panelframe, text="UPLOAD(^)", command=self.Upload, font=("Times New Roman", 16))
        btn_upload.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        button = tk.Button(panelframe, text='Back to Main', command=self.back_to_main)
        button.grid(row=5, column=2, pady=10)

        panelframe.pack()

    # creates window that allows user to download files
    def open_window2(self):
        self.withdraw()  # Hide the main window

        # Create window 2
        self.window2 = tk.Toplevel(self)
        self.window2.title('DOWNLOAD')
        self.window2.geometry('500x600')

        # Add a button to switch back to the main window

        panelframe = tk.Frame(self.window2)
        panelframe.columnconfigure(0, weight=1)
        panelframe.columnconfigure(1, weight=1)

        label_email = tk.Label(panelframe, text="Email: ", font=("Times New Roman", 16))
        label_email.grid(row=0, column=0, padx=10, pady=10, sticky="wn")
        textbox_email = tk.Entry(panelframe, font=("Times New Roman", 16))
        textbox_email.grid(row=0, column=1, padx=10, pady=10, sticky="wn")
        MainWindow.email = textbox_email

        label_password = tk.Label(panelframe, text="Password: ", font=("Times New Roman", 16))
        label_password.grid(row=1, column=0, padx=10, pady=10, sticky="wn")
        textbox_password = tk.Entry(panelframe, font=("Times New Roman", 16))
        textbox_password.grid(row=1, column=1, padx=10, pady=10, sticky="wn")
        MainWindow.password = textbox_password

        btn_upload = tk.Button(panelframe, text="Load Items", command=self.Load_Items, font=("Times New Roman", 16))
        btn_upload.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        btn_upload = tk.Button(panelframe, text="Select Folder", command=self.Load_Folder, font=("Times New Roman", 16))
        btn_upload.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        label_password = tk.Label(panelframe, text="Select File To Download ", font=("Times New Roman", 16))
        label_password.grid(row=4, column=1, padx=10, pady=10, sticky="wn")
        MainWindow.listbox = tk.Listbox(panelframe)
        MainWindow.listbox.grid(row=5, column=1, pady=10)

        btn_upload = tk.Button(panelframe, text="DOWNLOAD", command=self.Download_File, font=("Times New Roman", 16))
        btn_upload.grid(row=6, column=0, padx=10, pady=10, columnspan=2)

        button = tk.Button(panelframe, text='Back to Main', command=self.back_to_main)
        button.grid(row=7, column=2, columnspan=2, pady=10)

        panelframe.pack()

    # Creates window that allows user to be able to search and delete something
    def open_window3(self):
        self.withdraw()  # Hide the main window

        # Create window 3
        self.window3 = tk.Toplevel(self)
        self.window3.title('DELETE')
        self.window3.geometry('500x230')

        # Add a button to switch back to the main window

        panelframe = tk.Frame(self.window3)
        panelframe.columnconfigure(0, weight=1)
        panelframe.columnconfigure(1, weight=1)

        label_email = tk.Label(panelframe, text="File to Delete: ", font=("Times New Roman", 16))
        label_email.grid(row=0, column=1, padx=10, pady=10, sticky="wn", columnspan=2)

        label_email = tk.Label(panelframe, text="Name: ", font=("Times New Roman", 16))
        label_email.grid(row=1, column=0, padx=10, pady=10, sticky="wn")
        textbox_email = tk.Entry(panelframe, font=("Times New Roman", 16))
        textbox_email.grid(row=1, column=1, padx=10, pady=10, sticky="wn")
        MainWindow.email = textbox_email

        btn_upload = tk.Button(panelframe, text="DELETE(-)", command=self.Delete_File, font=("Times New Roman", 16))
        btn_upload.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        button = tk.Button(panelframe, text='Back to Main', command=self.back_to_main)
        button.grid(row=3, column=2, pady=10)

        panelframe.pack()

    # Gets the folder path we want to download our file to
    def Load_Folder(self):
        MainWindow.folder_path = filedialog.askdirectory()

    # Downloads file and extract all the details supplied by user before Downloading File
    def Download_File(self):
        selection = MainWindow.listbox.curselection()
        if selection:
            index = selection[0]
            item = MainWindow.listbox.get(index)
            MainWindow.selected_file = item

        if (len(MainWindow.folder_path) == 0):
            messagebox.showinfo("Requirement!", "Please Select Folder Path")
        elif (MainWindow.selected_file == ""):
            messagebox.showinfo("Requirement!", "Please Select a file")

        else:

            if (MainWindow.selected_file.find("decrypted") != -1):
                MainWindow.main(MainWindow.email.get(), MainWindow.password.get(), MainWindow.selected_file,
                                MainWindow.folder_path, "D", "DOWNLOAD")
            else:
                MainWindow.main(MainWindow.email.get(), MainWindow.password.get(), MainWindow.selected_file,
                                MainWindow.folder_path, "DOWNLOAD")
            messagebox.showinfo("Server Response", f"{MainWindow.response}")  # Display the message box

    # This method is responsible for locating a file in your computer system and uploading it to the server
    def Upload(self):
        if (len(MainWindow.email.get()) == 0):
            MainWindow.email.config(bg="red")
        if (len(MainWindow.password.get()) == 0):
            MainWindow.password.config(bg="red")
        elif ((len(MainWindow.email.get()) == 0)) and (len(MainWindow.password.get()) >= 1):
            MainWindow.email.config(bg="red")
            MainWindow.password.config(bg="white")
        elif ((len(MainWindow.email.get()) >= 1)) and (len(MainWindow.password.get()) == 0):
            MainWindow.email.config(bg="white")
            MainWindow.password.config(bg="red")
        elif (len(MainWindow.email.get()) >= 1) and (len(MainWindow.password.get()) >= 1):

            selected_value = MainWindow.combo_items.get()
            print(selected_value)
            MainWindow.email.config(bg="white")
            MainWindow.password.config(bg="white")
            self.window1.deiconify()
            file_path = filedialog.askopenfilename()
            MainWindow.main(MainWindow.email.get(), MainWindow.password.get(), selected_value, file_path, "UPLOAD")
            messagebox.showinfo("Server Response", f"{MainWindow.response}")  # Display the message box

    # List all public and private files of the current user in the server to a listbox
    def Load_Items(self):
        MainWindow.listbox.delete(0, tk.END)
        if (len(MainWindow.email.get()) == 0):
            MainWindow.email.config(bg="red")
        if (len(MainWindow.password.get()) == 0):
            MainWindow.password.config(bg="red")
        elif ((len(MainWindow.email.get()) == 0)) and (len(MainWindow.password.get()) >= 1):
            MainWindow.email.config(bg="red")
            MainWindow.password.config(bg="white")
        elif ((len(MainWindow.email.get()) >= 1)) and (len(MainWindow.password.get()) == 0):
            MainWindow.email.config(bg="white")
            MainWindow.password.config(bg="red")
        elif (len(MainWindow.email.get()) >= 1) and (len(MainWindow.password.get()) >= 1):
            MainWindow.email.config(bg="white")
            MainWindow.password.config(bg="white")
            MainWindow.logged_email = MainWindow.email.get()
            MainWindow.main(MainWindow.email.get(), MainWindow.password.get(), "LIST")
            MainWindow.file_list = MainWindow.response.split("\n")
            count = 0
            for i in MainWindow.file_list:
                MainWindow.listbox.insert(count, i)
                count += 1
            MainWindow.logged_data = count

    # Deletes a file from the server based of the users input
    def Delete_File(self):
        """Uses the name supplied by the user to search for the file in the server and delete it"""
        if (len(MainWindow.email.get()) == 0):
            MainWindow.email.config(bg="red")
        else:
            MainWindow.email.config(bg="white")
            MainWindow.main(MainWindow.email.get(), "DELETE")
            messagebox.showinfo("Server Response", f"{MainWindow.response}")

        # allows us to switch to the main screen

    # Returns help prompts to users to allow users to be able to get a description of how things work
    def Client_Help(self):
        MainWindow.main("HELP")
        messagebox.showinfo("Server Response", f"{MainWindow.response}")

    # takes you back to the main window
    def back_to_main(self):
        # Destroy the current window and show the main window
        self.destroy()
        self.__init__()

    """ This function defines all the functionality of the application, if Help is passed it shows all
   help options
   if Download it allows user to download
   if Upload allows user to upload files
   if list returns a list of files on the server
   """

    @staticmethod
    def main(*client_details):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        # connect with server
        count = 0

        while True:
            count += 1
            data = client.recv(SIZE).decode()
            cmd, msg = data.split("@")
            if (
                    cmd == "OK"):  # if msg from server starts with 'OK', the client can continue operating, displaying the msg for the user
                print(f"{msg}")
            if (count >= 2):
                MainWindow.response = msg
                break
            elif cmd == "DISCONNECTED":  # if msg from server is 'disconnected', the client displays feedback for user and stops running
                print(f"{msg}")
                break

            cmd = client_details[-1].upper()

            if (cmd == "HELP"):  # if command is help, tell the server to print out the help string
                client.send(cmd.encode(FORMAT))

            elif cmd == "LOGOUT":  # if command is logout, inform server
                client.send(cmd.encode(FORMAT))
                break

            elif cmd == "LIST":
                data_list = cmd + "@"
                data_list += f"{client_details[0]},{client_details[1]}"
                client.send(data_list.encode())

            elif cmd == "UPLOAD":  # if cmd is upload, we must obtain the user's path to the file and send it to the server
                user_email = client_details[0]
                user_password = client_details[1]
                path = client_details[-2]
                file_name = path.split('/')[-1]
                file_size = os.path.getsize(path)
                hasher = hashlib.md5()
                with open(f"{path}", "rb") as f:
                    content = f.read()
                    hasher.update(content)

                data_obtained = cmd
                if (client_details[2][0].upper() == "E"):
                    data_obtained += f'@{file_name},{str(file_size)},{hasher.hexdigest()},'
                    data_obtained += f'{user_email},{user_password},{client_details[2][0]}'
                else:
                    data_obtained += f'@{file_name},{str(file_size)},{hasher.hexdigest()},'
                    data_obtained += f'{user_email},{user_password}'

                print(f"File Size:{file_size}")
                client.sendall(data_obtained.encode())

                with open(f"{path}", "rb") as f:
                    count = 0
                    while count < file_size:
                        file_data = f.read(file_size)

                        client.sendall(file_data)
                        count += len(file_data)
                f.close()
            # if cmd is download, the name of file to be downloaded must be captured, with the directory it must be saved to
            elif cmd == "DOWNLOAD":
                fname = client_details[2]  # name of file
                path = client_details[3]  # directory to save file to
                if (client_details[-2] == "D"):
                    send_data = f"{cmd}@{fname},{client_details[0]},{client_details[1]},{client_details[-2]}"  # send name of file to server
                else:
                    send_data = f"{cmd}@{fname}"
                client.send(send_data.encode())

                outputpath = os.path.join(path, fname)  # output path for the file, where it will be saved

                server_info = client.recv(SIZE).decode()
                fsize = server_info.split('@')[0]
                server_hash = server_info.split('@')[1]

                fsize = int(fsize)  # receive file size from the server

                with open(outputpath,
                          "wb") as f:  # write the file data into the path of user, getting the data from server until the whole file size has been received
                    count = 0
                    while count < fsize:
                        file_data = client.recv(fsize)
                        f.write(file_data)
                        count += len(file_data)

                dld_clnt_hash = hashlib.md5()  # hash variable for file in client directory
                with open(f"{outputpath}", "rb") as f:
                    hash_content = f.read()
                    dld_clnt_hash.update(hash_content)

                # compare server hash and client hash to see if they are the same
                if dld_clnt_hash == server_hash:
                    print("File downloaded without alterations")
                else:
                    print("File altered during downloading process")

                f.close()  # close f when done wrting to the file

            elif cmd == "DELETE":  # if cmd is delete, capture name of file to be deleted, and send it to server
                client.send(f"{cmd}@{client_details[0]}".encode())

        else:  # if the command is not recognised, an error message is displayed, and server is prompted to send the help string for user
            print("You entered an invalid command. Here is a list of commands below:")
            client.send("HELP".encode())

        print("Disconnected from the server.")  # display feedback message to the user
        client.close()  # closing the connection when done


# Create the main window
app = MainWindow()

# Start the main event loop
app.mainloop()

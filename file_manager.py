# ========================= Mohammad Amin Nasiri =========================
# ============================= File Manager =============================


from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
import shutil
import os
import easygui
import subprocess
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class FileManager:
    def __init__(self):
        self.setup_db()
        self.window = Tk()
        self.window.title("File Manager")
        self.window.configure(bg="bisque2")
        self.window.geometry("500x620")
        Label(self.window, text="What should I do?", bg="bisque2", font=("Arial", 16, "bold")).pack(pady=20)
        self.button_frame = Frame(self.window, bg="bisque2")
        self.button_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)
        self.btn_params = {"width": 25, "height": 2, "bg": "white", "activebackground": "chartreuse4"}
        self.create_buttons()

    def setup_db(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="fm_user",
                password="fm_pass",
                database="file_manager"
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS operations (
                    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                    operation VARCHAR(255) NOT NULL,
                    path VARCHAR(1024) NOT NULL,
                    do_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except Error as e:
            messagebox.showerror("DB Error", f"Cannot connect to MySQL: {e}")

    def log_operation(self, operation, path):
        try:
            self.cursor.execute(
                "INSERT INTO operations (operation, path) VALUES (%s, %s)",
                (operation, path)
            )
            self.conn.commit()
        except Error as e:
            messagebox.showerror("DB Error", f"Cannot log operation: {e}")

    def file_open_box(self):
        return easygui.fileopenbox()

    def directory_open_box(self):
        return filedialog.askdirectory()

    def open_file(self):
        path = self.file_open_box()
        if not path:
            return
        try:
            subprocess.call(["xdg-open", path])
            self.log_operation("Open File", path)
        except:
            messagebox.showerror("Error", "Unable to open the selected file.")

    def copy_file(self):
        source = self.file_open_box()
        destination = self.directory_open_box()
        if not source or not destination:
            return
        try:
            shutil.copy(source, destination)
            self.log_operation("Copy File", f"{source} -> {destination}")
            messagebox.showinfo("Success", "File copied successfully.")
        except:
            messagebox.showerror("Error", "Unable to copy the file.")

    def delete_file(self):
        path = self.file_open_box()
        if not path:
            return
        try:
            os.remove(path)
            self.log_operation("Delete File", path)
            messagebox.showinfo("Success", "File deleted successfully.")
        except: 
            messagebox.showerror("Error", "Unable to delete the file.")

    def rename_file(self):
        file = self.file_open_box()
        if not file:
            return
        try:
            path1 = os.path.dirname(file)
            extension = os.path.splitext(file)[1]
            new_name = simpledialog.askstring("Rename File", "Enter new file name:")
            if not new_name:
                return
            path2 = os.path.join(path1, new_name + extension)
            os.rename(file, path2)
            self.log_operation("Rename File", f"{file} -> {path2}")
            messagebox.showinfo("Success", "File renamed successfully.")
        except:
            messagebox.showerror("Error", "Unable to rename the file.")

    def move_file(self):
        source = self.file_open_box()
        destination = self.directory_open_box()
        if not source or not destination:
            return
        if source == destination:
            messagebox.showerror("Error", "Please choose a different directory.")
            return
        try:
            shutil.move(source, destination)
            self.log_operation("Move File", f"{source} -> {destination}")
            messagebox.showinfo("Success", "File moved successfully.")
        except:
            messagebox.showerror("Error", "Unable to move the file.")

    def make_directory(self):
        path = self.directory_open_box()
        if not path:
            return
        name = simpledialog.askstring("Create Folder", "Enter new folder name:")
        if not name:
            return
        new_dir = os.path.join(path, name)
        try:
            os.mkdir(new_dir)
            self.log_operation("Create Folder", new_dir)
            messagebox.showinfo("Success", "Directory created successfully.")
        except:
            messagebox.showerror("Error", "Unable to create the directory.")

    def remove_directory(self):
        path = self.directory_open_box()
        if not path:
            return
        try:
            shutil.rmtree(path)
            self.log_operation("Delete Folder", path)
            messagebox.showinfo("Success", "Directory deleted successfully.")
        except:
            messagebox.showerror("Error", "Unable to delete the directory.")

    def list_files(self):
        path = self.directory_open_box()
        if not path:
            return
        try:
            file_list = sorted(os.listdir(path))
            list_window = Toplevel(self.window)
            list_window.title(f"Files in {path}")
            list_window.geometry("400x400")
            list_window.configure(bg="bisque2")
            frame = Frame(list_window, bg="bisque2")
            frame.pack(expand=True, fill=BOTH, padx=10, pady=10)
            text_area = Text(frame, bg="bisque2", fg="black")
            text_area.pack(expand=True, fill=BOTH)
            for filename in file_list:
                text_area.insert(END, filename + "\n")
            text_area.config(state=DISABLED)
            self.log_operation("List Files", path)
        except:
            messagebox.showerror("Error", "Unable to list files in the directory.")

    def exit_program(self):
        try:
            self.conn.close()
        except:
            pass
        self.window.destroy()

    def create_buttons(self):
        Button(self.button_frame, text="Open File", command=self.open_file, **self.btn_params).pack(pady=5)
        Button(self.button_frame, text="Copy File", command=self.copy_file, **self.btn_params).pack(pady=5)
        Button(self.button_frame, text="Delete File", command=self.delete_file, **self.btn_params).pack(pady=5)
        Button(self.button_frame, text="Rename File", command=self.rename_file, **self.btn_params).pack(pady=5)
        Button(self.button_frame, text="Move File", command=self.move_file, **self.btn_params).pack(pady=5)
        Button(self.button_frame, text="Create Folder", command=self.make_directory, **self.btn_params).pack(pady=5)
        Button(self.button_frame, text="Delete Folder", command=self.remove_directory, **self.btn_params).pack(pady=5)
        Button(self.button_frame, text="List Files", command=self.list_files, **self.btn_params).pack(pady=5)
        Button(self.button_frame, text="Exit", command=self.exit_program, **self.btn_params).pack(pady=5)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    fm = FileManager()
    fm.run()

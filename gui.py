import tkinter as tk
import subprocess
import os

class CLI_GUI:
    def __init__(self, master):
        self.master = master
        master.title("CLI GUI")

        # Command Input Field
        self.command_entry = tk.Entry(master)
        self.command_entry.pack(fill=tk.X)
        self.command_entry.focus()

        # Output Display Area
        self.output_text = tk.Text(master, height=10, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Command History
        self.history_label = tk.Label(master, text="Command History:")
        self.history_label.pack()
        self.history_listbox = tk.Listbox(master, height=5)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)

        # Execute Command Button
        self.execute_button = tk.Button(master, text="Execute", command=self.execute_command)
        self.execute_button.pack()

        # Bind Return key to execute command
        master.bind('<Return>', lambda event: self.execute_command())

    def execute_command(self):
        command = self.command_entry.get()
        self.output_text.insert(tk.END, f">>> {command}\n")  # Display command
        result = self.execute_command_line(command)
        self.output_text.insert(tk.END, f"{result}\n\n")  # Display command output
        self.command_entry.delete(0, tk.END)  # Clear command entry

        # Update command history
        self.history_listbox.insert(tk.END, command)

    def execute_command_line(self, command):
        # Check if it's a directory change command
        if command.startswith("cd "):
            directory = command[3:].strip()  # Extract the directory path
            try:
                # Change the current working directory
                os.chdir(directory)
                return f"Changed directory to: {directory}"
            except FileNotFoundError:
                return f"Directory not found: {directory}"
            except Exception as e:
                return f"Error changing directory: {str(e)}"
        
        elif command.startswith("rm ") or command.startswith("del "):
            file_path = command[3:].strip()  # Extract the file path
            return self.delete_file(file_path)

        elif command.startswith("touch ") or command.startswith("echo ") or command.startswith("type NUL >"):
            file_path = command[6:].strip()  # Extract the file path
            return self.create_file(file_path)

        else:
            try:
                # Execute other commands using subprocess
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout
                else:
                    return f"Error executing command: {result.stderr}"
            except Exception as e:
                return f"Error executing command: {str(e)}"

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            return f"File '{file_path}' deleted successfully."
        except FileNotFoundError:
            return f"File '{file_path}' not found."
        except Exception as e:
            return f"Error deleting file '{file_path}': {e}"

    def create_file(self, file_path):
        try:
            with open(file_path, "w") as f:
                pass  # Create an empty file
            return f"File '{file_path}' created successfully."
        except Exception as e:
            return f"Error creating file '{file_path}': {e}"

def main():
    root = tk.Tk()
    cli_gui = CLI_GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

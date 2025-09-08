import os
import platform
import subprocess
import signal

def kill_running_processes():
    system = platform.system()
    script_name = "AntiWare"  # base name of your program

    if system == "Windows":
        try:
            # Get the list of processes
            output = subprocess.check_output("tasklist", shell=True).decode()
            for line in output.splitlines():
                if script_name.lower() in line.lower():
                    # Extract PID and kill process
                    parts = line.split()
                    pid = int(parts[1])
                    subprocess.call(f"taskkill /F /PID {pid}", shell=True)
                    print(f"Killed process PID {pid}")
        except Exception as e:
            print(f"Error killing processes: {e}")

    elif system == "Darwin":  # macOS
        try:
            # Get PIDs for the running script
            output = subprocess.check_output(["pgrep", "-f", script_name]).decode()
            for pid_str in output.splitlines():
                pid = int(pid_str)
                os.kill(pid, signal.SIGKILL)
                print(f"Killed process PID {pid}")
        except subprocess.CalledProcessError:
            print("No running processes found.")
        except Exception as e:
            print(f"Error killing processes: {e}")

def reset_unlock_and_startup():
    system = platform.system()

    if system == "Windows":
        home = os.path.expanduser("~")
        unlock_file = os.path.join(home, ".pianto_unlocked")
        startup_folder = os.path.join(os.environ.get("APPDATA", ""), 
                                      "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        shortcut_path = os.path.join(startup_folder, "PiantoRedScreen.lnk")

        # Remove unlock file
        if os.path.exists(unlock_file):
            os.remove(unlock_file)
            print(f"Removed unlock file: {unlock_file}")
        else:
            print("No unlock file found.")

        # Remove startup shortcut
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
            print(f"Removed startup shortcut: {shortcut_path}")
        else:
            print("No startup shortcut found.")

    elif system == "Darwin":  # macOS
        unlock_file = os.path.expanduser("~/.pianto_unlocked")
        plist_folder = os.path.expanduser("~/Library/LaunchAgents")
        plist_path = os.path.join(plist_folder, "com.user.pianto.plist")

        # Remove unlock file
        if os.path.exists(unlock_file):
            os.remove(unlock_file)
            print(f"Removed unlock file: {unlock_file}")
        else:
            print("No unlock file found.")

        # Remove plist startup file
        if os.path.exists(plist_path):
            os.system(f"launchctl unload {plist_path} 2>/dev/null")
            os.remove(plist_path)
            print(f"Removed startup plist: {plist_path}")
        else:
            print("No startup plist found.")

    else:
        print("Unsupported OS.")
        return

    # Kill any running instances
    kill_running_processes()

if __name__ == "__main__":
    reset_unlock_and_startup()

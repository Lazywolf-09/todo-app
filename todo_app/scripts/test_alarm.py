import os

def trigger_alarm():
    # You can use different methods to trigger an alarm sound
    # This example uses a system beep sound, you can replace this with an actual alarm sound
    if os.name == 'nt':  # For Windows
        import winsound
        winsound.Beep(1000, 1000)  # Beep sound for 1 second
    else:  # For macOS/Linux
        os.system('say "Reminder!"')  # Or you can use `afplay /path/to/alarm.mp3`

if __name__ == "__main__":
    trigger_alarm()

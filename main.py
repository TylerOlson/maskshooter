import serial
import threading


def main():
    port = input("What port is Arduino on?\n")
    ser = serial.Serial(port)

    stop_event = threading.Event()
    read_thread = threading.Thread(
        target=serial_reader, args=(ser, stop_event), daemon=True)
    read_thread.start()
    while(True):
        try:
            inp = input()
            if inp == "stop":
                break
            ser.write(inp.encode('UTF-8'))
        except (KeyboardInterrupt, SystemExit):
            break

    stop_event.set()
    ser.close()


def serial_reader(ser, stop_event):
    while not stop_event.is_set():
        if ser.in_waiting > 0:
            print("Recieved message: " +
                  ser.readline().decode().replace("\r\n", ""))


if __name__ == "__main__":
    main()

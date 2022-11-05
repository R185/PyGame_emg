import serial


con_done = False
ser = serial
def connection(port):
    global ser
    try:
        ser = serial.Serial("COM"+str(3), 115200)
    except Exception:
        return "NO"
    return "OK"


def make_conn():
    global con_done
    i = 0
    while con_done != True:
        if connection(i) != "OK":
            i += 1
        else:
            con_done = True
        if i == 1000:
            break




import pymem
import keyboard
import time

#Offsets
dwLocalPlayer = 0xDEA964
dwForceJump = 0x52BBD50
m_fFlags = 0x104

def main():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    player = pm.read_int(client + dwLocalPlayer)

    while True:
        if keyboard.is_pressed("space"):
            if pm.read_int(player + m_fFlags) == 257:
                pm.write_int(client + dwForceJump, 6)
                time.sleep(0.04)
                pm.write_int(client + dwForceJump, 4)
        time.sleep(0.01)

if __name__ == '__main__':
    main()
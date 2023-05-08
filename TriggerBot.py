import pymem
import pymem.process
import keyboard
import time

#Offsets
dwEntityList = 0x4DFFFB4
dwLocalPlayer = 0xDEA964
m_iCrosshairId = 0x11838
m_iHealth = 0x100
m_iTeamNum = 0xF4
dwForceAttack = 0x322DDEC

def main():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        
        if not keyboard.is_pressed("alt"):
            time.sleep(.01)
            
        if keyboard.is_pressed("alt"):
            player = pm.read_uint(client + dwLocalPlayer)
            enemyID = pm.read_uint(player + m_iCrosshairId)
            enemy = pm.read_uint(client + dwEntityList + (enemyID - 1) * 16)

            EnemyTeam = pm.read_uint(enemy + m_iTeamNum)
            PlayerTeam = pm.read_uint(player + m_iTeamNum)

            if enemyID > 0 and enemyID <= 32 and PlayerTeam != EnemyTeam:
                pm.write_uint(client + dwForceAttack, 6)

            time.sleep(0.002)

if __name__ == '__main__':
    main()
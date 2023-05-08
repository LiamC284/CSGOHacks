import pymem
import pymem.process
import time

#Offsets
dwLocalPlayer = 0xDEA964
dwEntityList = 0x4DFFFC4
dwGlowObjectManager = 0x535AA70
m_iGlowIndex = 0x10488
m_iTeamNum = 0xF4

def main():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        player = pm.read_int(client + dwLocalPlayer)
        glow_manager = pm.read_int(client + dwGlowObjectManager)

        for i in range (1, 32):
            entity = pm.read_int(client + dwEntityList + (i - 1) * 16)
            entity_team = pm.read_int(entity + m_iTeamNum)
            player_team = pm.read_int(player + m_iTeamNum)

            if entity_team != player_team:
                glow_index = pm.read_int(entity + m_iGlowIndex)
                pm.write_float(glow_manager + (glow_index * 0x38) + 0x8, float(1))
                pm.write_float(glow_manager + (glow_index * 0x38) + 0xC, float(0))
                pm.write_float(glow_manager + (glow_index * 0x38) + 0x10, float(0))
                pm.write_float(glow_manager + (glow_index * 0x38) + 0x14, float(1))

                pm.write_bool(glow_manager + glow_index * 0x38 + 0x28, True)
                pm.write_bool(glow_manager + glow_index * 0x38 + 0x29, False)

        time.sleep(0.01)

if __name__ == '__main__':
    main()
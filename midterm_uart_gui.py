import serial
import serial.tools.list_ports
import threading
import sys
import time

def read_from_port(ser):
    """ 後台執行緒：持續接收並列印來自 STM32 的資料 """
    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8', errors='ignore')
                print(data, end='', flush=True)
        except Exception:
            break

def main():
    print("=" * 60)
    print("  老媽突擊終結者 (Mom Raid Terminator) - 串口文字控制台")
    print("=" * 60)
    
    # 自動搜尋可用的 COM 埠
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("[Error] 找不到任何可用的 COM 埠，請檢查 STM32 是否已連接！")
        return

    print("偵測到的串口列表：")
    for i, p in enumerate(ports):
        print(f"  [{i+1}] {p.device} - {p.description}")

    # 預設選擇第一個 COM 埠或由使用者輸入
    port_name = ports[0].device
    baud_rate = 115200

    try:
        ser = serial.Serial(port_name, baud_rate, timeout=1)
        print(f"\n[System] 成功開啟 {port_name} (BaudRate: {baud_rate})")
        print("[System] 系統監控中... 當進入 State 3 時，輸入 'Safe' 並按 Enter 可解鎖重置。")
        print("[System] 輸入 'exit' 可關閉程式。\n" + "-" * 60)
    except Exception as e:
        print(f"\n[Error] 無法開啟串口 {port_name}: {e}")
        return

    # 啟動背景接收執行緒
    thread = threading.Thread(target=read_from_port, args=(ser,), daemon=True)
    thread.start()

    # 主執行緒：讀取鍵盤輸入並發送至 STM32
    while True:
        try:
            user_input = input()
            if user_input.lower() == 'exit':
                print("[System] 結束連線。")
                break
            
            # 發送指令給 STM32
            send_cmd = user_input + "\r\n"
            ser.write(send_cmd.encode('utf-8'))
            print(f"[TX 發送] -> {user_input}")
            
        except (KeyboardInterrupt, EOFError):
            print("\n[System] 程式結束。")
            break

    ser.close()

if __name__ == '__main__':
    main()
    
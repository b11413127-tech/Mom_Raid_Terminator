README.md —老媽突擊終結者



\# 老媽突擊終結者 (Mom Raid Terminator) (NUCLEO-G474RE 期中專題)



用於偵測老媽突擊並應對的系統。平常是桌燈，警報時快閃倒數，最後提供解鎖題目。每天一筆狀態記錄送上雲端。



\## 1. 情境故事：誰、在哪、遇到什麼麻煩



學生正在房間電腦前專心學習/娛樂，突然老媽無預警推門而入，造成尷尬或打擾。需要一個系統能在老媽靠近時發出警告，並提供一個緊急防禦（例如桌燈變黃，電腦輸出微積分題目）來爭取時間。



\## 2. 替身對照：故事裡的模組 -> 板上替身



\- 老媽偵測感測器 (BTN1\_SENSOR) -> PC13 藍色按鈕 (一按 = 老媽來了)



\- 緊急解鎖按鈕 (BTN2\_EMERGENCY) -> PB2 黑色按鈕



\- 桌燈 (核心裝置) -> 包含 PA5 PWM 綠燈、PA6 紅燈、PA7 黃燈、PB6 蜂鳴器的複合裝置



\## 3. 功能與驗收條件：動作、預期、實測結果



\- \*\*\[State 1] 待命\*\*: PA5 綠燈 10% 亮度。預期：平常狀態。實測：OK。



\- \*\*\[State 2] 警報\*\*: 按下 PC13。綠燈滅，PA6 紅燈與 PB6 蜂鳴器 0.5 秒同步快閃。UART 每秒發送 'Count: XX'，10秒倒數。預期：警報觸發。實測：OK。



\- \*\*\[State 3] 防禦\*\*: 倒數結束或按下 PB2。紅燈滅，PB6 蜂鳴器滅，PA7 黃燈點亮。UART 發送微積分題目，提示使用者輸入 'Safe' 解鎖。預期：進入防禦。實測：OK。



\- \*\*解鎖\*\*: 在 UART 接收到 "Safe\\r\\n"。系統自動重置系統回 \[State 1]。預期：解鎖成功。實測：OK。



\- \*\*雲端記錄\*\*: 每天發送一筆狀態記錄上傳至雲端。預期：記錄成功。實測：OK (雲端平台確認)。



\## 4. 用到的技術：第 3 ～ 7 週勾選表 (同投影片)



GPIO EXTI (按鈕中斷), TIM (PWM 綠燈、1ms 計時計時), LPUART (電腦通訊), ADC (模擬狀態記錄數據), Cloud Communication (模擬上傳記錄)。



\## 5. 腳位表：用到的每支腳與用途



\- \*\*LPUART1 (通訊)\*\*: PA2 = TX, PA3 = RX (115200 8N1)



\- \*\*TIM2 (PWM 綠燈)\*\*: PA5 = CH1



\- \*\*GPIO Output (LEDs/Buzzer)\*\*: PA6 = LED\_RED, PA7 = LED\_YELLOW, PB6 = BUZZER



\- \*\*GPIO EXTI (按鈕)\*\*: PC13 = BTN1\_SENSOR (藍色按鈕) - 替身為老媽偵測器, PB2 = BTN2\_EMERGENCY (黑色按鈕) - 替身為緊急解鎖



\- \*\*(模擬 ADC)\*\*: 例如 PA0 (ADC1\_IN0) - 用於模擬上傳的狀態數據。



\## 6. 建置與執行：開發環境、燒錄步驟、終端機設定、命令



\- \*\*開發環境\*\*: STM32CubeIDE (或其他兼容 IDE)。



\- \*\*燒錄步驟\*\*: ...



\- \*\*終端機設定\*\*: 波特率 115200，8N1，無硬體流控。



\- \*\*命令\*\*: 在 \[State 3] 時輸入 \*\*'Safe'\*\*。



\## 7. 程式結構：哪個檔做什麼、ISR 與主迴圈分工



\-本專案主要包含三個核心程式檔案：檔案名稱核心職責與分工main.c主要邏輯與狀態機控制中心• 定義全域變數與 FSM 狀態枚舉 (SystemState)。• 包含 main() 進入點與 while(1) 主迴圈。• 實作 FSM 狀態切換與硬體控制（PWM、LED、蜂鳴器）。• 處理非阻塞式 UART 接收與指令解析（如收到 "Safe"）。• 提供 EXTI 與 Timer 中斷的回呼函式（Callback）。stm32g4xx\_it.c底層中斷向量入口 (Interrupt Service Routines, ISR)• 存放 CPU 硬體中斷向量函式（如 TIM2\_IRQHandler()、EXTI2\_IRQHandler() 等）。• 當硬體觸發中斷時，CPU 第一時間進入此處，並呼叫 HAL 庫的通用處理函式（如 HAL\_TIM\_IRQHandler()）。• 最終將執行流程轉交給 main.c 中的 Callback 函式。main.h全域標頭檔與腳位巨集定義• 宣告全域周邊 Handle（如 hlpuart1、htim2）。• 定義硬體腳位標籤巨集（如 BTN1\_SENSOR\_Pin、LED\_RED\_Pin 等）。• 引入 STM32 HAL 庫核心標頭檔。二、 ISR 與主迴圈的分工架構 (Core Architecture)嵌入式系統設計的重要原則是：「中斷處理 (ISR) 越短越好，耗時任務交給主迴圈 (while(1))」。\[ 硬體事件觸發 ] (按鍵按下 / 1ms 定時器溢位)

&#x20;      │

&#x20;      ▼

\[ ISR 中斷服務函式 ] (stm32g4xx\_it.c / HAL Callback)

&#x20;      │

&#x20;      ├─► 僅執行：快速防抖 / 累加計數器 / 設定 Flag 標籤

&#x20;      │

&#x20;      ▼

\[ 主迴圈 while(1) ] (main.c)

&#x20;      │

&#x20;      └─► 執行：UART 字串發送 / 狀態機(FSM)切換 / PWM 與 GPIO 輸出控制

1\. 中斷服務函式 (ISR / Callbacks) 的分工ISR 的職責是即時響應硬體事件，絕不執行阻塞（如 HAL\_Delay）或耗時動作（如 UART HAL\_UART\_Transmit）：按鈕外部中斷 (HAL\_GPIO\_EXTI\_Callback)：動作：使用 HAL\_GetTick() 進行 >200ms 軟體去彈跳。分工：確認為有效按壓後，僅更新 currentState（如切換至 STATE\_2 或 STATE\_3）與重置計數器，隨即退出中斷。定時器中斷 (HAL\_TIM\_PeriodElapsedCallback)：動作：每 1ms 觸發一次。分工：累加 timer\_500ms\_counter，滿 500ms 時僅切換 buzzer\_led\_toggle 旗標與控制 GPIO Toggle。累加 timer\_1ms\_counter，滿 1000ms 時將 countdownSeconds 扣減。當需要發送串口倒數訊息時，僅將 uart\_send\_flag 設為 1，不直接在中斷內呼叫 UART 發送。2. 主迴圈 (main() 的 while(1)) 的分工主迴圈負責系統狀態輪詢、指令解析與耗時/通訊任務：非阻塞 UART 接收：呼叫 HAL\_UART\_Receive(\&hlpuart1, \&rx\_byte, 1, 0)（Timeout = 0）。當收到 \\r 或 \\n 時解析字串，若收到 "Safe" 則將 currentState 切回 STATE\_1。安全 UART 訊息發送：輪詢檢查 uart\_send\_flag。若為 1，則在主迴圈中使用 sprintf 格式化字串並透過 UART\_SendString 阻塞式發送倒數訊息。FSM 狀態機與硬體輸出：判定 if (currentState != lastState)。當狀態發生改變時，更新 lastState 並透過 switch-case 統一調配 PWM 佔空比（\_\_HAL\_TIM\_SET\_COMPARE）、LED 電位（HAL\_GPIO\_WritePin）以及發送狀態切換提示訊息。



\## 8. 實作照片

!\[圖片1](image/1.png)

!\[圖片2](image/2.png)

!\[圖片3](image/3.png)


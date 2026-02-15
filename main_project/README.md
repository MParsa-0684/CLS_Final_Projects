# BadUSB HID Simulation Project 🖥️

## 1. Title and Introduction 🚀

This project simulates a BadUSB device using the following components:

- **MCU:** ATtiny85 microcontroller (firmware in C/Assembly)
- **Bridge Script:** Python script on host PC
- **Simulation Environment:** Proteus for LED/UART simulation

The system functions as a Human Interface Device (HID) that can:

- Extract system data (e.g., IP) from the host PC
- Transmit and receive data using a custom LED/UART protocol
- Replay stored keystrokes to the target system

### Run the Bridge Script on Host PC

```bash
python3 bridge.py
```

### Notes

- MCU communicates via bit-banged UART.
- LED states (CapsLock/NumLock/ScrollLock) represent transmitted bits.
- Bridge interprets MCU commands and simulates keyboard input using pyautogui.

---

## 2. MCU Firmware (ATtiny85) 🧩

### Pin Configuration

```c
#define TX_PIN PORTB.0
#define RX_PIN PINB.1
#define BTN_PIN PINB.4
```

### UART Functions

- uart_tx(char data) — sends a character bit by bit using precise delays
- uart_rx() — receives characters bit by bit
- uart_print_flash(flash char *str) — prints string stored in flash
- uart_print_ram(char *str) — prints string stored in RAM

### Attack Mode (Extraction)

- MCU sends CMD:RUN → opens Windows Run dialog
- MCU sends TYPE:powershell "Set-Clipboard -Value (Get-NetIPAddress -AddressFamily IPv4).IPAddress[0]" → copies IP to clipboard
- MCU sends KEY:ENTER → executes command
- MCU sends ACTION:GET_CLIP → Bridge reads clipboard and sends IP character-by-character back to MCU
- MCU stores result in stolen_data[32]

### Playback Mode

- User presses the button → MCU sends stored keystrokes to the host
- Automatically opens Notepad and types extracted data

---

## 3. Bridge Python Script 🐍

The Bridge Python script handles communication with the MCU and simulates keyboard input on the host PC.

### Command Handling

- CMD:RUN → Opens Run dialog
- TYPE:<text> → Types text using pyautogui
- KEY:ENTER → Presses Enter key
- ACTION:GET_CLIP → Reads clipboard content and sends to MCU

### Example Code Snippet

```python
if cmd.startswith("TYPE:"):
    pyautogui.write(cmd[5:], interval=0.01)
```

### Bridge Script Responsibilities

- Serial communication with MCU
- Execute host-side commands
- Send LED status updates to MCU
- Maintain timing to ensure correct UART communication

---

## 4. Proteus Simulation 💡

- Simulates LEDs representing CapsLock / NumLock / ScrollLock
- LED states are used to transmit bits to the MCU
- Allows testing of the extraction and playback system without physical hardware

---

## 5. Custom Protocol 🔄

- Data transmitted character by character over bit-banged UART
- Commands terminated with \n

### Supported Commands

- CMD:<action> — system actions
- TYPE:<text> — type text on host
- KEY:<key> — press a specific key
- ACTION:GET_CLIP — retrieve clipboard content

### Timing Considerations

- MCU and Bridge maintain delays (50–100 ms) between characters to avoid overflow
- LED polling occurs every 0.2 seconds to detect state changes

---

## 6. Memory Management 🧠

- Temporary storage: stolen_data[32]
- Prevents overflow by limiting extracted data length
- EEPROM functionality is simulated using RAM in Proteus
- MCU firmware clears buffer before reuse

---

## 7. Sample Flow (Extraction → Playback) 🔁

1. MCU sends CMD:RUN → Bridge opens Run dialog
2. MCU sends TYPE:powershell command → executes clipboard extraction
3. MCU sends KEY:ENTER
4. MCU sends ACTION:GET_CLIP
5. Bridge sends clipboard data to MCU
6. MCU stores extracted IP in stolen_data
7. Playback mode: button press → MCU sends TYPE:<stolen_data> to host

---

## 8. Example Commands and Actions 📝

MCU Command | Host Action  
-----------|-------------
CMD:RUN | Open Windows Run dialog  
TYPE:notepad | Open Notepad  
KEY:ENTER | Press Enter  
ACTION:GET_CLIP | Retrieve clipboard content  

---

## 9. Challenges and Notes ⚡

- Bit-banged UART required precise timing
- LED signaling used unconventional channel for data transmission
- Ensuring reliable clipboard reading in Windows required retries
- MCU firmware written in C/Assembly required careful memory management

---

## 10. Conclusion ✅

- Successfully simulates a BadUSB HID device without physical hardware
- Demonstrates microcontroller programming, custom UART protocol, LED signaling, and host automation
- Safe environment to test data extraction and playback mechanisms
- Bridges theoretical understanding with practical simulation of hardware attack

# 🖥️ BadUSB Mechanism Implementation Using ATtiny85

**Project Name:** System Information (IP Address) Extraction via Keyboard Simulation  
**Microcontroller:** ATtiny85  
**Programming Languages:** C (CodeVisionAVR) and Python  
**Simulation Environment:** Proteus Design Suite  

---

## 1. Introduction and Objectives 🎯

This project simulates the behavior of a **BadUSB** device. BadUSBs are malicious USB devices that present themselves as a keyboard (HID – Human Interface Device). Since operating systems inherently trust keyboards, such devices can rapidly type and execute commands.

To avoid implementing the full USB protocol in simulation, a hybrid approach is used:

- ATtiny85 manages the attack logic  
- UART is used as the command transport layer  
- A Python script converts serial commands into real keyboard events  

**Final Objective:** Automatically extract the victim system’s IP address upon connection and display it when the user presses a button.

---

## 2. Hardware Design 🔧

### Circuit Overview
- **MCU:** ATtiny85 running on internal 8 MHz oscillator  
- **Serial Interface:** COMPIM (Proteus) connected to Windows COM ports  
- **User Input:** Push button on PB4  
- **UART:** Software-based (bit-banging) on PB0  

### Fuse Bit Settings ⚙️
- **CKSEL:** Internal RC Oscillator 8 MHz  
- **CKDIV8:** Disabled  

---

## 3. Software Design 💻

### MCU Firmware (CodeVisionAVR)
- Software UART at 9600 baud  
- Two-phase state machine:
  - **Auto-Run:** Executes payload after startup delay  
  - **Interactive:** Waits for button press  

**Payload Used:**

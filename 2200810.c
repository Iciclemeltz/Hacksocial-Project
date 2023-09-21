#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "pico/time.h"

// Define the GPIO pin for the START button and the debounce time
#define START_BUTTON_PIN 15
#define DEBOUNCE_TIME_MS 100 // Debounce time in milliseconds

// Variables to track stopwatch state and start time
volatile bool is_stopwatch_running = false;
volatile uint64_t start_timestamp_ms = 0;

// Callback function for button press with debounce
void handle_button_press(uint gpio, uint32_t events)
{
    // Debounce algorithm using time (100ms debounce time)
    static uint64_t last_interrupt_time_ms = 0;
    uint64_t current_timestamp_ms = to_ms_since_boot(get_absolute_time());

    if ((current_timestamp_ms - last_interrupt_time_ms) < DEBOUNCE_TIME_MS)
    {
        // Ignore button events within the debounce time
        return;
    }
    last_interrupt_time_ms = current_timestamp_ms;

    // Check if the button(input pin is inserted or released) is pressed or released
    if (gpio_get(gpio))
    {
        if (!is_stopwatch_running)
        {
            // Start the stopwatch and record the start time
            start_timestamp_ms = current_timestamp_ms;
            is_stopwatch_running = true;
            printf("Stopwatch started\n");
        }
        else
        {
            // Stop and reset the stopwatch, then calculate and print the elapsed time
            is_stopwatch_running = false;
            uint64_t elapsed_seconds = (current_timestamp_ms - start_timestamp_ms) / 1000; // Convert to seconds
            printf("Stopwatch stopped. Elapsed time: %llu seconds\n", elapsed_seconds);
        }
    }
}

int main()
{
    // Initialize the standard I/O for printf
    stdio_init_all();

    // Initialize the GPIO pin for the START button and configure the pull-up resistor
    gpio_init(START_BUTTON_PIN);
    gpio_set_dir(START_BUTTON_PIN, GPIO_IN);
    gpio_pull_up(START_BUTTON_PIN);

    // Enable interrupts on the START button with the debounce callback
    gpio_set_irq_enabled_with_callback(START_BUTTON_PIN, GPIO_IRQ_EDGE_RISE | GPIO_IRQ_EDGE_FALL, true, &handle_button_press);

    while (1)
    {
        // Enter a tight loop, waiting for button events and handling them in the callback
        tight_loop_contents();
    }

    return 0;
}

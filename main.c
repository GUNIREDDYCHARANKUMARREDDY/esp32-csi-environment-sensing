// Standard C string handling
#include <string.h>

// FreeRTOS headers
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// ESP32 system and Wi-Fi headers
#include "esp_wifi.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_event.h"
#include "esp_netif.h"

// lwIP headers
#include "lwip/sockets.h"
#include "lwip/inet.h"

#define AP_SSID "ESP32_AP_B"
#define AP_PASS "12345678"
#define AP_CHANNEL 6
#define MAX_STA_CONN 4

#define DEST_IP "192.168.4.2"   // Change to receiver STA IP if needed
#define DEST_PORT 1234

static const char *TAG = "TX_CONTINUOUS";

// UDP Packet Sender Task
void udp_sender_task(void *pvParameters)
{
    struct sockaddr_in dest_addr;
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(DEST_PORT);
    dest_addr.sin_addr.s_addr = inet_addr(DEST_IP);

    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP);
    if (sock < 0) {
        ESP_LOGE(TAG, "Failed to create socket: errno %d", errno);
        vTaskDelete(NULL);
        return;
    }

    char payload[] = "CSI Trigger Packet";

    while (1) {
        int err = sendto(sock, payload, strlen(payload), 0,
                         (struct sockaddr *)&dest_addr, sizeof(dest_addr));
        if (err < 0) {
            ESP_LOGE(TAG, "Send error: errno %d", errno);
        } else {
            ESP_LOGI(TAG, "Packet sent");
        }

        // ✅ Small delay to avoid CPU overload, Wi-Fi congestion, and crashes
        vTaskDelay(pdMS_TO_TICKS(5));  // Delay of 1ms for safety & stability
    }

    close(sock);
    vTaskDelete(NULL);
}

// Wi-Fi Access Point Setup
void wifi_init_softap(void)
{
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_ap();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    wifi_config_t wifi_config = {
        .ap = {
            .ssid = AP_SSID,
            .ssid_len = strlen(AP_SSID),
            .password = AP_PASS,
            .channel = AP_CHANNEL,
            .max_connection = MAX_STA_CONN,
            .authmode = WIFI_AUTH_WPA_WPA2_PSK,
            .ssid_hidden = 0,
            .beacon_interval = 100,
        },
    };

    if (strlen(AP_PASS) == 0) {
        wifi_config.ap.authmode = WIFI_AUTH_OPEN;
    }

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_AP, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "SoftAP Started: SSID:%s Password:%s Channel:%d",
             AP_SSID, AP_PASS, AP_CHANNEL);
}

// App Entry Point
void app_main(void)
{
    ESP_ERROR_CHECK(nvs_flash_init());
    wifi_init_softap();
    xTaskCreate(udp_sender_task, "udp_sender_task", 4096, NULL, 5, NULL);

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

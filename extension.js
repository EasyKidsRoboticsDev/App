({
    name: Blockly.Msg.blocks_uart, // Category Name
    description: "ESP32 BLE UART",
    author: "microBlock",
    category: "Communication",
    version: "1.0.0",
    icon: "/static/icon.png", // Category icon
    color: "#F39C12", // Category color (recommend some blocks color)
    blocks: [ // Blocks in Category      
        "ble_device_name",
        "ble_on_receive",
        "ble_get_data",
        //"ble_send_text",
        {
            xml: `
                <block type="ble_send_text">
                    <value name="sendtxt">
                        <shadow type="text">
                            <field name="TEXT">text</field>
                        </shadow>
                    </value>
                </block>
            `
        },
         "string_decode"
         ]
});

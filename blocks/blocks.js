Blockly.defineBlocksWithJsonArray(
[
{
  "type": "ble_device_name",
  "message0": Blockly.Msg.ble_device_name,
  "args0": [
    {
      "type": "field_input",
      "name": "devname",
      "text": ""
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": "#F39C12",
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "ble_on_receive",
  "message0": Blockly.Msg.ble_on_receive,
  "args0": [
    {
      "type": "input_dummy"
    },
    {
      "type": "input_statement",
      "name": "rxd_callback"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": "#F39C12",
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "ble_send_text",
  "message0": Blockly.Msg.ble_send_text,
  "args0": [
    {
      "type": "input_value",
      "name": "sendtxt",
      "check": "String"
    },
    {
      "type": "field_checkbox",
      "name": "CR",
      "checked": false
    },
    {
      "type": "field_checkbox",
      "name": "LF",
      "checked": false
    }	
  ],
  "inputsInline": true,
  "previousStatement": null,
  "nextStatement": null,
  "colour": "#F39C12",
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "ble_get_data",
  "message0": Blockly.Msg.ble_get_data,
  "output": null,
  "colour": "#F39C12",
  "tooltip": "",
  "helpUrl": ""
},
{  
  "type": "string_decode",
  "message0": Blockly.Msg.string_decode,
  "args0": [
    {
      "type": "input_value",
      "name": "v7rc_string",
      "check": ""
    },
    {
      "type": "field_number",
      "name": "decode_num1",
      "value":0
    },
    {
      "type": "field_number",
      "name": "decode_num2",
      "value":0
    }	
  ],
  "inputsInline": true,
  "output": null,
  "colour": "#F39C12",
  "tooltip": "",
  "helpUrl": ""
}
]
);

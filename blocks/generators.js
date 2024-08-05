Blockly.Python['ble_device_name'] = function(block) {
  Blockly.Python.definitions_['import ubluetooth as bt'] = 'import ubluetooth as bt';
  Blockly.Python.definitions_['from ble_uart import BLEUART'] = 'from ble_uart import BLEUART';
  //Blockly.Python.definitions_['from tools import BLETools'] = 'from tools import BLETools';
  //Blockly.Python.definitions_['from const import BLEConst'] = 'from const import BLEConst';
  var text_devname = block.getFieldValue('devname');
  var code = `ble = bt.BLE(); uart = BLEUART(ble, rx_callback,name="${text_devname}")\n`;
  return code;
};

Blockly.Python['ble_on_receive'] = function(block) {

  var globals = [];
  var varName;
  var workspace = block.workspace;
  var variables = Blockly.Variables.allUsedVarModels(workspace) || [];
  for (var i = 0, variable; variable = variables[i]; i++) {
    varName = variable.name;
    if (block.getVars().indexOf(varName) == -1) {
      globals.push(Blockly.Python.variableDB_.getName(varName,
          Blockly.VARIABLE_CATEGORY_NAME));
    }
  }
  // Add developer variables.
  var devVarList = Blockly.Variables.allDeveloperVariables(workspace);
  for (var i = 0; i < devVarList.length; i++) {
    globals.push(Blockly.Python.variableDB_.getName(devVarList[i],
        Blockly.Names.DEVELOPER_VARIABLE_TYPE));
  }

  globals = globals.length ?
      Blockly.Python.INDENT + 'global ' + globals.join(', ') + '\n' : '';
 

  var statements_callback = Blockly.Python.statementToCode(block, 'rxd_callback');
  var functionName = Blockly.Python.provideFunction_(
    'rx_callback',
    ['def ' + Blockly.Python.FUNCTION_NAME_PLACEHOLDER_ + '(data):',
    globals,
    statements_callback|| Blockly.Python.PASS]);

  var code = ``;
  return code;
};

Blockly.Python['ble_send_text'] = function(block) {
  var text_sendtxt =Blockly.Python.valueToCode(block, 'sendtxt', Blockly.Python.ORDER_ATOMIC);
  var L1=(block.getFieldValue('CR')=='TRUE'? '\\r' : '');
  var L2=(block.getFieldValue('LF')=='TRUE'? '\\n' : '');
  var string_code=L1+L2;
  var code = `uart.send(${text_sendtxt}+'${string_code}')\n`;
  return code;
};

Blockly.Python['ble_get_data'] = function(block) {
  var code = 'data';
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['string_decode'] = function(block) {
  var text_v7rc_string = Blockly.Python.valueToCode(block, 'v7rc_string', Blockly.Python.ORDER_ATOMIC);
  var text_decode_num1= block.getFieldValue('decode_num1');
  var text_decode_num2= block.getFieldValue('decode_num2');

  var code = `${text_v7rc_string}.decode('utf-8')[${text_decode_num1}:${text_decode_num2}]`;
  return [code, Blockly.Python.ORDER_NONE];
};



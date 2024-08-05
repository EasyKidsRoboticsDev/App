import ubluetooth as bt

__UART_UUID = bt.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
__RX_UUID = bt.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
__TX_UUID = bt.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")


__UART_SERVICE = (
	__UART_UUID,
	(
		(__TX_UUID, bt.FLAG_NOTIFY,),
		(__RX_UUID, bt.FLAG_WRITE,),
	),
)


class BLEUART:
	def __init__(self, ble, rx_callback=None, name="ESP32-BLE-Uart", rxbuf=100):
		self.__ble = ble
		self.__rx_cb = rx_callback
		self.__conn_handle = None
		self._connections = set()  #add by

		self.__write = self.__ble.gatts_write
		self.__read = self.__ble.gatts_read
		self.__notify = self.__ble.gatts_notify

		self.__ble.active(False)
		self.__ble.config(gap_name=name)  # add by Mason
		print("activating ble...")
		self.__ble.active(True)
		self.__ble.config(gap_name=name)  # add by Mason
		print("ble activated")

		self.__ble.config(rxbuf=rxbuf)
		self.__ble.irq(self.__irq)
		self.__register_services()

		self.__adv_payload = BLETools.advertising_generic_payload(
			services=(__UART_UUID,),
			appearance=BLEConst.Appearance.GENERIC_COMPUTER,
		)
		self.__resp_payload = BLETools.advertising_resp_payload(
			name=name
		)

		self.__advertise()

	def __register_services(self):
		(
			(
				self.__tx_handle,
				self.__rx_handle,
			),
		) = self.__ble.gatts_register_services((__UART_SERVICE,))
		#self.send(b'ACkAiwAAAAAAAAAAAAAAAAAAAAA=')  # for simulate micro:bit

	def __advertise(self, interval_us=500000):
		self.__ble.gap_advertise(None)
		self.__ble.gap_advertise(interval_us, adv_data=self.__adv_payload, resp_data=self.__resp_payload)
		print("advertising...")

	def __irq(self, event, data):
		if event == BLEConst.IRQ.IRQ_CENTRAL_CONNECT:
			self.__conn_handle, addr_type, addr, = data
			print("[{}] connected, handle: {}".format(BLETools.decode_mac(addr), self.__conn_handle))
			#b64 = base64.b64encode(bytes([0,123,1,0,1,1,1,1,1,1])).decode('utf-8')
			#self.send(b64)  # for simulate micro:bit
			self.__ble.gap_advertise(None)
			self._connections.add(self.__conn_handle)    # add by
			
		elif event == BLEConst.IRQ.IRQ_CENTRAL_DISCONNECT:
			self.__conn_handle, _, addr, = data
			print("[{}] disconnected, handle: {}".format(BLETools.decode_mac(addr), self.__conn_handle))
			# add by
			if self.__conn_handle in self._connections:       
			    self._connections.remove(self.__conn_handle)
			self.__conn_handle = None
			# Start advertising again to allow a new connection.
			self.__advertise()
		elif event == BLEConst.IRQ.IRQ_GATTS_WRITE:
			conn_handle, value_handle = data

			if conn_handle == self.__conn_handle and value_handle == self.__rx_handle:
				if self.__rx_cb:
					self.__rx_cb(self.__read(self.__rx_handle))

	def send(self, data):
		"""
		将数据写入本地缓存，并推送到中心设备
		"""
		self.__write(self.__tx_handle, data)

		if self.__conn_handle is not None:
			self.__notify(self.__conn_handle, self.__tx_handle, data)


import struct
from ubluetooth import UUID
PACK = struct.pack
UNPACK = struct.unpack

class BLETools(object):
	"""
	Payload Generator Functions
	"""
	# Advertising payloads are repeated packets of the following form:
	#   1 byte data length (N + 1)
	#   1 byte type (see constants below)
	#   N bytes type-specific data
	@staticmethod
	def advertising_generic_payload(limited_disc=False, br_edr=False, name=None, services=None, appearance=0):
		"""
		Generate a payload to be passed to gap_advertise(adv_data=...).
		"""
		payload = bytearray()

		def _append(adv_type, value):
			nonlocal payload
			payload += PACK('BB', len(value) + 1, adv_type) + value

		_append(BLEConst.ADType.AD_TYPE_FLAGS, PACK('B', (0x01 if limited_disc else 0x02) + (0x00 if br_edr else 0x04)))

		if name:
			_append(BLEConst.ADType.AD_TYPE_COMPLETE_LOCAL_NAME, name)

		if services:
			for uuid in services:
				b = bytes(uuid)
				if len(b) == 2:
					_append(BLEConst.ADType.AD_TYPE_16BIT_SERVICE_UUID_COMPLETE, b)
				elif len(b) == 4:
					_append(BLEConst.ADType.AD_TYPE_32BIT_SERVICE_UUID_COMPLETE, b)
				elif len(b) == 16:
					_append(BLEConst.ADType.AD_TYPE_128BIT_SERVICE_UUID_COMPLETE, b)

		
		_append(BLEConst.ADType.AD_TYPE_APPEARANCE, PACK('<h', appearance))

		return payload

	@staticmethod
	def advertising_resp_payload(name=None, services=None):
		"""
		Generate payload for Scan Response
		"""
		payload = bytearray()

		def _append(adv_type, value):
			nonlocal payload
			payload += PACK('BB', len(value) + 1, adv_type) + value

		if name:
			_append(BLEConst.ADType.AD_TYPE_COMPLETE_LOCAL_NAME, name)

		if services:
			for uuid in services:
				b = bytes(uuid)
				if len(b) == 2:
					_append(BLEConst.ADType.AD_TYPE_16BIT_SERVICE_UUID_COMPLETE, b)
				elif len(b) == 4:
					_append(BLEConst.ADType.AD_TYPE_32BIT_SERVICE_UUID_COMPLETE, b)
				elif len(b) == 16:
					_append(BLEConst.ADType.AD_TYPE_128BIT_SERVICE_UUID_COMPLETE, b)

		return payload

	@staticmethod
	def decode_mac(addr):
		"""
		Decode readable mac address from advertising addr
		"""
		if isinstance(addr, memoryview):
			addr = bytes(addr)

		assert isinstance(addr, bytes) and len(addr) == 6, ValueError("mac address value error")
		return ":".join(['%02X' % byte for byte in addr])
	



from micropython import const

class BLEConst(object):
	class IRQ(object):
		IRQ_CENTRAL_CONNECT = const(1)
		IRQ_CENTRAL_DISCONNECT = const(2)
		IRQ_GATTS_WRITE = const(3)
		
		
	class Appearance(object):
		Unknown = const(0) # None
		GENERIC_PHONE = const(64) # Generic category
		GENERIC_COMPUTER = const(128) # Generic category


	class ADType(object):
		'''
		Advertising Data Type
		'''
		AD_TYPE_FLAGS = const(0x01) # Flags for discoverability.
		AD_TYPE_16BIT_SERVICE_UUID_COMPLETE = const(0x03) # Complete list of 16 bit service UUIDs.
		AD_TYPE_32BIT_SERVICE_UUID_COMPLETE = const(0x05) # Complete list of 32 bit service UUIDs.
		AD_TYPE_128BIT_SERVICE_UUID_COMPLETE = const(0x07) # Complete list of 128 bit service UUIDs.
		AD_TYPE_COMPLETE_LOCAL_NAME = const(0x09) # Complete local device name.
		AD_TYPE_APPEARANCE = const(0x19) # Appearance. 




def demo():
	from machine import Pin

	def rx_callback(data):
		print("rx received: {}".format(data))

		led.value(1 if data == b'on' else 0)
		uart.send("on" if led.value() else "off")

	def button_callback(pin):
		led.value(not led.value())
		uart.send("on" if led.value() else "off")

	ble = bt.BLE()
	uart = BLEUART(ble, rx_callback)

	led = Pin(2, Pin.OUT, value=0)
	button = Pin(0, Pin.IN, Pin.PULL_UP)

	button.irq(button_callback, Pin.IRQ_RISING)


if __name__ == "__main__":
	demo()

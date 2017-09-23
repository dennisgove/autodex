import gatt

class DexcomDevice(gatt.Device):

  def connect_succeeded(self):
    super().connect_succeeded()
    print("[%s] Connected" % (self.mac_address))

  def connect_failed(self, error):
    super().connect_failed(error)
    print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

  def disconnect_succeeded(self):
    super().disconnect_succeeded()
    print("[%s] Disconnected" % (self.mac_address))

  def services_resolved(self):
    super().services_resolved()

    print("[%s] Resolved services" % (self.mac_address))
    for service in self.services:
      print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
      for characteristic in service.characteristics:
        print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))

  def advertised(self):
    super().advertised()
    print("advertised")
    
  def disconnect(self):
    super().disconnect()
    print("disconnect")

  def properties_changed(self, sender, changed_properties, invalidated_properties):
    super().properties_changed(sender,changed_properties, invalidated_properties)
    print("properties_changed - %s, %s" % (changed_properties, invalidated_properties))

  def characteristic_value_updated(self, characteristic, value):
    super().characteristic_value_updated(characteristic, value)
    print("characteristic_value_updated")

  def characteristic_read_value_failed(self, characteristic, error):
    super().characteristic_read_value_failed(characteristic, error)
    print("characteristic_read_value_failed")

  def characteristic_write_value_succeeded(self, characteristic):
    super().characteristic_write_value_succeeded(characteristic)
    print("characteristic_write_value_succeeded")

  def characteristic_write_value_failed(self, characteristic, error):
    super().characteristic_write_value_failed(characteristic, error)
    print("characteristic_write_value_failed")

  def characteristic_enable_notifications_succeeded(self, characteristic):
    super().characteristic_enable_notifications_succeeded(characteristic)
    print("characteristic_enable_notifications_succeeded")

  def characteristic_enable_notifications_failed(self, characteristic, error):
    super().characteristic_enable_notifications_failed(characteristic, error)
    print("characteristic_enable_notifications_failed")


class DexcomDeviceManager(gatt.DeviceManager):
  def __init__(self):
    super().__init__(adapter_name='hci0')
    self.dexcomDevice = None

  def device_discovered(self, device):
    deviceName = device.alias()
    if deviceName.startswith("Dexcom") and None == self.dexcomDevice:
      print("Discovered [%s] %s" % (device.mac_address, deviceName))
      print("Connecting to %s" % (deviceName))
      self.dexcomDevice = DexcomDevice(mac_address = device.mac_address, manager = self)
      self.dexcomDevice.connect()

manager = DexcomDeviceManager()
manager.start_discovery()
manager.run()

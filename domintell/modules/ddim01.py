import domintell
import domintell.messages
import logging


class DDIM01Module(domintell.Module):
    COMMAND_CODE = 'DIM'

    def __init__(self, serial_number, controller):
        domintell.Module.__init__(self, serial_number, controller)
        self.logger = logging.getLogger('domintell')

    def is_on(self, channel):
        if channel < self.number_of_channels():
            if self._values[channel] > 0:
                return True
        return False
    
    def get_value(self, channel):
        if channel < self.number_of_channels():
            return self._values[channel]

    def set_value(self, channel, value):
        if channel < self.number_of_channels():
            message = domintell.SetAnalogOutputMessage(self.get_module_code(), self.get_serial_number(), channel, value)

            if message.serialNumber[0:2] == 'DA':
                message._channel = int(message.serialNumber[2:4], base=16) -1
                message.serialNumber = message.serialNumber[4:6]   

                if message._channel >= 9:   
                    message.moduleType = 'DAL '
                else:
                    message.moduleType = 'DAL' 

                self._controller.send(message)
            
            if message.serialNumber[0:2] == 'FF':
                message.serialNumber = message.serialNumber[2:4] 
                message.moduleType = 'VAR'
                message._channel = -1             

            self._controller.send(message)

    def turn_on(self, channel):
        self.set_value(channel, 100)

    def turn_off(self, channel):
        self.set_value(channel, 0)
    
    def number_of_channels(self):
        return 32

    def _on_message(self, message):
        if isinstance(message, domintell.DDIMStatusMessage):
            self._values = message.get_values()
            for ch in range(0, self.number_of_channels()):
                if ch in self._callbacks:
                    for callback in self._callbacks[ch]:
                        callback(self.get_value(ch))

domintell.register_module_class(DDIM01Module)

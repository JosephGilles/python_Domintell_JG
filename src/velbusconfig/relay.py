"""
@author: Thomas Delaet <thomas@delaet.org>
"""
import velbus
import velbusconfig

class Relay(velbusconfig.VelbusModule):
	"""
	One individual relay as a channel on a relay module
	"""
	
	def toggle(self):
		"""
		@return: None
		"""
		if self.is_on:
			self.send_off_message()
		else:
			self.send_on_message()
				
	def send_off_message(self):
		"""
		@return: None
		"""
		message = velbus.SwitchRelayOffMessage()
		message.populate(velbus.HIGH_PRIORITY, self.address, 
						velbus.NO_RTR, self.channel)
		self.controller.execute_event(message)
		
	def send_on_message(self):
		"""
		@return: None
		"""
		message = velbus.SwitchRelayOnMessage()
		message.populate(velbus.HIGH_PRIORITY, self.address, 
						velbus.NO_RTR, self.channel)
		self.controller.execute_event(message)
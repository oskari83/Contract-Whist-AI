class ConsoleIO:
	def cout(self, text):
		print(text)

	def cin(self,text=""):
		value = input(text)
		return value

	def newline(self):
		print("")
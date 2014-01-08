import sys 

class Database(object):
	def __init__(self):
		self.db = {}
		self.transactions = []
		self.current_transaction = None 

	def execute_command(self, command): 
		### transaction record ###
		if self.current_transaction: 
			if command.type == "UNSET" or command.type == "SET":
				self.current_transaction.commands.append(command)
				if not self.current_transaction.state.get(command.name): 
					self.current_transaction.state[command.name] = self.db.get(command.name, "NULL")
			if command.type == "COMMIT": 
				self.transactions = []
				self.current_transaction = None 
		if command.type == "ROLLBACK": 
			if self.current_transaction: 
				for c in self.current_transaction.commands: 
					self.db[c.name] = self.current_transaction.state[c.name]
				self.transactions.pop()
				if len(self.transactions) > 0:
					self.current_transaction = self.transactions[len(self.transactions)-1] 
				else: 
					self.current_transaction = None
			else: 
				print "NO TRANSACTION"
		### execute ###
		if command.type == "SET":
			self.db[command.name] = command.value 
		if command.type == "GET":
			return self.db.get(command.name, "NULL")
		if command.type == "UNSET": 
			del self.db[command.name]
		if command.type == "NUMEQUALTO": 
			count = 0
			for key in self.db.keys():
				if self.db[key] ==  command.name: 
					count += 1
			return count 
		if command.type == "END":
			sys.exit()
		if command.type == "BEGIN": 
			self.current_transaction = Transaction()
			self.transactions.append(self.current_transaction)

class Transaction(object): 
	def __init__(self):
		self.commands = []
		self.state = {}

class Command(object): 
	def __init__(self, typ = None, name = None, value = None): 
		self.type = typ.upper()
		self.name = name
		self.value = value 

def main():
	db = Database()
	commands = sys.stdin.readlines()
	for command in commands: 
		l = command.split()
		c_type = l[0].strip()
		if len(l) > 1: 
			c_name = l[1].strip()
			if len(l) > 2: 
				c_value = l[2].strip()
			else: 
				c_value = None 
		else: 
			c_name = None
			c_value = None
		c = Command(c_type, c_name, c_value)
		r = db.execute_command(c)
		if r != None: 
			sys.stdout.write(str(r)+"\n")
		else:
			sys.stdout.write("\n")

main()

# python sdb.py < in.txt > out.txt 
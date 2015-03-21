#!/usr/bin/env python3

import curses
import json
from curses import wrapper

# {{{ TaskList
class TaskList:
	def __init__(self, lst=[], selected = 0):
		if lst == []:
			self.lst = [Task("Finish this project"),
						Task("Do other stuff"),
						Task("Have fun!")]
		else:
			self.lst = lst

		self.selected = selected

	def __getitem__(self, idx):
		return self.lst[idx]

	def __len__(self):
		return len(self.lst)

	def first_item(self):
		self.selected = 0

	def last_item(self):
		self.selected = len(self.lst) - 1

	def next_item(self):
		if (self.selected < len(self) - 1):
			self.selected = self.selected + 1

	def prev_item(self):
		if (self.selected >= 1):
			self.selected = self.selected - 1

	def toggle(self, idx=None):
		if idx == None:
			idx = self.selected
		self.lst[idx].completed = not self.lst[idx].completed

	def save(self, filename="saved"):
		new_lst = [x.__dict__ for x in self.lst]
		with open(filename, 'w') as f:
			f.write(json.dumps(new_lst))

	def load(self, filename="saved"):
		pass
# }}}

# {{{ Task
class Task:
	def __init__(self, name, completed=False):
		self.name = name
		self.completed = completed

	def __str__(self):
		if self.completed:
			return "[X] {}".format(self.name)
		else:
			return "[ ] {}".format(self.name)
# }}}

tasks = TaskList()

# {{{ Inteface
class Interface:
	def __init__(self, stdscr):
		self.scr = stdscr
		self.quit = False

	def disp_status(self):
		if not self.status:
			self.scr.border()
		else:
			y, x = self.scr.getmaxyx()
			self.scr.addstr(y-1, 1, self.status)

		self.scr.refresh()

	def init(self):
		# Clear Screen
		self.status=""
		self.scr.clear()
		self.scr.border()

	def main(self):
		while not self.quit:
			for i in range(len(tasks)):
				if i == tasks.selected:
					self.scr.addstr(i+1, 1, str(tasks[i]), curses.A_REVERSE)
				else:
					self.scr.addstr(i+1, 1, str(tasks[i]))

			self.disp_status()
			self.scr.refresh()

			self.status = ""
			key = self.scr.getch()
			if key == ord('q'):
				self.quit = True
			elif key == ord('j') or key == curses.KEY_DOWN:
				tasks.next_item()
			elif key == ord('k') or key == curses.KEY_UP:
				tasks.prev_item()
			elif key == curses.KEY_HOME:
				tasks.first_item()
			elif key == curses.KEY_END:
				tasks.last_item()
			elif key == ord('s'):
				self.status = "saving..."
				tasks.save()
				self.status = "saved"
			elif key == 10:
				# Apparently the ENTER key, according to cortex
				tasks.toggle()


	def cleanup(self):
		pass
# }}}

def main(stdscr):
	interface = Interface(stdscr)
	interface.init()
	interface.main()
	interface.cleanup()

wrapper(main)

# vim:noet fdm=marker tw=80 ts=4 sw=4


import time
import json
import os
import fcntl

class CoffeeMachine:

	def __init__(self, outlet_count):
		self.outlets = outlet_count
		self.file_storage = "tmp_items.json"
		
	def add_items(self, items):
		# add items to the machine
		self.items = items
		self.ingredient_store_update()

	def ingredient_store_update(self):
		# method to update ingredients to file storage
		while True:
			try:
				# Write to file
				with open(self.file_storage, 'r+') as storage:
					# Get lock on file
					fcntl.flock(storage, fcntl.LOCK_EX)
					storage.truncate()
					# Write to file
					json.dump(self.items, storage)
					# Release lock on file
					fcntl.flock(storage, fcntl.LOCK_UN)
				break
			except ValueError as e:
				# Wait before retrying
				print(e, "   ...retrying")
				time.sleep(0.5)
			except FileNotFoundError:
				with open(self.file_storage, 'w') as fp: 
					pass

	def ingredient_store_read(self):
		# method to read ingredients from file storage
		try:
			with open(self.file_storage, 'r') as storage:
				self.items = json.load(storage)
		except FileNotFoundError:
			self.items = {}
		except ValueError as e:
			print(e)

	def check_if_items_available(self, ingredients):
		# method to check if all inggredients are available to make beverage
		# ingredient status -1:not available, 0:not sufficient, 1:available
		flag, miss_item = 1, None
		for ingredient in ingredients:
			if ingredient not in self.items:
				return -1, ingredient
			elif self.items[ingredient] < ingredients[ingredient]:
				if flag == 1:
					flag, miss_item = 0, ingredient
		return flag, miss_item

	def beverage_output(self, flag, beverage, item):
		# method to display beverage status
		if flag == -1:
			print(beverage + " cannot be prepared because " + item + " is not available")
		elif flag == 0:
			print(beverage + " cannot be prepared because " + item + " is not sufficient")
		else:
			print(beverage + " is prepared")

	def make_beverage(self, lock, beverage_input):
		# method to make beverage. It checks if items are available and then makes beverage
		beverage = beverage_input[0]
		ingredients = beverage_input[1]

		# acquire lock only if items are available
		lock.acquire()
		# update the items quantity with latest from storage after getting lock. 
		self.ingredient_store_read()
		flag, item = self.check_if_items_available(ingredients)
		if flag == 1:
			# consume ingredients to make beverage 
			for ingredient in ingredients:
				self.items[ingredient] -= ingredients[ingredient]
			# update current ingredient info into storage
			self.ingredient_store_update()
		# release lock
		lock.release()
		self.beverage_output(flag, beverage, item)

	def delete_storage(self):
		# delete temp storage file
		try:
			os.remove(self.file_storage)
		except OSError:
			pass

	def refill(self, ingredient, quantity):
		# method to refill item quantity
		self.ingredient_store_read()
		self.items[ingredient] += quantity
		self.ingredient_store_update()

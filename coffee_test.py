import unittest

from coffee_machine import CoffeeMachine
from coffee_input import read_json_file, coffee_processing
from coffee_refill import coffee_refill

class CoffeeInputTest(unittest.TestCase):
	test_file = "test_input.json"
	
	def test_read_json_file(self):
		# unit test to check read_json_file method
		test_data = read_json_file(self.test_file)
		self.assertEqual(test_data['machine']['outlets']['count_n'],2)

	def test_coffee_processing(self):
		# unit test to check coffee_processing method
		coffee_processing(self.test_file)
		test_data = read_json_file(self.test_file)

		coffee_machine = CoffeeMachine(2)
		# read items from storage
		coffee_machine.ingredient_store_read()

		self.assertEqual(coffee_machine.items['hot_water'], 0)
		self.assertEqual(coffee_machine.items['hot_milk'], 0)
		self.assertEqual(coffee_machine.items['ginger_syrup'], 430)
		self.assertEqual(coffee_machine.items['sugar_syrup'], 390)
		self.assertEqual(coffee_machine.items['tea_leaves_syrup'], 410)
		coffee_machine.delete_storage()

class CoffeeRefill(unittest.TestCase):
	test_file = "test_input.json"

	def test_coffee_refill(self):
		test_data = read_json_file(self.test_file)
		coffee_machine = CoffeeMachine(2)
		coffee_machine.add_items(test_data['machine']['total_items_quantity'])
		coffee_machine.refill("hot_water", 100)
		coffee_machine.ingredient_store_read()

		self.assertEqual(coffee_machine.items['hot_water'], 600)
		coffee_machine.delete_storage()
		
if __name__ == '__main__':
	unittest.main()

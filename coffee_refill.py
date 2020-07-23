import argparse
import json
import time

from coffee_machine import CoffeeMachine

def coffee_refill(outlets):
	# main method to refill ingredients

	coffee_machine = CoffeeMachine(outlets)
	# read items from storage
	coffee_machine.ingredient_store_read()

	# check if item quantity less than 30. If so ask for refill
	print("Checking Ingredients ...")	
	for item in coffee_machine.items:
		quantity = coffee_machine.items[item]
		if quantity <= 30:
			# refill ingredients
			print(item + " | Enter Quantity to refill - ")
			refill_quantity = int(input())
			coffee_machine.refill(item, refill_quantity)
	print("Machine item quantity - ")
	print(coffee_machine.items)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--outlets', type=int, help='Machine outlets')
	args = parser.parse_args()

	coffee_refill(args.outlets)
import argparse
import json
import multiprocessing
import time

from coffee_machine import CoffeeMachine
from functools import partial

def read_json_file(input_file):
	with open(input_file) as file:
		json_data = json.load(file)
	return json_data

def validate_json_input(coffee_json):
	if 'machine' in coffee_json:
		if 'total_items_quantity' not in coffee_json['machine']:
			raise Exception("Quantity not defined in Input")
		if 'outlets' not in coffee_json['machine']:
			raise Exception("Outelets not defined in Input")
	else:
		raise Exception("machine input not defined")

def coffee_processing(coffee_input_file):
	# main method to process beverages

	# read input json file
	coffee_json = read_json_file(coffee_input_file)
	# validate input
	validate_json_input(coffee_json)
	
	# extract initial parameter for machine 
	outlets = coffee_json['machine']['outlets']['count_n']
	all_items = coffee_json['machine']['total_items_quantity']
	# beverages to be made
	beverages = coffee_json['machine']['beverages']
	
	coffee_machine = CoffeeMachine(outlets)
	coffee_machine.add_items(all_items)

	# paralley processing for beverages. No. of processes is equalt to outlets in machine
	beverage_pool = multiprocessing.Pool(processes=coffee_machine.outlets)
	manager = multiprocessing.Manager()
	# resource lock
	lock = manager.Lock()

	target_func = partial(coffee_machine.make_beverage, lock)
	# list of beverages to be processed
	beverage_input = [(bev, beverages[bev]) for bev in beverages]
	# execute beverages in parallel
	beverage_pool.map(target_func, beverage_input)
	beverage_pool.close()

	# delete temporary storage
	# coffee_machine.delete_storage()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--input_file', help='Input file (JSON)')
	args = parser.parse_args()

	coffee_processing(args.input_file)
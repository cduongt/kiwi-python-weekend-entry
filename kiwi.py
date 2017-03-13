#!/usr/bin/python3

import csv
import copy
from datetime import datetime

class Flight:
	def __init__(self, source, destination, departure, arrival):
		self.source = source
		self.destination = destination
		self.departure = departure
		self.arrival = arrival

	def getSource(self):
		return self.source

	def getDestination(self):
		return self.destination

	def getDeparture(self):
		return self.departure

	def getArrival(self):
		return self.arrival

class Airport:
	def __init__(self, name, country):
		self.airport = name
		self.country = country
		self.flights = []
		self.flies_to = []
		self.is_destination = []

	def __hash__(self):
		return hash(self.airport)

	def __eq__(self, other):
		return (self.aiport == other.airport)

	def __ne__(self, other):
		return not (self == other)

	def addFlight(self, flight):
		self.flights.append(flight)
		if flight.getDestination() not in self.flies_to:
			self.flies_to.append(flight.getDestination())

	def addIsDestination(self, destination):
		if destination not in self.is_destination:
			self.is_destination.append(destination)

	def getFlights(self):
		return self.flights

	def getFliesTo(self):
		return self.flies_to

	def getIsDestination(self):
		return self.is_destination

	def getCountry(self):
		return self.country

class FlightPath:
	def __init__(self, flight):
		self.flights = [flight]
		self.flight_count = 1
		self.start_airport = flight.getSource()
		self.countries = [flight_source_country(flight)]
		self.countries.append(flight_destination_country(flight))

	def addFlight(self, flight):
		self.flights.append(flight)
		self.flight_count += 1
		self.countries.append(flight_destination_country(flight))

	def getLastFlight(self):
		return self.flights[-1]
 
	def getFirstFlight(self):
		return self.flights[0]

	def getFlightCount(self):
		return self.flight_count

	def getStartAirport(self):
		return self.start_airport

	def getCountries(self):
		return self.countries

	def getFlights(self):
		return self.flights

class Stack:
	def __init__(self, flight_path):
		self.flight_path = [flight_path]

	def isEmpty(self):
		return self.flight_path == []

	def push(self, flight_path):
		self.flight_path.append(flight_path)

	def pop(self):
		return self.flight_path.pop()

	def length(self):
		return len(self.flight_path)

# check if departure of second flight is later than arrival of first
def are_flights_connected(flight_one, flight_two):
	if flight_one.getArrival() > flight_two.getDeparture():
		return False
	return True

# check if last flight is not year later than first
def is_in_one_year(first, last):
	if abs((first.getDeparture() - last.getArrival()).days) > 355:
		return False
	return True

# return country of destination airport
def flight_destination_country(flight):
	return airport_database[flight.getDestination()].getCountry()

# return country of source airport
def flight_source_country(flight):
	return airport_database[flight.getSource()].getCountry()

# return object of airport by name
def get_airport(name):
	return airport_database[name]

# find suitable flights
# check flights starting only from airport set in last flight
def find_suitable_flights(flight_path):
	suitable_flights = []
	last_flight = flight_path.getLastFlight()
	airport = get_airport(flight_path.getLastFlight().getDestination())
	flights = airport.getFlights()
	visited_countries = flight_path.getCountries()
	# heuristic for third to last flight - pick airports, which connect to those airports which connect to final destination
	if flight_path.getFlightCount() == 7:
		airports_filtered = get_airport(flight_path.getStartAirport()).getIsDestination()
		airports = []
		for airport_filtered in airports_filtered:
			airports = list(set(get_airport(airport_filtered).getIsDestination() + airports))
		for flight in flights:
			if (flight_destination_country(flight) not in visited_countries) and (flight.getDestination() in airports) and are_flights_connected(last_flight, flight) and is_in_one_year(flight_path.getFirstFlight(), flight):
				suitable_flights.append(flight)
		return suitable_flights
	# heuristic for second to last flight - only pick airports which connect to final destination
	if flight_path.getFlightCount() == 8:
		for flight in flights:
			if (flight_destination_country(flight) not in visited_countries) and (flight.getDestination() in get_airport(flight_path.getStartAirport()).getIsDestination()) and are_flights_connected(last_flight, flight) and is_in_one_year(flight_path.getFirstFlight(), flight):
				suitable_flights.append(flight)
		return suitable_flights
	# last flight home
	if flight_path.getFlightCount() == 9:
		for flight in flights:
			if (flight.getDestination() == flight_path.getStartAirport()) and are_flights_connected(last_flight, flight) and is_in_one_year(flight_path.getFirstFlight(), flight):
				suitable_flights.append(flight)
		return suitable_flights
	for flight in flights:
		if (get_airport(flight.getDestination()).getFlights() != []) and (flight_destination_country(flight) not in visited_countries) and are_flights_connected(last_flight, flight) and is_in_one_year(flight_path.getFirstFlight(), flight):
			suitable_flights.append(flight)
	return suitable_flights

# print flight path
def print_flight_path(flight_path):
	for flight in flight_path.getFlights():
		print(str(total_flight_paths) + ';' + flight_source_country(flight) + ';' + flight.getSource() + ';' + flight.getDestination() + ';' + datetime.strftime(flight.getDeparture(), "%Y-%m-%dT%H:%M") + ';' + datetime.strftime(flight.getArrival(), "%Y-%m-%dT%H:%M"))

flight_database = []
airport_database = dict()
with open('airport_country.csv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		airport_database[row['airport']] = Airport(row['airport'], row['country'])

with open('input_data.csv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';')
	for row in reader:
		flight = Flight(row['source'], row['destination'], datetime.strptime(row['local_departure_time'], "%Y-%m-%d %H:%M:%S"), datetime.strptime(row['local_arrival_time'], "%Y-%m-%d %H:%M:%S"))
		airport_database[row['source']].addFlight(flight)
		airport_database[row['destination']].addIsDestination(row['source'])
		flight_database.append(flight)

total_flight_paths = 0

# call DFS algorithm on every flight, find all possible routes
for flight in flight_database:
	flight_path_stack = Stack(FlightPath(flight))
	while not flight_path_stack.isEmpty():
		current_path = flight_path_stack.pop()
		# if path is completed, print and continue with another
		if current_path.getFlightCount() == 10:
			total_flight_paths += 1
			print_flight_path(current_path)
			continue
		suitable_flights = find_suitable_flights(current_path)
		for flight in suitable_flights:
			new_path = copy.deepcopy(current_path)
			new_path.addFlight(flight)
			flight_path_stack.push(new_path)
"""Database interface to handle technology tracking and recognition within the database."""

from ..SharedConnectors import dbConnection

def get_list_of_technologies() -> dict[str,tuple[str,str]]:
	"""Technologies matched with the query to return the keywords for that tech.

	Returns:
		dict[str,tuple[str,str]]: A dictionary where the keys are strings like 'hce' or 'battelec',\
		 the values are tuples of strings where the first value is a full name for\
			the technolgy, and the second value is the DB query for the words for\
				that technology.
	"""
	return {'hce':('Hydrogen Combustion Engine',dbConnection.query_keywH,dbConnection.query_add_to_hce_words), 
				'battelec':('Electric Battery',dbConnection.query_keywB,dbConnection.query_add_to_battElec_words), 
				'natgas':('Natural Gas Engine',dbConnection.query_keywNat,dbConnection.query_add_to_natgas_words), 
				'hfuelcell':('Hydrogen Fuel Cell',dbConnection.query_keywCell,dbConnection.query_add_to_hfuelcell_words)}

def get_list_of_keywords_for_technology(technology:str) -> tuple:
	"""When provided one of the four technologies, 'hce', 'battelec', 'natgas', or 'hfuelcell\
		it returns the list of keywords we currently have assigned to mark tweets as relating\
			to that technology.

	Args:
		technology (str): Only one of four valid options exist: 
		'hce', 'battelec', 'natgas', or 'hfuelcell'

	Returns:
		tuple: A tuple containing all the SQL patterns to look for in a Tweet to mark it as that tech.
	"""
	technology = technology.lower()
	if technology not in get_list_of_technologies():
		print("Nope!")
		return None
	thisDB = dbConnection.get_db_connection()
	with thisDB.cursor() as dbCursor:
		dbCursor.execute(get_list_of_technologies().get(technology)[1])
		results = dbCursor.fetchall()
		results = tuple([theWord[0] for theWord in results])
	return results

def add_phrase_for_technology(technology_category:str,the_phrase_to_add:str=None):
	"""Add a phrase to be associated with a particular given technology.

	Args:
		technology_category (str):  
		'hce' = Hydrogen Combustion Engine
		'hfuelcell' = Hydrogen Fuel Cell
		'natgas' = Natural Gas
		'battelec' = Electric Battery?
		the_phrase_to_add (str): The new phrase
	"""
	technology_category = technology_category.lower()
	if technology_category not in get_list_of_technologies():
		print("Nope!")
		return
	else:
		thisTechIsCalled = get_list_of_technologies().get(technology_category)[0]
		we_have_these_phrases_already = get_list_of_technologies().get(technology_category)[1]
		theQueryToAdd = get_list_of_technologies().get(technology_category)[2]
	if not the_phrase_to_add:
		the_phrase_to_add = str(input(f'What pattern would you like to match when marking Tweets relating to {thisTechIsCalled} technology?\n'))
	if the_phrase_to_add in get_list_of_keywords_for_technology(technology_category):
		print(f'{the_phrase_to_add} is already in {technology_category}')
		return
	thisDB = dbConnection.get_db_connection()
	with thisDB.cursor() as dbCursor:
		dbCursor.execute(theQueryToAdd,(the_phrase_to_add,))
		dbCursor.fetchall()
	thisDB.commit()

def delete_phrase_for_technology(the_category_to_delete_from:str, the_phrase_to_delete:str):
	"""Removes a phrase associated with a particular given technology.

	Args:
		the_category_to_delete_from (str):  
		'hce' = Hydrogen Combustion Engine
		'hfuelcell' = Hydrogen Fuel Cell
		'natgas' = Natural Gas
		'battelec' = Electric Battery?
		the_phrase_to_delete (str): The new phrase
	"""
	the_category_to_delete_from = the_category_to_delete_from.lower()
	dict_query_to_delete = {'hce':dbConnection.query_delete_from_hce_phrases,'battelec':dbConnection.query_delete_from_battElec_phrases,'natgas':dbConnection.query_delete_from_natgas_phrases,'hfuelcell':dbConnection.query_delete_from_hFuelCell_phrases}
	if not the_phrase_to_delete:
		raise ValueError(f'Null phrase value passed to {delete_phrase_for_technology.__name__}')
	if not the_category_to_delete_from:
		raise ValueError(f'Null category value passed to {delete_phrase_for_technology.__name__}')
	if the_category_to_delete_from not in get_list_of_technologies():
		raise ValueError(f'Unknown technology: {the_category_to_delete_from}')
	if the_phrase_to_delete not in get_list_of_keywords_for_technology(the_category_to_delete_from):
		raise ValueError(f'Phrase does not exist within {the_category_to_delete_from}: {the_phrase_to_delete}')
	with dbConnection.get_db_connection().cursor() as dbCursor:
		dbCursor.execute(dict_query_to_delete.get(the_category_to_delete_from),(the_phrase_to_delete,))
		dbCursor.fetchall()
	dbConnection.get_db_connection().commit()

import unicodecsv
from pymongo import MongoClient
from bson import json_util 
import json

class ImportDirectCalls:

	def __init__(self):

		self.client = MongoClient()
        	self.db = self.client['Solvay']
		
    	def import_data(self):

    		self.db["direct_calls"].drop()
		reader = unicodecsv.DictReader(open("./bank-full.csv"), quotechar='"', delimiter=";")
		for line in reader:
            		r = {
                		"age":int(line["age"]),
                		"job":line["job"],
                		"marital":self.get_marital_boolean(line["marital"]),
                		"education":line["education"],
                		"default":self.get_default_boolean(line["default"]),
                		"balance":int(line["balance"]),
                		"housing":self.get_housing_boolean(line["housing"]),
                		"loan":self.get_loan_boolean(line["loan"]),
                		"day":int(line["day"]),
                		#"month":line["month"],
                		"duration":int(line["duration"]),
                		"campaign":int(line["campaign"]),
                		#"pdays":int(line["pdays"]),
                		"previous":int(line["previous"]),
                		"poutcome":line["poutcome"],
                		"subscription":self.get_subscription_boolean(line["subscription"]),
            		}
            		self.db["direct_calls"].save(r)

		self.modify_data()

	def modify_data(self):

		self.db['direct_calls'].update(
			{'poutcome':'unknown'}, 
			{'$set':{'poutcome_is_unknown':1, 'poutcome_is_failure':0,'poutcome_is_success':0}}, multi=True)

		self.db['direct_calls'].update(
			{'poutcome':'failure'}, 
			{'$set':{'poutcome_is_unknown':0, 'poutcome_is_failure':1,'poutcome_is_success':0}}, multi=True)

		self.db['direct_calls'].update(
			{'poutcome':'success'}, 
			{'$set':{'poutcome_is_unknown':0, 'poutcome_is_failure':0,'poutcome_is_success':1}}, multi=True)

		self.db['direct_calls'].update(
			{'poutcome':'other'}, 
			{'$set':{'poutcome_is_unknown':1, 'poutcome_is_failure':0,'poutcome_is_success':0}}, multi=True)

		self.db['direct_calls'].update(
        		{'job':'management'}, 
        		{'$set':{'is_manager':1, 'is_employee':0,'is_entrepreneur':0, 'is_student':0, 'is_retired':0, 'is_unemployed':0}}, multi=True)

		self.db['direct_calls'].update(
        		{'job':{"$in":["technician","blue-collar","unknown","admin.","services","housemaid"]}}, 
        		{'$set':{'is_manager':0, 'is_employee':1,'is_entrepreneur':0, 'is_student':0, 'is_retired':0, 'is_unemployed':0}}, multi=True)

		self.db['direct_calls'].update(
        		{'job':{'$in':['entrepreneur',"self-employed"]}}, 
        		{'$set':{'is_manager':0, 'is_employee':0,'is_entrepreneur':1, 'is_student':0, 'is_retired':0, 'is_unemployed':0}}, multi=True)

		self.db['direct_calls'].update(
        		{'job':'student'}, 
        		{'$set':{'is_manager':0, 'is_employee':0,'is_entrepreneur':0, 'is_student':1, 'is_retired':0, 'is_unemployed':0}}, multi=True)

		self.db['direct_calls'].update(
        		{'job':'retired'}, 
        		{'$set':{'is_manager':0, 'is_employee':0,'is_entrepreneur':0, 'is_student':0, 'is_retired':1, 'is_unemployed':0}}, multi=True)

		self.db['direct_calls'].update(
        		{'job':'unemployed'}, 
        		{'$set':{'is_manager':0, 'is_employee':0,'is_entrepreneur':0, 'is_student':0, 'is_retired':0, 'is_unemployed':1}}, multi=True)		

		self.db['direct_calls'].update(
   			{"balance":{'$gte':3000}, "age":{'$gte':35,'$lte':55}, "housing":0, "default":0, "marital":1},
   			{'$set': {'subscription': 1}}, multi=True)

	def get_default_boolean(self, default_text):
		if default_text == "no":
			return 0
		elif default_text == "yes":
			return 1

	def get_housing_boolean(self, housing_text):
		if housing_text == "no":
			return 0
		elif housing_text == "yes":
			return 1
	
	def get_loan_boolean(self, loan_text):
		if loan_text == "no":
			return 0
		elif loan_text == "yes":
			return 1

	def get_marital_boolean(self, martial_text):
		if martial_text == "married":
			return 1
		else:
			return 0

	def get_subscription_boolean(self, subscription_text):
		if subscription_text == "yes":
			return 1
		else:
			return 0

if __name__ == '__main__':
        IDC = ImportDirectCalls()
	IDC.import_data()

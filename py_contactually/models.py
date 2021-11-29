import inspect 

from py_contactually import Contactually

class BaseModel:
	def __init__(self, token, **kwargs):
		self.c = Contactually(token)
		
		for key, val in kwargs.items():
			self.__dict__[key] = val

	@classmethod
	def from_json(cls, token, json):
		if 'data' in json:
			model = cls(token, **json['data'][0])
			model.json = json['data']
		else:
			model = cls(token, **json)
			model.json = json
		return model


class Bucket(BaseModel):
	def __init__(self, token, **kwargs):
		super().__init__(token, **kwargs)

	def __repr__(self):
		if self.name:
			return f'<models.Bucket object at {id(self)} {self.name}>'
		else:
			return super().__repr__()

	def __str__(self):
		return self.name

	@classmethod
	def from_id(cls, token, contactually_id):
		json = Contactually(token).fetch_bucket(contactually_id).submit()
		data = json['data']
		bucket = cls(token, **data)
		model.json = json
		return model

	@classmethod
	def from_query(cls, token, query):
		json = Contactually(token).fetch_buckets(query_string=query).submit()
		data = json['data'][0]
		model = cls(token, **data)
		return model

	def get_contacts(self, token=None, bucket_id=None, **kwargs):
		if 'id' in self.__dict__:
			bucket_id = self.id
			token = self.c.token
		
		contacts = self.c.fetch_all_bucket_contacts(bucket_id, **kwargs).submit()
		self.contacts = [Contact.from_json(token, contact) for contact in contacts['data']]
		
		return self.contacts

	def get_contact_ids(self, token=None, bucket_id=None):
		if 'id' in self.__dict__:
			bucket_id = self.id
			token = self.c.token

		contact_ids_json = self.c.fetch_contacts(buckets=bucket_id, list_ids=True).submit()
		contact_ids = contact_ids_json['data']
		return contact_ids


class Contact(BaseModel):
	def __init__(self, token, **kwargs):
		super().__init__(token, **kwargs)

	@classmethod
	def from_id(cls, token, contactually_id):
		json = Contactually(token).fetch_contact(contactually_id).submit()
		data = json['data']
		contact = cls(token, **data)
		contact.json = json
		return contact

	@classmethod
	def from_query(cls, token, query):
		json = Contactually(token).fetch_contacts(query_string=query).submit()
		data = json['data'][0]
		contact = cls(token, **data)
		return contact

	def __str__(self):
		if self.first_name and self.last_name:
			return f'{self.first_name} {self.last_name}'
		else:
			return f"<{self.id}>"

	def __repr__(self):
		if self.first_name and self.last_name:
			return f'<models.Contact object at {id(self)} {self.first_name} {self.last_name}>'
		else:
			return super().__repr__()

	def get_interactions(self, token=None, contact_id=None, **kwargs):
		if 'id' in self.__dict__:
			contact_id = self.id
			token = self.c.token

			interactions = Contactually(token).fetch_contact_interactions(contact_id, **kwargs).submit()
			self.interactions = [Interaction.from_json(token, interaction) for interaction in interactions['data']]

			for interaction in self.interactions:
			    interaction.participants = self
			
	def create_interaction(self, token=None, **kwargs):
		if 'id' in self.__dict__ and token == None:
			token = self.c.token
		return Interaction(token, participants={self.id:self.id},**kwargs)

	def delete(self, contact_id=None):
		if 'id' in self.__dict__ and contact_id == None:
			contact_id = self.id
		self.c.delete_contact(contact_id).submit()


class Interaction(BaseModel):
	def __init__(self, token, **kwargs):
		super().__init__(token, **kwargs)

	@classmethod
	def from_id(cls, token, contactually_id):
		json = Contactually(token).fetch_interaction(contactually_id).submit()
		data = json['data']
		interaction = cls(token, **data)
		interaction.json = json
		return interaction

	@classmethod
	def from_query(cls, token, query):
		json = Contactually(token).fetch_interactions(query_string=query).submit()
		data = json['data'][0]
		interaction = cls(token, **data)
		return interaction

	def save(self):
		params = {}
		update = False

		if 'id' in self.__dict__:
			update = True
			args = inspect.getfullargspec(self.c.update_interactions).args[1:]
		else: 
			args = inspect.getfullargspec(self.c.create_interaction).args[1:]
		for arg in args:
			if arg == 'interaction_id':
				params['interaction_id'] = self.id
			elif arg != 'self' and arg in self.__dict__:
				params[arg] = self.__dict__[arg]

		if update: 
			self.c.update_interactions(self.id, **params).submit()
		self.c.create_interaction(**params).submit()
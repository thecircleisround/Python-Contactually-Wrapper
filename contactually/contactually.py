from functools import wraps
from contact_token import TOKEN as ctoken
import requests

''' Python wrapper for Contactually API v2. Refer to Readme.md for examples'''


class Request:
    _host = "https://api.contactually.com/v2"
   
    def __init__(self, ctoken, method, dest, payload=None, params=None, headers=None):
        self.method = method
        self.url = self._host + dest
        self.payload = payload
        self.params = params
        if headers: 
            self.headers = headers
        else: 
            self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {ctoken}',
            'Content-type': 'application/json'
        }


class Contactually:
    _reserved = ['self', 'payload', 'dest', 'method']

    def __init__(self, ctoken, host='https://api.contactually.com/v2'):
        self.token = ctoken

    def _payload_fact(self, params, data_dict=True, exclude=None):
        payload = {'data':{}} if data_dict else {}
        suffixes = ['before','after','none','min','max']
        development
        exclude = exclude+self._reserved if exclude else self._reserved


        for key, val in params:
            if key not in exclude and val: 
                for suffix in suffixes: 
                    if key[-len(suffix):] == suffix:
                        key = f'{key[:-len(suffix)-1]}.{suffix}'
                    if key == 'query_string':
                        key = 'q'
                if data_dict:
                    payload['data'][key] = val
                else:
                    payload[key] = val
        return payload

    def _submit_request(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            r = func(self, *args, **kwargs)
            response = requests.request(r.method,
                                        r.url,
                                        headers=r.headers,
                                        json=r.payload,
                                        params=r.params)
            return response.json()
        return inner

    @_submit_request
    def fetch_current_user(self):
        method = 'GET'
        dest = '/me'
        return Request(self.token, method, dest)

    @_submit_request
    def fetch_buckets(self, id=None, id_not=None, created_at_before=None, created_at_after=None,
                      created_at_none=None, updated_at_before=None, updated_at_after=None,
                      query_string=None, order=None, page=None, page_size=None, offset=None):

        params = self._payload_fact(locals().items(),data_dict=False)
        method = 'GET'
        dest = '/buckets'
        return Request(self.token, method, dest, params=params)

    @_submit_request
    def fetch_bucket(self, bucket_id: str):
        method = 'GET'
        dest = f'/buckets/{bucket_id}'
        return Request(self.token, method, dest)

    @_submit_request
    def create_bucket(self, name=None, goal=None, reminder_interval=None, cloned_from_id=None):
        payload = {'data': {'name': name, 'goal': goal,
                            'reminder_interval': reminder_interval, 'cloned_from_id': cloned_from_id}}
        method = 'POST'
        dest = '/buckets'
        return Request(self.token, method, dest, payload=payload)

    @_submit_request
    def update_bucket(self, bucket_id: str, name=None, goal=None, reminder_interval: int=None):
        params = {'name': name, 'goal': goal,
                  'reminder_interval': reminder_interval}
        method = 'PUT'
        dest = f'/buckets/{bucket_id}'
        return Request(self.token, method, dest, params=params)

    @_submit_request
    def delete_bucket(self, bucket_id):
        method = 'DELETE'
        dest = f'/buckets/{bucket_id}'
        return Request(self.token, method, dest)

    @_submit_request
    def fetch_all_bucket_contacts(self, bucket_id, id=None, id_not=None, created_at_before=None, created_at_after=None,
                                  created_at_none=None, updated_at_before=None, updated_at_after=None, updated_at_none=None,
                                  audiences=None, audiences_all=None, audiences_not=None, company=None, location=None,
                                  connected_to=None, tags=None, tags_not=None, connected_accounts=None, external_id=None,
                                  external_id_not=None, external_id_presence=None, last_bucketed_at_before=None,
                                  last_bucketed_at_after=None, last_bucketed_at_none=None, is_overdue=None,
                                  status=None, status_not=None, last_contacted_before=None, last_contacted_after=None,
                                  last_contacted_none=None, inbound_last_contacted_at_before=None, inbound_last_contacted_at_after=None,
                                  inbound_last_contacted_at_none=None, times_contacted_min=None, times_contacted_max=None,
                                  times_contacted_inbound_min=None, times_contacted_inbound_max=None, total_interaction_count_min=None,
                                  total_interaction_count_max=None, relationship_types=None, days_to_followup_min=None, days_to_followup_max=None,
                                  days_overdue_min=None, days_overdue_max=None, recurring_type=None, recurring_type_not=None,
                                  recurring_next_due_date_before=None, recurring_next_due_date_after=None, deals=None, assigned_to=None,
                                  assigned_to_not=None, lead_pools=None, email=None, email_not=None, address=None, bucketed_at_before=None,
                                  bucketed_at_after=None, bucketed_at_none=None, query_string=None, order=None, page=None, page_size=None, offset=None):


        params = self._payload_fact(locals().items(),data_dict=False,exclude=['bucket_id'])
        method = 'GET'
        dest = f'/buckets/{bucket_id}/contacts'
        print(dest)
        return Request(self.token, method, dest, params=params)

    @_submit_request
    def fetch_contacts(self, method='GET', id=None, id_not=None, created_at_before=None, created_at_after=None, create_at_none=None,
                       updated_at_before=None, updated_at_after=None, updated_at_none=None, audiences=None, audiences_all=None,
                       audiences_not=None, company=None, location=None, connected_to=None, tags=None, tags_all=None, tags_not=None,
                       connected_accounts=None, external_id=None, external_id_not=None, external_id_presence=None, last_bucketed_at_before=None,
                       last_bucketed_at_after=None, last_bucketed_at_none=None, is_overdue=None, status=None, status_not=None, last_contacted_before=None, last_contacted_after=None,
                       last_contacted_none=None, inbound_last_contacted_at_before=None, inbound_last_contacted_at_after=None,
                       inbound_last_contacted_at_none=None, times_contacted_min=None, times_contacted_max=None,
                       times_contacted_inbound_min=None, times_contacted_inbound_max=None, total_interaction_count_min=None,
                       total_interaction_count_max=None, relationship_types=None, days_to_followup_min=None, days_to_followup_max=None,
                       days_overdue_min=None, days_overdue_max=None, recurring_type=None, recurring_type_not=None,
                       recurring_next_due_date_before=None, recurring_next_due_date_after=None, archived_at_before=None, archived_at_after=None,
                       archived_at_none=None, buckets=None, buckets_all=None, buckets_not=None, deals=None, assigned_to=None, assigned_to_not=None,
                       lead_pools=None, email=None, email_not=None, address=None, archived=None, with_archived=None, team_search=None,
                       q_fields=None, custom_field_id=None, custom_field_id_param=None, custom_field_before=None, custom_field_after=None,
                       custom_field_min=None, custom_field_max=None, query_string=None, notes=None, order=None, page=None, page_size=None, offset=None, fetch_ids=False):

        params = self._payload_fact(locals().items(), data_dict=False, exclude=[x for x in locals() if 'custom' in x])

        dest = '/contacts'

        if custom_field_id:
            custom_field_str = f'custom_field_{custom_field_id}'
            params[custom_field_str] = custom_field_id_param
            params[f'{custom_field_str}.before'] = custom_field_before
            params[f'{custom_field_str}.after'] = custom_field_after
            params[f'{custom_field_str}.min'] = custom_field_min
            params[f'{custom_field_str}.max'] = custom_field_max

        if fetch_ids:
            dest += '/resolve'

        elif method == "POST" and not fetch_ids:
            dest += '/search'
            payload = {'data': {x[0]: x[1] for x in params.items() if x[1]}}
            print(payload)
            return Request(self.token, method, dest, payload=payload)

        return Request(self.token, method, dest, params=params)

    @_submit_request
    def create_new_contact(self, contact:dict):

        payload = {'data':contact}
        dest = '/contacts'
        method = "POST"

        return Request(self.token, method, dest, payload=payload)

    def generate_contact(self, first_name: str, last_name: str, company: str=None, location: str=None,
                         title: str=None, avatar_url: str=None, days_to_followup: int=None, created_at=None,
                         relationship_types: str=None, tags: str=None, assigned_to_id: str=None, external_id: str=None,
                         audience_list=None, addresses: list=None, custom_fields: list=None, email_addresses: list=None,
                         phone_numbers: list=None, social_media_profiles: list=None, websites: list=None, grouping_ids: str=None,
                         bucket_ids: str=None, tag_ids: str=None, audience_ids: str=None, create_contact=False):
        ''' 
        Generates a new contact. List parameters should contain dict with parameter data. 
        Ex. an address parameter: 
                            [{"label":"Home",
                            "street_1": "123 Sesame St.",
                            "city": "Boston",
                            "state": "Massachusetts",
                            "zip": "02101",
                            "country": "United States"} }]

        Set create_contact to True to save generated contact to Contactually or pass to Contactually.create_new_contact
        '''

        contact = self._payload_fact(locals().items(), data_dict=False, exclude=['create_contact'])
        
        if create_contact:
            return self.create_new_contact(contact)

        return contact


    @_submit_request
    def create_multiple_contacts(self, contacts:list):
        ''' 
        Creates multiple contacts. List parameters should contain dict with parameter data. 
        Ex. an address parameter: 
                            [{"label":"Home",
                            "street_1": "123 Sesame St.",
                            "city": "Boston",
                            "state": "Massachusetts",
                            "zip": "02101",
                            "country": "United States"} }]
        '''

        payload = {'data':contacts}
        dest = '/contacts/bulk_create'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    @_submit_request
    def delete_contact(self, contact_id: str):
        dest = f'/contacts/{contact_id}'
        method = 'DELETE'
        
        return Request(self.token, method, dest)

    @_submit_request
    def bulk_delete_contacts(self, contact_ids: list):
        dest = '/contacts'
        method = 'DELETE'
        payload = {'data': {'contact_ids': contact_ids}}

        return Request(self.token, method, dest, payload=payload)

    @_submit_request
    def fetch_contact(self, contact_id, with_archived=False):
        dest = f'/contacts/{contact_id}'
        method = 'GET'
        payload = {'with_archived':with_archived}

        return Request(self.token, method, dest, payload=payload)

    @_submit_request
    def update_contact(self, contact_id, first_name: str=None, last_name: str=None, company: str=None, location: str=None,
                           title: str=None, avatar_url: str=None, days_to_followup: int=None, created_at=None,
                           relationship_types: str=None, tags: str=None, assigned_to_id: str=None, external_id: str=None,
                           audience_list=None, addresses: list=None, custom_fields: list=None, email_addresses: list=None,
                           phone_numbers: list=None, social_media_profiles: list=None, websites: list=None, grouping_ids: str=None,
                           bucket_ids: str=None, tag_ids: str=None, audience_ids: str=None):

        payload = self._payload_fact(locals().items())
        dest = f'/contacts/{contact_id}'
        method = 'POST'
        

        return Request(self.token, method, dest, payload=payload)

    @_submit_request
    def update_multiple_contacts(self, contact_ids,field, changes:dict):
        payload = {'data':{'contact_ids':contact_ids,'field':field, 'changes':[{"value":value, "type":change_type} for value,change_type in changes.items()] }}
        dest = '/contacts/bulk-change'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    @_submit_request
    def merge_contacts(self, contact_id, contact_ids:list):
        payload = {'data': {'contact_ids':contact_ids}}
        dest = f'/contacts/{contact_id}/merge'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    @_submit_request
    def archive_contact(self, contact_id, contact_ids:list):
        dest = f'/contacts/{contact_id}/archive'
        method = 'POST'

        return Request(self.token, method, dest)

    @_submit_request
    def unarchive_contact(self, contact_id, contact_ids:list):
        dest = f'/contacts/{contact_id}/unarchive'
        method = 'POST'

        return Request(self.token, method, dest)

    @_submit_request
    def archive_multiple_contacts(self, contact_ids:list):
        payload = {'data':{'contact_ids':contact_ids}}
        dest = '/contacts/archive-multiple'

    @_submit_request
    def unarchive_multiple_contacts(self, contact_ids:list):
        payload = {'data':{'contact_ids':contact_ids}}
        dest = '/contacts/unarchive-multiple'

    @_submit_request
    def export_contacts_to_csv(self, assigned_to:list=None, buckets:list=None, company:list=None, connected_accounts:list=None, 
                                connected_to:list=None, created_at_after=None, created_at_before=None, custom_field_id=None, 
                                custom_field_param=None, contact_ids:list=None, last_contacted_after=None, 
                                last_contacted_before=None, location:list=None, query_string=None, status:list=None, 
                                tags:list=None, times_contacted_min:int=None, times_contacted_max:int=None, team_search:bool=False, order:str=None, 
                                include_notes:bool=True):
       
        filters = self._payload_fact(locals().items(), data_dict=False, exclude=['include_notes'])
        payload = {'data':{'filters':filters},"include_notes":include_notes}
        dest='/contacts/export'
        method = 'POST'
        print(payload)
        return Request(self.token, method, dest, payload=payload)

    @_submit_request
    def fetch_job(self, job_id):
        dest = f'/jobs/{job_id}'
        method = 'GET'

        return Request(self.token, method, dest)

    @_submit_request
    def fetch_companies(self, id=None, id_not=None, created_at_before=None, created_at_after=None, created_at_none=None, updated_at_before=None, updated_at_after=None,
                        update_at_none=None, query_string=None, order:list=None, page:int=None, page_size:int=None, offset=None):
        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/companies'
        method = 'POST'

        return Request(self.token, method, dest, params=params)

    @_submit_request
    def create_company(self, name):
        payload = {'data':{'name':name}}
        dest = '/companies'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    @_submit_request
    def update_company(self, company_id, name):
        payload = {'data':{'name':name}}
        dest = f'/companies/{company_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    @_submit_request
    def delete_company(self, company_id):
        dest = f'/companies/{company_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    @_submit_request
    def fetch_linked_contacts(self, contact_id, id=None, id_not=None, created_at_before=None, created_at_none=None, updated_at_before=None, updated_at_after=None,
                              updated_at_none=None, order=None, page=None, page_size=None, offset=None):

        dest = f"/contacts/{contact_id}/linked-contacts"
        params = self._payload_fact(locals().items(), data_dict=False)
        method = "GET"

        return Request(self.token, method, dest, params=params)







if __name__ == '__main__':
    from pprint import pprint
    c = Contactually(ctoken)


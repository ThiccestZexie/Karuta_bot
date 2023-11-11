import json
import re

def extract_card_print(post : list):
    card_print = re.search(r'#(\d+)', post[0]).group(1)
    return int(card_print)

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
ed_lists = ['ed_one_post', 'ed_two_post', 'ed_three_post', 'ed_four_post', 'ed_five_post', 'ed_six_post']

class Settings:
    def __init__(self):
        self.this_server_link = "https://discord.gg/WwCsaDfRSC"
        self.karuta_bot_id = 646937666251915264 # Change if needed
        self.karuta_bot_name = "Karuta" # Change if needed 
        self.expected_channel_id  = 1154079321913307167 # Change if needed
        self.expected_market_id = 0 # Change if needed
        self.current_posting = list()
        self.market_channel_id = 1168671255604506745
        
        self.ed_one_post = list()
        self.ed_two_post = list()
        self.ed_three_post = list()
        self.ed_four_post = list()
        self.ed_five_post = list()
        self.ed_six_post = list()
        
        with open('current_market.json', 'r') as f:
            data = json.load(f)

        for ed_list in ed_lists:
            setattr(self, ed_list, data.get(ed_list, []))
            



    def get_current_posting(self):
        return self.current_posting
        
    def get_market_channel_id(self):
        return self.market_channel_id
    
    def add_to_current_posting(self, post_info, owner_id, ticket_price):
   #     self.current_posting.append([post_info, owner_id, ticket_price])
        pass
    def save_posting(self):
        #self.current_posting = sorted(self.current_posting, key=lambda x: extract_card_print(x), reverse=False)
        self.sort_all()
        data = {
            "ed_one_post": self.ed_one_post,
            "ed_two_post": self.ed_two_post,
            "ed_three_post": self.ed_three_post,
            "ed_four_post": self.ed_four_post,
            "ed_five_post": self.ed_five_post,
            "ed_six_post": self.ed_six_post,
        }

        with open('current_market.json', 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_json(self, key):
        with open('current_market.json', 'r') as f:
            data = json.load(f)
        return data.get(key, [])

    def sort_all(self):
        for ed_list in ed_lists:
            setattr(self, ed_list, sorted(getattr(self, ed_list), key=lambda x: extract_card_print(x), reverse=False))

    def get_ed_list(self, ed):
        return getattr(self, ed)
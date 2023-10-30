import json
import re

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

def extract_card_print(post):
    card_print = re.search(r'#(\d+)', post[0]).group(1)
    return int(card_print)
class Settings:
    def __init__(self):
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




    def get_current_posting(self):
        return self.current_posting
    def get_market_channel_id(self):
        return self.market_channel_id
    
    def add_to_current_posting(self, post_info, owner_id, ticket_price):
        self.current_posting.append([post_info, owner_id, ticket_price])
        self.save_posting()

    def save_posting(self):
        self.current_posting = sorted(self.current_posting, key=lambda x: extract_card_print(x), reverse=False)
        with open('current_market.json', 'w') as f:
            json.dump(self.get_current_posting(), f)

    def load_posting(self):
        try:
            with open('current_market.json', 'r') as f:
                self.current_posting = json.load(f)
        except FileNotFoundError:
            return []
"""
For first start of the script is necessary to run the following comand in command promt
-> pip3 install py-trello
After you can run this script

trello.json is stored trello settings used in this script
"""
import trello
import os
import re
import linecache
import json

class TrelloAdapter:
    """
    This class initializes trello client and provides methods for working with it.
    """
    def __init__(self):
        #initialize trello client
        settings = self.getSettings()
        self.client = trello.TrelloClient(api_key=settings['api_key'], token=settings['token'])
        #get board by boards's identifier (you can see it on url to board https://trello.com/b/S0JZaTMR)
        self.board = self.client.get_board(settings['board_id'])
        #get lists of board by his identifier (you identifier we get programly using command board.id)
        self.trlist = self.board.get_list(settings['list_id'])


    def getSettings(self):
        with open('trello_config.json', 'r', encoding='utf-8') as fh:
            settings = json.load(fh)
        return settings

    def getCardForName(self, name):
        cards = self.trlist.list_cards(card_filter="open")
        card = list(filter(lambda x: x.name in name, cards))
        if card:
            return card[0]

        return None

    def addCard(self, name, description):
        #add card to list specified name and desription
        self.trlist.add_card(name=name, desc=description)

class Report:
    """
    This class forms report and transfers control to the adapter
    """
    def __init__(self, name, num, code, path, filename, adapter):
        self.adapter = adapter
        self.num = num
        self.name = name
        self.header = name
        self.code = code.strip(' ').strip('\n')
        self.path = path
        self.filename = filename
        self.pattern = "Task: %s\nFile location: %s\nFile name: %s\nString number: %s\nPart of code: %s"
        self.patternchecklist = "File location: %s | File name: %s | String number: %s | Part of code: %s"

    def addToCheckList(self, card):
        name = self.patternchecklist % (self.path, self.filename, self.num, self.code)
        description = self.pattern % (self.header, self.path, self.filename, self.num, self.code)
        checklists = card.fetch_checklists()
        if checklists:
            item = list(filter(lambda x: x['name'] in name, checklists[0].items))
            if not item:
                checklists.add_checklist_item(name)
        else:
            desc = card.desc
            card.set_description('')
            if not (desc in description):
                card.add_checklist(title=self.name, items=[desc, name])
            else:
                card.add_checklist(title=self.name, items=[name])

    def execute(self):
        description = self.pattern % (self.header, self.path, self.filename, self.num, self.code)
        #transfer control to adapter, in our case is trello client
        self.adapter.addCard(self.name, description)

#initialize instance of trello adapter
adapter = TrelloAdapter()

#walk all files in directory where this script is located, also files of subfolders are considered
for path, dir, files in os.walk(os.getcwd()):
    #filter by .py extension
    for file in filter(lambda x: x.endswith('.py'), files):
        #open file
        with open(file) as content:
            # for each row we can see, does it satisfy our condition
            for num, line in enumerate(content, 1):
                #find matches
                match = re.search(r'(\#TECHDEBT\:\s?[\w\d\._\s]+)', line)
                if match:
                    #remove unused symbols
                    name = re.match(r'\#TECHDEBT\:\s?([\w\d\._\s]+)', match.string.strip(' ').strip('\n')).group(1)
                    #initialize instance of report
                    report = Report(name = name, num = num,
                                    code = linecache.getline(file, num+1), path = path,
                                    filename = file, adapter = adapter)

                    card = adapter.getCardForName(name)
                    if card:
                        #add to check list if card with this name is already exist
                        report.addToCheckList(card)
                    else:
                        #form report
                        report.execute()




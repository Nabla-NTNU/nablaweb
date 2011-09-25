# Utils-fil som brukes av views

import json
import WikiSettings
from simplemediawiki import MediaWiki
from simplemediawiki import build_user_agent

agent = simplemediawiki.build_user_agent('Django','stable','http://www.nabla.no')

w = MediaWiki(wiki_api_location,user_agent=agent)

def login_wiki(user, pw):
    try:
        w.login(user, pw)
    except:
        # Skal sende mail til admin om at noe er galt
        raise

def get_page_json(page):
    w.call(

import wikipedia
from random import *

def searching(sentence, lang):
    wikipedia.set_lang(str(lang))
    
    try:
        page = wikipedia.page(sentence)
        
    except wikipedia.DisambiguationError as e:
        chosen = choice(e.options)
        page = wikipedia.page(chosen)

    print("Слишком много страниц...\nРасскажу о "+str(page)) 
        
        
    return page

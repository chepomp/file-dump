import random

def handle_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'blue gandhi':
        return 'blue gandhi'
    
    quotes = ['If theres one thing Mahatma Gandhi stands for, its blue.', '"Blue and Tan"! High five, racial pride!', 'Now that my testicles have descended, I cant wait for some serious blue humping.', 'Blue is everywhere!', 'I dont wanna live in a world where blues diss their homies.', 'I need a moment to blue about this...', 'Im anti-violence, not anti-blue.', 'Oh man, if that were me, Id just blue myself!']

    if p_message == 'quote':
        return random.choice(quotes)
    if p_message == 'grinch me':
        return 'https://cdn.discordapp.com/attachments/1066929071990247427/1135777787953819728/grinch_me.mp4'
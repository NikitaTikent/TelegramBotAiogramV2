def moderate(message):
    user_name = message.from_user.first_name
    text = message.text.lower()
    mat = ['блять', 'сук', 'сука', 'пиздец', 'соси', 'хуйло', 'тварь', 'идиот', 'хуй', 'пенис']
    for x in mat:
        if x in text:
            return True
    return False

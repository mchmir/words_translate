from deep_translator import GoogleTranslator

to_translate = 'I want to translate this text'
translated = GoogleTranslator(source='auto', target='ru').translate(to_translate)

print(translated)

to_translate = 'want'
translated = GoogleTranslator(source='auto', target='ru').translate(to_translate)

print(translated)

to_translate = 'translate'
translated = GoogleTranslator(source='auto', target='ru').translate(to_translate)

print(translated)


import unicodedata
# Normalize characters with accents
arg = unicodedata.normalize('NFKD', arg)
arg = unicodedata.normalize('NFKD', arg).encode('ascii', 'ignore').decode('utf-8', 'ignore')
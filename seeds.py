import json
from models import Quotes, Authors, Tag
import connect


with open('quotes.json', encoding="utf-8") as fd:
    templates = json.load(fd)


for rec in templates:
    for section, value in rec.items():
        match section:
            case 'tags':
                tags = []
                for tag in value:
                    tags.append(Tag(name=tag))
            case 'author':
                author = Authors.objects(name=value).first()
                if not author:
                    author = Authors(name=value).save()
            case 'quote':
                Quotes(title=value, author=author, tags=tags).save()
            case _:
                print('Wrong format JSON file')

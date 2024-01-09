import json
from models import Quotes, Authors, Tag
import connect


with open('quotes.json') as fd:
    templates = json.load(fd)

authors = []
for rec in templates:
    for section, value in rec.items():
        match section:
            case 'tags':
                tags = []
                for tag in value:
                    tags.append(Tag(name=tag))
            case 'author':
                if value not in authors:
                    author = Authors(name=value).save()
                    authors.append(value)
                else:
                    author = Authors.objects(name=value).first()
            case 'quote':
                Quotes(title=value, author=author, tags=tags).save()
            case _:
                print('Wrong format JSON file')

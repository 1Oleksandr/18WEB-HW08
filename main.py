# from functools import lru_cache
from models import Authors, Quotes
from mongoengine import *
import redis
from redis_lru import RedisLRU

import connect

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

COMMANDS = {
    'name': 'name:',
    'tag': 'tag:',
    'tags': 'tags:',
    'exit': 'exit'
}


def parcer(text: str):
    for func, kw in COMMANDS.items():
        command = text.rstrip().split()
        if command[0].lower() == kw:
            return func, text[len(kw):].strip()
    return 'unknown', []


@cache
def seek_author(data):
    author = Authors.objects(name__istartswith=data).first()
    if author is None:
        res = f"We don't have quotes with author {data}"
        return res
    else:
        notes = Quotes.objects(author=author.id)
        res = []
        for note in notes:
            tags = [tag.name for tag in note.tags]
            res.append(
                f"Author: {author.name} Quote: {note.title} tags: {tags}")
        return res


@cache
def seek_by_tag(data):
    notes = Quotes.objects(tags__name__istartswith=data)
    if notes.count() == 0:
        res = f"We didn't find qoutes with tag: {data}"
        return res
    else:
        res = []
        print(F"---We found {notes.count()} quotes by tag {data} ---")
        for note in notes:
            tags = [tag.name for tag in note.tags]
            author = Authors.objects(id=note.author.id).first()
            res.append(
                f"Author: {author.name} - quote: {note.title} tags: {tags}")
        return res


@cache
def seek_by_tags(tags):
    ids = {}
    res = set()
    for tag in tags:
        notes = Quotes.objects(tags__name=tag)
        if notes is None:
            res = f"We didn't find qoutes with tag: {tag}"
            return res
        else:
            print(f"We found {notes.count()} quotes by '{tag}'")
            for note in notes:
                if note.id in ids:
                    # res.append(f'This is the same quotes for tag: {ids[note.id]}')
                    ...
                else:
                    tags = [tag.name for tag in note.tags]
                    author = Authors.objects(
                        id=note.author.id).first()
                    res.add(
                        f"author: {author.name} - quote: {note.title} tags: {tags}")
                    ids[note.id] = tag
    return res


def main():
    while True:
        com = input('Search by: ')
        func, data = parcer(com)
        match func:
            case 'name':
                res = seek_author(data)
                print(res)
            case 'tag':
                res = seek_by_tag(data)
                print(res)
            case 'tags':
                d = data.replace(' ', '')
                l = d.strip().split(',')
                tags = tuple(l)
                print(F'--- Quotes by tags {tags} ---')
                res = seek_by_tags(tags)
                print(res)
            case 'exit':
                break
            case _:
                print(
                    '''Unknown command. Use 
                    name: name author - can seek by first's symbols of author [or]
                    tags: tag1, tag2,...,tagN - seek by list of tags [or]
                    tag: brief - we can seek by "brief" is the first's symbols of tag''')

        # print('---1 Quotes by Einstein---')
        # note = Quotes.objects(author=author.id).first()
        # tags = [tag.name for tag in note.tags]
        # print(
        #     f"id: {note.id} author: {note.author.id} quote: {note.title} tags: {tags}")


if __name__ == '__main__':
    main()

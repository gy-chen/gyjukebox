import click
from flask.cli import AppGroup
from gyjukebox.lyrics.web import lyrics_search_ext

lyrics_cli = AppGroup("lyrics")


@lyrics_cli.command("index")
def index():
    lyrics_search_ext.index()


@lyrics_cli.command("search")
@click.argument("artist")
@click.argument("title")
def search(artist, title):
    print(lyrics_search_ext.searcher.search(artist, title))

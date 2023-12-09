import argparse
from getpass import getpass

import config
from config import Streamer
import spotify


class CLI:
    def __init__(self) -> None:
        self.config = config.Config()
        self.add_parser()

    def add_parser(self):
        self.parser = argparse.ArgumentParser()
        dw_t = self.parser.add_subparsers()

        common_args = argparse.ArgumentParser(add_help=False)
        common_args.add_argument("--username")
        common_args.add_argument("--password")
        common_args.add_argument("--format", default="mp3")
        common_args.add_argument("--quality", default="auto")

        sp = dw_t.add_parser("spotify", aliases=["s", "sp"])
        sp.set_defaults(func=lambda x: sp.print_help())

        sp_sub = sp.add_subparsers()
        sp_dw = sp_sub.add_parser("download", aliases=["d", "dw"], parents=[common_args])
        sp_dw.add_argument("url")
        sp_se = sp_sub.add_parser("search", aliases=["s", "se"], parents=[common_args])

        sp_dw.set_defaults(func=self.spotify)
        sp_se.set_defaults(func=self.spotify)

        yt = dw_t.add_parser("youtube", aliases=["y", "yt"])

    def parse(self):
        args = self.parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            self.parser.print_help()

    def spotify(self, args):
        is_download = hasattr(args, "url")
        if is_download:
            url = args.url.replace("intl-ja/", "")

        if not args.username and not args.password:
            credential = self.config.default_user(Streamer.SPOTIFY)
            if credential is None:
                username = input("Please enter your username>> ")
                password = getpass("Please enter your password>> ")
                self.config.add_user(username, password, Streamer.SPOTIFY, True)
            else:
                username = credential["username"]
                password = credential["password"]
        else:
            username = args.username
            password = args.password

        commander = spotify.Spotify(username, password)
        quality = spotify.DWQuality.cast(args.quality)

        if is_download:
            commander.download(url, ".", None, quality, args.format)
        else:
            commander.search(".", None, quality, args.format)


if __name__ == "__main__":
    CLI().parse()

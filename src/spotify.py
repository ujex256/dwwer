import subprocess


class DWQuality:
    AUTO = "auto"
    BEST = "normal"
    HIGH = "high"
    VERY_HIGH = "very_high"

    @classmethod
    def cast(cls, string):
        candidates = [cls.AUTO, cls.BEST, cls.HIGH, cls.VERY_HIGH]
        try:
            return list(filter(lambda x: x in string.lower(), candidates))[0]
        except IndexError:
            return cls.AUTO


class Spotify:
    def __init__(self, username, password) -> None:
        self.username = username
        self._password = password

        if not avaliable_zotify():
            raise Exception("Zotify is not available")

    def download(self, url, output_dir=None, format=None, quality=DWQuality.AUTO, dw_format="mp3"):
        args_str = self._format_args(output_dir, format, quality, dw_format)
        args_str = f"--username {self.username} --password {self._password} " + args_str
        subprocess.run(f"zotify {url} {args_str}", shell=True)

    def search(self, output_dir=None, format=None, quality=DWQuality.AUTO, dw_format="mp3"):
        args_str = self._format_args(output_dir, format, quality, dw_format)
        args_str = f"--username {self.username} --password {self._password} " + args_str
        subprocess.run(f"zotify {args_str}", shell=True)

    @staticmethod
    def _format_args(output_dir=None, format=None, quality=DWQuality.AUTO, dw_format="mp3"):
        args = [
            ("--root-path", output_dir),
            ("--output", format, lambda x: f'"{x}"'),
            ("--download-quality", quality),
            ("--download-format", dw_format),
        ]
        args = map(lambda x: x + (None,) if len(x) == 2 else x, args)
        args_str = ""
        for key, value, func in args:
            if value is None:
                continue
            if func:
                value = func(value)
            args_str = f"{args_str} {key} {value}"
        return args_str


def avaliable_zotify():
    dn = subprocess.DEVNULL
    res = subprocess.run("zotify -h", shell=True,
                         stdout=dn, stderr=dn, stdin=dn)
    return res.returncode == 0

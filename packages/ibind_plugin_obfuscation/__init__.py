import ibind
import re

class Plugin(ibind.Plugin):
    def process_code(self, code: str) -> str:
        regex = re.compile(r"(def)\s([a-zA-Z]*)\(([a-zA-z,\s]*)\)")
        matches = re.match(regex, code.splitlines(False))
        print(matches.groups())

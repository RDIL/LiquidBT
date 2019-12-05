from liquidbt.plugins import Plugin, TransformerPlugin, log

class RemoveComments(TransformerPlugin):
    def process_code(self, code: str) -> str:
        lines = code.splitlines()
        for line in lines:
            if "# " in line:
                lines.pop(lines.index(line))
        return "\n".join(lines)

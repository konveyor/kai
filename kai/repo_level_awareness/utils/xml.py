# Force python XML parser not faster C accelerators
# because we can't hook the C implementation
# trunk-ignore-begin(ruff/E402)
import sys

sys.modules["_elementtree"] = None  # type: ignore[assignment]
import xml.etree.ElementTree as ET  # trunk-ignore(bandit/B405)

# trunk-ignore-end(ruff/E402)


class LineNumberingParser(ET.XMLParser):
    def _start(self, *args, **kwargs):
        # Here we assume the default XML parser which is expat
        # and copy its element position attributes into output Elements
        element = super()._start(*args, **kwargs)
        element._start_line_number = self.parser.CurrentLineNumber
        element._start_column_number = self.parser.CurrentColumnNumber
        element._start_byte_index = self.parser.CurrentByteIndex
        return element

    def _end(self, *args, **kwargs):
        element = super(self.__class__, self)._end(*args, **kwargs)
        element._end_line_number = self.parser.CurrentLineNumber
        element._end_column_number = self.parser.CurrentColumnNumber
        element._end_byte_index = self.parser.CurrentByteIndex
        return element

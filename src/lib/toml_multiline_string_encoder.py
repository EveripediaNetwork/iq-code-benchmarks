import datetime
import re
import sys

from toml.decoder import InlineTableDict
from toml.encoder import _dump_str, _dump_float, _dump_time

if sys.version_info >= (3,):
    unicode = str


def _dump_str_new(v):
    multilines = v.split("\n")
    if len(multilines) > 1:
        return unicode('"""\n' + v.strip() + '\n"""')
    else:
        return _dump_str(v)


"""
This is a modified version of the toml encoder that preserves multiline strings
Got it from: https://github.com/uiri/toml/issues/236#issuecomment-471198145
"""


class MultilineStringTomlEncoder(object):
    def __init__(self, _dict=dict, preserve=False):
        self._dict = _dict
        self.preserve = preserve
        self.dump_funcs = {
            str: _dump_str_new,
            unicode: _dump_str_new,
            list: self.dump_list,
            bool: lambda v: unicode(v).lower(),
            int: lambda v: v,
            float: _dump_float,
            datetime.datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
            datetime.time: _dump_time,
            datetime.date: lambda v: v.isoformat(),
        }

    def get_empty_table(self):
        return self._dict()

    def dump_list(self, v):
        retval = "["
        for u in v:
            retval += " " + unicode(self.dump_value(u)) + ","
        retval += "]"
        return retval

    def dump_inline_table(self, section):
        """Preserve inline table in its compact syntax instead of expanding
        into subsection.

        https://github.com/toml-lang/toml#user-content-inline-table
        """
        retval = ""
        if isinstance(section, dict):
            val_list = []
            for k, v in section.items():
                val = self.dump_inline_table(v)
                val_list.append(k + " = " + val)
            retval += "{ " + ", ".join(val_list) + " }\n"
            return retval
        else:
            return unicode(self.dump_value(section))

    def dump_value(self, v):
        # Lookup function corresponding to v's type
        dump_fn = self.dump_funcs.get(type(v))
        if dump_fn is None and hasattr(v, "__iter__"):
            dump_fn = self.dump_funcs[list]
        # Evaluate function (if it exists) else return v
        return dump_fn(v) if dump_fn is not None else self.dump_funcs[str](v)

    def dump_sections(self, o, sup):
        retstr = ""
        if sup != "" and sup[-1] != ".":
            sup += "."
        retdict = self._dict()
        arraystr = ""
        for section in o:
            section = unicode(section)
            qsection = section
            if not re.match(r"^[A-Za-z0-9_-]+$", section):
                if '"' in section:
                    qsection = "'" + section + "'"
                else:
                    qsection = '"' + section + '"'
            if not isinstance(o[section], dict):
                arrayoftables = False
                if isinstance(o[section], list):
                    for a in o[section]:
                        if isinstance(a, dict):
                            arrayoftables = True
                if arrayoftables:
                    for a in o[section]:
                        arraytabstr = "\n"
                        arraystr += "[[" + sup + qsection + "]]\n"
                        s, d = self.dump_sections(a, sup + qsection)
                        if s:
                            if s[0] == "[":
                                arraytabstr += s
                            else:
                                arraystr += s
                        while d:
                            newd = self._dict()
                            for dsec in d:
                                s1, d1 = self.dump_sections(
                                    d[dsec], sup + qsection + "." + dsec
                                )
                                if s1:
                                    arraytabstr += (
                                        "[" + sup + qsection + "." + dsec + "]\n"
                                    )
                                    arraytabstr += s1
                                for s1 in d1:
                                    newd[dsec + "." + s1] = d1[s1]
                            d = newd
                        arraystr += arraytabstr
                else:
                    if o[section] is not None:
                        retstr += (
                            qsection
                            + " = "
                            + unicode(self.dump_value(o[section]))
                            + "\n"
                        )
            elif self.preserve and isinstance(o[section], InlineTableDict):
                retstr += qsection + " = " + self.dump_inline_table(o[section])
            else:
                retdict[qsection] = o[section]
        retstr += arraystr
        return (retstr, retdict)

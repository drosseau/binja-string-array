import binaryninja as binja

from binaryninja.enums import (
    Endianness
)


ENDIANS = (
    Endianness.LittleEndian,
    Endianness.BigEndian
)

ADDRESS_SIZES = (
    32,
    8,
    16,
    64
)


class Options(object):
    def __init__(self, endian, addr_size, n_strings):
        self.endian = endian
        self.addr_size = addr_size
        self.n_strings = n_strings


def get_opts():
    fields = []
    endian_field = binja.interaction.ChoiceField(
        "Endian", ENDIANS
    )
    fields.append(endian_field)
    fields.append(binja.interaction.SeparatorField())
    addr_size_field = binja.interaction.ChoiceField(
        "Address size (bits)", ADDRESS_SIZES
    )
    fields.append(addr_size_field)
    fields.append(binja.interaction.SeparatorField())
    nstrings_field = binja.interaction.IntegerField(
        "Number of strings"
    )
    fields.append(nstrings_field)
    binja.interaction.get_form_input(
        fields,
        "Options"
    )
    return Options(
        ENDIANS[endian_field.result],
        ADDRESS_SIZES[addr_size_field.result],
        nstrings_field.result
    )


def _to_be(bs):
    val = 0
    sz = len(bs) - 1
    for (i, b) in enumerate(bs):
        val |= b << (8*(sz - i))
    return val


def _to_le(bs):
    val = 0
    for (i, b) in enumerate(bs):
        val |= b << (8*i)
    return val


def to_int(b, endian):
    if b is None:
        return None
    if isinstance(b, str):
        b = map(ord, b)
    if endian == Endianness.LittleEndian:
        return _to_le(b)
    else:
        return _to_be(b)


def get_string(br, nbytes, opts):
    ptr = br.read(nbytes)
    if ptr is None:
        binja.log.log_error("read failed at {}".format(
            hex(br.offset - nbytes))
        )
        return None
    prev_off = br.offset
    ptr = to_int(ptr, opts.endian)
    if ptr == 0:
        return None
    br.seek(ptr)
    s = ""
    while True:
        c = br.read(1)
        if c is None:
            binja.log.log_error(
                "read failed at {}".format(hex(br.offset - 1))
            )
            break
        if c == "\x00":
            break
        s += c
    br.seek(prev_off)
    return s


def read_strings_array(view, address):
    strings = []
    opts = get_opts()
    br = binja.binaryview.BinaryReader(view, endian=opts.endian)
    if br.offset != address:
        br.seek(address)
    nbytes = opts.addr_size / 8
    if (opts.n_strings != -1):
        for _ in range(opts.n_strings):
            s = get_string(br, nbytes, opts)
            if s is None:
                s = "NULL";
            strings.append(s)
    else:
        while True:
            s = get_string(br, nbytes, opts)
            if s is None:
                break
            strings.append(s)

    output = "static const char* strings[] = {\n"
    for s in strings:
        if s == "NULL":
            output += "\tNULL,\n"
        else:
            output += "\t\"{}\",\n".format(s)
    output += "};"
    binja.interaction.show_plain_text_report("Strings", output)


binja.plugin.PluginCommand.register_for_address(
    "View String Array", (
        "Treats the address as an array of string pointers and loads a view "
        "of the strings as a C array: static const char* strings[] = { .. };"
    ),
    read_strings_array
)

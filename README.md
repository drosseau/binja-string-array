# String array viewer (v1.0)
Author: **Danny Rosseau**

_View the strings in an array at a given address as a C variable_

## Description:
Enumerates the string pointers at a given address. The address is treated as if it were a `const char**`. If you put -1 as the number of strings it will keep reading until the first `NULL` address.

![Using on the example binary](example-image.png)

## Minimum Version

This plugin requires the following minimum version of Binary Ninja:

 * release - 1.1.1038

## License
This plugin is released under a [MIT](LICENSE) license.

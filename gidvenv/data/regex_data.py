import re


package_value_regex = re.compile(r"""^(?P<option1>-{1,2}[a-z,\-]+)?
                    \s*
                    (?P<option2>-{1,2}[a-z,\-]+)?
                    \s*
                    (?P<option3>-{1,2}[a-z,\-]+)?
                    \s*
                    (?P<option4>-{1,2}[a-z,\-]+)?
                    \s*
                    (?P<option5>-{1,2}[a-z,\-]+)?
                    \s*
                    (?P<option6>-{1,2}[a-z,\-]+)?
                    \s*
                    (?P<package_name>(?:\s?)[a-z,\-,0-9_]+)
                    \[?
                    (?P<extras>\w+)?
                    \]?
                    (?P<specifier>==|<=|>=|~=|!=|=|<|>|~)?
                    (?P<version>[0-9,.a-z]+)?$""", re.VERBOSE | re.IGNORECASE)

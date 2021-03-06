import pytest

from stix2matcher.matcher import match


_observations = [
    {
        "type": "observed-data",
        "number_observed": 1,
        "first_observed": "2011-12-03T21:34:41Z",
        "last_observed": "2011-12-03T21:34:41Z",
        "objects": {
            "0": {
                "type": "binary_test",
                "name": "alice",
                "name_u": u"\u0103lice",
                "name_hex": "616c696365",
                "name_bin": "YWxpY2U=",
                "bin_hex": "01020304"
            }
        }
    }
]


@pytest.mark.parametrize("pattern", [
    "[binary_test:name = h'616c696365']",
    "[binary_test:name = b'YWxpY2U=']",
    "[binary_test:name_bin = h'616c696365']",
    "[binary_test:name_bin = b'YWxpY2U=']",
    "[binary_test:name_bin = 'alice']",
    "[binary_test:name_hex = h'616c696365']",
    "[binary_test:name_hex = b'YWxpY2U=']",
    "[binary_test:name_hex = 'alice']",

    "[binary_test:name > h'616172647661726b']",
    "[binary_test:name > b'YWFyZHZhcms=']",
    "[binary_test:name_bin > h'616172647661726b']",
    "[binary_test:name_bin > b'YWFyZHZhcms=']",
    "[binary_test:name_bin > 'aardvark']",
    "[binary_test:name_hex > h'616172647661726b']",
    "[binary_test:name_hex > b'YWFyZHZhcms=']",
    "[binary_test:name_hex > 'aardvark']",

    # some nonprintable binary data tests too.
    "[binary_test:bin_hex = h'01020304']",
    "[binary_test:bin_hex = b'AQIDBA==']",
    "[binary_test:bin_hex = '\x01\x02\x03\x04']",
])
def test_binary_match(pattern):
    assert match(pattern, _observations)


@pytest.mark.parametrize("pattern", [
    # test codepoint >= 256, in both pattern and json
    u"[binary_test:name_bin = '\u0103lice']",
    u"[binary_test:name_bin > '\u0103lice']",
    u"[binary_test:name_bin < '\u0103lice']",
    u"[binary_test:name_hex = '\u0103lice']",
    u"[binary_test:name_hex > '\u0103lice']",
    u"[binary_test:name_hex < '\u0103lice']",
    u"[binary_test:name_u = h'616c696365']",
    u"[binary_test:name_u > h'616c696365']",
    u"[binary_test:name_u < h'616c696365']",
    u"[binary_test:name_u = b'YWxpY2U=']",
    u"[binary_test:name_u > b'YWxpY2U=']",
    u"[binary_test:name_u < b'YWxpY2U=']",
])
def test_binary_nomatch(pattern):
    assert not match(pattern, _observations)

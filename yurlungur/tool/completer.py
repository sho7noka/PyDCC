# coding: utf-8
import keyword
import yurlungur as yr

# yr.meta.__make_completer("UnityEngine")


class _Completer(object):
    """Taken from rlcompleter, with readline references stripped, and a local
    dictionary to use."""

    def __init__(self, locals):
        self.locals = locals

    def Complete(self, text, state):
        """Return the next possible completion for 'text'.
        This is called successively with state == 0, 1, 2, ... until it
        returns None.  The completion should begin with 'text'.
        """
        if state == 0:
            if "." in text:
                self.matches = self._AttrMatches(text)
            else:
                self.matches = self._GlobalMatches(text)
        try:
            return self.matches[state]
        except IndexError:
            return None

    def _GlobalMatches(self, text):
        """Compute matches when text is a simple name.

        Return a list of all keywords, built-in functions and names
        currently defines in __main__ that match.
        """
        import __builtin__, __main__
        matches = set()
        n = len(text)
        for l in [keyword.kwlist, __builtin__.__dict__.keys(),
                  __main__.__dict__.keys(), self.locals.keys()]:
            for word in l:
                if word[:n] == text and word != "__builtins__":
                    matches.add(word)
        return list(matches)

    def _AttrMatches(self, text):
        """Compute matches when text contains a dot.

        Assuming the text is of the form NAME.NAME....[NAME], and is
        evaluatable in the globals of __main__, it will be evaluated
        and its attributes (as revealed by dir()) are used as possible
        completions.  (For class instances, class members are are also
        considered.)

        WARNING: this can still invoke arbitrary C code, if an object
        with a __getattr__ hook is evaluated.
        """
        import re, __main__

        assert len(text)

        # This is all a bit hacky, but that's tab-completion for you.

        # Now find the last index in the text of a set of characters, and split
        # the string into a prefix and suffix token there.  The suffix token
        # will be used for completion.
        splitChars = ' )(;,+=*/-%!<>'
        index = -1
        for char in splitChars:
            index = max(text.rfind(char), index)

        if index >= len(text) - 1:
            return []

        prefix = ''
        suffix = text
        if index >= 0:
            prefix = text[:index + 1]
            suffix = text[index + 1:]

        m = re.match(r"([^.]+(\.[^.]+)*)\.(.*)", suffix)
        if not m:
            return []
        expr, attr = m.group(1, 3)

        try:
            myobject = eval(expr, __main__.__dict__, self.locals)
        except (AttributeError, NameError, SyntaxError):
            return []

        words = set(dir(myobject))
        if hasattr(myobject, '__class__'):
            words.add('__class__')
        words = words.union(set(_GetClassMembers(myobject.__class__)))

        words = list(words)
        matches = set()
        n = len(attr)
        for word in words:
            if word[:n] == attr and word != "__builtins__":
                matches.add("%s%s.%s" % (prefix, expr, word))
        return list(matches)


def _GetClassMembers(cls):
    ret = dir(cls)
    if hasattr(cls, '__bases__'):
        for base in cls.__bases__:
            ret = ret + _GetClassMembers(base)
    return ret

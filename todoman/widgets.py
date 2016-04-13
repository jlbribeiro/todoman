# Copyright (c) 2016 Hugo Osvaldo Barrera
# Copyright (c) 2013-2016 Christian Geier et al.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re

import urwid


def delete_last_word(text, number=1):
    """delete last `number` of words from text"""
    words = re.findall(r"[\w]+|[^\w\s]", text, re.UNICODE)
    for one in range(1, number + 1):
        text = text.rstrip()
        if text == '':
            return text
        text = text[:len(text) - len(words[-one])]
    return text


def delete_till_beginning_of_line(text):
    """delete till beginning of line"""
    if text.rfind("\n") == -1:
        return ''
    return text[0:text.rfind("\n") + 1]


def delete_till_end_of_line(text):
    """delete till beginning of line"""
    if text.find("\n") == -1:
        return ''
    return text[text.find("\n"):]


def goto_beginning_of_line(text):
    if text.rfind("\n") == -1:
        return 0
    return text.rfind("\n") + 1


def goto_end_of_line(text):
    if text.find("\n") == -1:
        return len(text)
    return text.find("\n")


class ExtendedEdit(urwid.Edit):
    """A text editing widget supporting some more editing commands"""
    def keypress(self, size, key):
        if key == 'ctrl w':
            self._delete_word()
        elif key == 'ctrl u':
            self._delete_till_beginning_of_line()
        elif key == 'ctrl k':
            self._delete_till_end_of_line()
        elif key == 'ctrl a':
            self._goto_beginning_of_line()
        elif key == 'ctrl e':
            self._goto_end_of_line()
        elif key == 'ctrl d':
            self._delete_forward_letter()
        # TODO: alt b, alt f
        else:
            return super(ExtendedEdit, self).keypress(size, key)

    def _delete_forward_letter(self):
        text = self.get_edit_text()
        pos = self.edit_pos
        text = text[:pos] + text[pos + 1:]
        self.set_edit_text(text)

    def _delete_word(self):
        """delete word before cursor"""
        text = self.get_edit_text()
        f_text = delete_last_word(text[:self.edit_pos])
        self.set_edit_text(f_text + text[self.edit_pos:])
        self.set_edit_pos(len(f_text))

    def _delete_till_beginning_of_line(self):
        """delete till start of line before cursor"""
        text = self.get_edit_text()
        f_text = delete_till_beginning_of_line(text[:self.edit_pos])
        self.set_edit_text(f_text + text[self.edit_pos:])
        self.set_edit_pos(len(f_text))

    def _delete_till_end_of_line(self):
        """delete till end of line before cursor"""
        text = self.get_edit_text()
        f_text = delete_till_end_of_line(text[self.edit_pos:])
        self.set_edit_text(text[:self.edit_pos] + f_text)

    def _goto_beginning_of_line(self):
        text = self.get_edit_text()
        self.set_edit_pos(goto_beginning_of_line(text[:self.edit_pos]))

    def _goto_end_of_line(self):
        text = self.get_edit_text()
        self.set_edit_pos(
            goto_end_of_line(text[self.edit_pos:]) + self.edit_pos
        )

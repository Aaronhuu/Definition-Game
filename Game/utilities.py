'''
Created on Dec 3, 2015

@author: aaronhu
'''
def word_wrap(text, max_length=60):
    """Word wraps a string and returns as list of strings.

    Takes a string and returns list of strings that 
    are max length characters longed, preserving words 
    at end of line.
    """
    lines = []

    if len(text) < max_length:
        return [text]

    while len(text) > 0:
        line = text[:max_length]
        i = 0
        while line[-1] != ' ' and len(line) >= max_length:
            line = text[:max_length + i]
            i += 1
            if line == text:
                break
        lines += [line]
        text = text[(max_length - 1) + i:]
    return lines

if __name__ == '__main__':
    print(word_wrap('A frame house with two stories in front and one in back, having a pitched roof with unequal sides.', 50))
    print(word_wrap('To fall head down through the air.', 50))
    print(word_wrap('Entertainingly and strikingly clever or original in concept, design, or performance.', 50))
    print(word_wrap('A hooded garment, especially a hooded sweatshirt.', 50))
    print(word_wrap('The second stanza in a poem consisting of alternating stanzas in contrasting metrical form.', 50))
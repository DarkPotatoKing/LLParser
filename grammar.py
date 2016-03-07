class Rule(object):
    def __init__(self, rule):
        self.rule = rule.strip()

    def __repr__(self):
        return self.rule

class Grammar(object):

    def __init__(self, filename = 'grammar.txt'):
        self.grammar = list()
        try:
            with open(filename, 'r') as f:
                self.grammar = [Rule(i) for i in f.readlines()]
        except IOError:
            print 'Grammar text file does not exist'

    def __repr__(self):
        return '\n'.join([str(i) for i in self.grammar])

if __name__ == '__main__':
    g = Grammar()
    print g

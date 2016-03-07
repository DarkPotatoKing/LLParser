class Clause(object):

    def __init__(self, clause):
        self.tokens = clause.strip().split()

    def __repr__(self):
        return ' '.join(self.tokens)

class Rule(object):

    def __init__(self, rule):
        # split rule into premise and clauses
        rule = rule.split('->')
        self.premise = rule[0].strip()
        self.clauses = [Clause(i) for i in rule[1].split('|')]

    def __repr__(self):
        return self.premise + ' -> ' + ' | '.join([str(i) for i in self.clauses])

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

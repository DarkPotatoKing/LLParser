class Clause(object):

    def __init__(self, clause):
        self.tokens = clause.strip().split()

    def __repr__(self):
        return ' '.join(self.tokens)

    def token_set(self):
        return set([i for i in self.tokens])

class Rule(object):

    def __init__(self, rule):
        # split rule into premise and clauses
        rule = rule.split('->')
        self.premise = rule[0].strip()
        self.clauses = [Clause(i) for i in rule[1].split('|')]

    def __repr__(self):
        return self.premise + ' -> ' + ' | '.join([str(i) for i in self.clauses])

    def has_direct_left_recursion(self):
        for clause in self.clauses:
            if self.premise == clause.tokens[0]:
                return True
        return False

    def token_set(self):
        return reduce(lambda a,b: a | b, [i.token_set() for i in self.clauses]) | set(self.premise)


class Grammar(object):

    def __init__(self, filename = 'grammar.txt'):
        self.rules = list()
        try:
            with open(filename, 'r') as f:
                rules = [Rule(i) for i in f.readlines()]

            self.starting_rule = rules[0]

            # check for direct left recursion
            for rule in rules:
                if rule.has_direct_left_recursion():
                    modified_rules = self.remove_direct_left_recursion(rule)
                    if rule == self.starting_rule:
                        self.starting_rule = modified_rules[0]
                    for r in modified_rules:
                        self.rules.append(r)
                else:
                    self.rules.append(rule)

            # filter tokens
            self.tokens = reduce(lambda a,b: a | b, [i.token_set() for i in self.rules]) - set("'")
            self.non_terminals = set()
            self.terminals = set()
            for token in self.tokens:
                if token.isupper():
                    self.non_terminals.add(token)
                else:
                    self.terminals.add(token)

            # get first set
            self.first = dict()

            # the first set of every terminal is itself:
            for i in self.terminals:
                self.first[i] = set(i)

            # recursively find the first set of every non-terminal
            for rule in self.rules:
                self.find_first(rule.premise)

            for i in self.non_terminals:
                print 'FIRST(' + i + ') = ' + str(self.first[i])
        except IOError:
            print 'Grammar text file does not exist'

    def find_rule(self, token):
        for rule in self.rules:
            if token == rule.premise:
                return rule

    def find_first(self, token):
        try:
            return self.first[token]
        except KeyError:
            rule = self.find_rule(token)
            first_tokens = [clause.tokens[0] for clause in rule.clauses]
            first = set()
            for t in first_tokens:
                first = first | self.find_first(t)
            self.first[token] = first
            return first

    def __repr__(self):
        return '\n'.join([str(i) for i in self.rules])

    def remove_direct_left_recursion(self, rule):
        modified_rules = list()
        recursive_clauses = list()
        non_recursive_clauses = list()

        for clause in rule.clauses:
            if rule.premise == clause.tokens[0]:
                recursive_clauses.append(clause)
            else:
                non_recursive_clauses.append(clause)

        modified_rules.append(Rule(rule.premise + ' -> ' + ' | '.join([str(i) + ' ' + rule.premise + "'" for i in non_recursive_clauses])))

        recursive_clauses = [' '.join(i.tokens[1:]) for i in recursive_clauses]
        modified_rules.append(Rule(rule.premise + "\' -> " + ' | '.join([str(i) + ' ' + rule.premise + "'" for i in recursive_clauses]) + ' | $'))

        return modified_rules

    def token_set(self):
        return self.tokens

    def non_terminal_token_set(self):
        return self.non_terminals

    def terminal_token_set(self):
        return self.terminals

if __name__ == '__main__':
    g = Grammar()

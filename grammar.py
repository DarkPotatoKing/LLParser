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

    def has_direct_left_recursion(self):
        for clause in self.clauses:
            if self.premise == clause.tokens[0]:
                return True
        return False

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
                    for r in modified_rules:
                        self.rules.append(r)
                else:
                    self.rules.append(rule)

        except IOError:
            print 'Grammar text file does not exist'

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

if __name__ == '__main__':
    g = Grammar()
    print g

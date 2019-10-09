#!/usr/local/bin/python3
import json
import sys

class ExecutionError(Exception):
    def __init__(self, message):
        super().__init__("Execution Error Occured !!")
        
        
class NullValueError(Exception):
    def __init__(self, message):
        super().__init__(message)


class KeyMissingError(Exception):
    def __init__(self, message):
        super().__init__(message)  
        

class UnknownOperatorError(Exception):    
    def __init__(self, message):
        super().__init__(message)


class DecisionTree(object):
    """
    Handles JSON files for loading and executing data as decision structure

    {
    "condition": "AND",
    "rules": [
        {
        "id": "price",
        "field": "price",
        "type": "double",
        "input": "number",
        "operator": "less",
        "value": 10.25
        },
        {
            "id": "in_stock",
            "field": "in_stock",
            "type": "integer",
            "input": "radio",
            "operator": "equal",
            "value": 1
        }
    ],
    "valid": true
    }

    Methods:
        self.__init__()
        execute_tree()
    """

    def __init__(self, dataset):
        self._compare_to = dataset


    def _compare(self, rule):
        '''
        Performs comparision operator 

        Parameters:
            rule: consist of a comparison operator and predicate

        Returns:
            bool: rule operation result
        '''
        
        if not rule:
            raise NullValueError("Rule Value should not be null.")
        
        if 'value' not in rule:
            raise KeyMissingError("No value Key available in rule")
        
        if rule['id'] not in self._compare_to:
            raise KeyMissingError("No value Key available in given data")
        
        if rule['operator'] == "equal":
            return rule['value'] == self._compare_to[rule['id']]
        elif rule['operator'] == "not_equal":
            return rule['value'] != self._compare_to[rule['id']]
        elif rule['operator'] == "in":
            return rule['value'] in self._compare_to[rule['id']]
        elif rule['operator'] == "not_in":
            return not (rule['value'] in self._compare_to[rule['id']])
        elif rule['operator'] == 'less':
            return rule['value'] < self._compare_to[rule['id']]
        elif rule['operator'] == "less_or_equal":
            return rule['value'] <= self._compare_to[rule['id']]
        elif rule['operator'] == "greater":
            return rule['value'] > self._compare_to[rule['id']]
        elif rule['operator'] == "greater_or_equal":
            return rule['value'] >= self._compare_to[rule['id']]
        elif rule['operator'] == "between":
            return rule['value'][0] <= self._compare_to[rule['id']] <= rule['value'][1]
        elif rule['operator'] == "not_between":
            return not (rule['value'][0] <= self._compare_to[rule['id']] <= rule['value'][1])
        elif rule['operator'] == "is_null":
            return rule['value'] is None
        elif rule['operator'] == "is_not_null":
            return rule['value'] is not None
        else:
            raise UnknownOperatorError(f"Unknown operator: '{rule['operator']}'. Operation not in database!!")

    def execute_tree(self, tree):
        '''
        Takes in json document with descriptive structure
        Runs tree parsing and traversal using fixed operations to 

        Parameters:
            tree: internal parameter; Parsed JSON with tree structure; Dictionary in python

        Returns:
            bool: Returns decision made from data in structure
        '''
        if 'condition' in tree:
            op = tree['condition']
            rules = tree['rules']
            if len(rules) == 2:
                if op == "AND":
                    return self.execute_tree(rules[0]) and self.execute_tree(rules[1])
                return self.execute_tree(rules[0]) or self.execute_tree(rules[1])
            else:
                ex = {'condition': op, 'rules': rules[1:]}
                if op == "AND":
                    return self.execute_tree(rules[0]) and self.execute_tree(ex2)
                return self.execute_tree(rules[0]) or self.execute_tree(ex2)

        return self._compare(tree)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("""
            Decision Grid.

            Usage:
            ops_relay.py init <file>

            Options:
            -h --help     Show this screen.
            --version     Show version.
        """)
        exit(0)
    # data = {"price": 34, "category": 2, "category1": 2}
    # rs = DecisionTree(sys.argv[2], data)
    # print(rs.execute_tree(rs._intel_tree))

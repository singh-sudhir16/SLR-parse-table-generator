import streamlit as st
import pandas as pd
import re
from collections import defaultdict, deque

class SLRParser:
    def __init__(self, grammar_input):
        self.grammar = self.parse_grammar(grammar_input)
        self.terminals = set()
        self.non_terminals = set()
        self.start_symbol = None
        self.first_sets = {}
        self.follow_sets = {}
        self.canonical_collection = []
        self.goto_table = {}
        self.parsing_table = {}
        self.augmented_grammar = []
        
        self.process_grammar()
        self.compute_first_sets()
        self.compute_follow_sets()
        self.build_canonical_collection()
        self.construct_parsing_table()
    
    def parse_grammar(self, grammar_input):
        """Parse the input grammar into a dictionary."""
        grammar = {}
        lines = grammar_input.strip().split('\n')
        
        for line in lines:
            if '->' not in line:
                continue
            lhs, rhs = line.split('->', 1)
            lhs = lhs.strip()
            productions = [p.strip() for p in rhs.split('|')]
            if lhs not in grammar:
                grammar[lhs] = []
            grammar[lhs].extend(productions)
        return grammar
    
    def process_grammar(self):
        """Extract terminals, non-terminals and create augmented grammar."""
        # Set the start symbol as the first non-terminal in the grammar
        self.start_symbol = list(self.grammar.keys())[0]
        
        # Add augmented production S' -> S
        augmented_start = f"{self.start_symbol}'"
        self.augmented_grammar.append((augmented_start, tuple([self.start_symbol])))
        
        # Extract terminals and non-terminals
        self.non_terminals = set(self.grammar.keys())
        
        for nt, productions in self.grammar.items():
            for prod in productions:
                symbols = prod.split()
                for symbol in symbols:
                    if symbol not in self.non_terminals and symbol != 'ε':
                        self.terminals.add(symbol)
                # Add original production to augmented grammar
                self.augmented_grammar.append((nt, tuple(symbols) if prod != 'ε' else tuple()))
        
        self.terminals.add('$')  # Add end marker
    
    def compute_first_sets(self):
        """Compute FIRST sets for all symbols."""
        # Initialize FIRST sets
        for nt in self.non_terminals:
            self.first_sets[nt] = set()
        for terminal in self.terminals:
            self.first_sets[terminal] = {terminal}
        
        # Add ε to FIRST sets of non-terminals with ε-productions
        for nt, productions in self.grammar.items():
            if 'ε' in productions:
                self.first_sets[nt].add('ε')
        
        # Compute FIRST sets until no more changes
        changed = True
        while changed:
            changed = False
            for nt, productions in self.grammar.items():
                for prod in productions:
                    if prod == 'ε':
                        continue
                    symbols = prod.split()
                    i = 0
                    can_derive_epsilon = True
                    while i < len(symbols) and can_derive_epsilon:
                        symbol = symbols[i]
                        if symbol in self.first_sets:
                            non_epsilon_first = self.first_sets[symbol] - {'ε'}
                            old_size = len(self.first_sets[nt])
                            self.first_sets[nt].update(non_epsilon_first)
                            if len(self.first_sets[nt]) > old_size:
                                changed = True
                        can_derive_epsilon = ('ε' in self.first_sets.get(symbol, set()))
                        i += 1
                    if can_derive_epsilon and i == len(symbols) and 'ε' not in self.first_sets[nt]:
                        self.first_sets[nt].add('ε')
                        changed = True
    
    def compute_follow_sets(self):
        """Compute FOLLOW sets for all non-terminals."""
        # Initialize FOLLOW sets
        for nt in self.non_terminals:
            self.follow_sets[nt] = set()
        # Add $ to FOLLOW of start symbol
        self.follow_sets[self.start_symbol].add('$')
        # Compute FOLLOW sets until no more changes
        changed = True
        while changed:
            changed = False
            for nt, productions in self.grammar.items():
                for prod in productions:
                    if prod == 'ε':
                        continue
                    symbols = prod.split()
                    for i, symbol in enumerate(symbols):
                        if symbol in self.non_terminals:
                            if i < len(symbols) - 1:
                                next_symbols = symbols[i+1:]
                                sequence_first = self.compute_first_of_sequence(next_symbols)
                                non_epsilon_first = sequence_first - {'ε'}
                                old_size = len(self.follow_sets[symbol])
                                self.follow_sets[symbol].update(non_epsilon_first)
                                if len(self.follow_sets[symbol]) > old_size:
                                    changed = True
                                if 'ε' in sequence_first:
                                    old_size = len(self.follow_sets[symbol])
                                    self.follow_sets[symbol].update(self.follow_sets[nt])
                                    if len(self.follow_sets[symbol]) > old_size:
                                        changed = True
                            else:
                                old_size = len(self.follow_sets[symbol])
                                self.follow_sets[symbol].update(self.follow_sets[nt])
                                if len(self.follow_sets[symbol]) > old_size:
                                    changed = True
    
    def compute_first_of_sequence(self, symbols):
        """Compute FIRST set of a sequence of symbols."""
        if not symbols:
            return {'ε'}
        result = set()
        all_can_derive_epsilon = True
        for symbol in symbols:
            if symbol not in self.first_sets:
                result.add(symbol)
                all_can_derive_epsilon = False
                break
            non_epsilon_first = self.first_sets[symbol] - {'ε'}
            result.update(non_epsilon_first)
            if 'ε' not in self.first_sets[symbol]:
                all_can_derive_epsilon = False
                break
        if all_can_derive_epsilon:
            result.add('ε')
        return result
    
    def build_canonical_collection(self):
        """Build the canonical collection of LR(0) items."""
        # Create augmented start production item: (S', [DOT, S])
        augmented_start = f"{self.start_symbol}'"
        initial_item = (augmented_start, tuple(['DOT', self.start_symbol]))
        initial_state = self.closure({initial_item})
        self.canonical_collection.append(initial_state)
        
        i = 0
        while i < len(self.canonical_collection):
            state = self.canonical_collection[i]
            next_symbols = set()
            for item in state:
                nt, rhs = item
                try:
                    dot_pos = rhs.index('DOT')
                    if dot_pos < len(rhs) - 1:
                        next_symbols.add(rhs[dot_pos + 1])
                except ValueError:
                    continue
            for symbol in next_symbols:
                next_state = self.goto(state, symbol)
                if next_state and next_state not in self.canonical_collection:
                    self.canonical_collection.append(next_state)
                if next_state:
                    self.goto_table[(i, symbol)] = self.canonical_collection.index(next_state)
            i += 1
    
    def closure(self, items):
        """Compute the closure of a set of LR(0) items."""
        result = set(items)
        changed = True
        while changed:
            changed = False
            new_items = set()
            for item in result:
                nt, rhs = item
                try:
                    dot_pos = rhs.index('DOT')
                    if dot_pos < len(rhs) - 1:
                        next_symbol = rhs[dot_pos + 1]
                        if next_symbol in self.non_terminals:
                            for prod_rhs in self.grammar.get(next_symbol, []):
                                if prod_rhs == 'ε':
                                    new_item = (next_symbol, tuple(['DOT']))
                                else:
                                    new_item = (next_symbol, tuple(['DOT'] + prod_rhs.split()))
                                if new_item not in result:
                                    new_items.add(new_item)
                                    changed = True
                except ValueError:
                    continue
            result.update(new_items)
        return frozenset(result)
    
    def goto(self, items, symbol):
        """Compute goto(I, X) where I is a set of items and X is a grammar symbol."""
        next_items = set()
        for item in items:
            nt, rhs = item
            try:
                dot_pos = rhs.index('DOT')
                if dot_pos < len(rhs) - 1 and rhs[dot_pos + 1] == symbol:
                    new_rhs = list(rhs)
                    new_rhs[dot_pos], new_rhs[dot_pos + 1] = new_rhs[dot_pos + 1], new_rhs[dot_pos]
                    next_items.add((nt, tuple(new_rhs)))
            except ValueError:
                continue
        if next_items:
            return self.closure(next_items)
        else:
            return None
    
    def construct_parsing_table(self):
        """Construct the SLR parsing table."""
        # Initialize the parsing table structure
        for i in range(len(self.canonical_collection)):
            self.parsing_table[i] = {}
            for symbol in self.terminals | self.non_terminals:
                self.parsing_table[i][symbol] = []
        # Fill actions based on canonical collection
        for i, state in enumerate(self.canonical_collection):
            for item in state:
                nt, rhs = item
                try:
                    dot_pos = rhs.index('DOT')
                    if dot_pos < len(rhs) - 1:
                        next_symbol = rhs[dot_pos + 1]
                        if next_symbol in self.terminals and (i, next_symbol) in self.goto_table:
                            next_state = self.goto_table[(i, next_symbol)]
                            action = f"s{next_state}"
                            if action not in self.parsing_table[i][next_symbol]:
                                self.parsing_table[i][next_symbol].append(action)
                    elif dot_pos == len(rhs) - 1 or (len(rhs) == 1 and rhs[0] == 'DOT'):
                        if nt == f"{self.start_symbol}'" and len(rhs) == 2 and rhs[1] == self.start_symbol:
                            self.parsing_table[i]['$'].append("acc")
                        else:
                            prod_num = -1
                            for j, (prod_nt, prod_rhs) in enumerate(self.augmented_grammar):
                                if prod_nt == nt:
                                    # Remove 'DOT' from the item’s RHS
                                    item_rhs_without_dot = tuple([s for s in rhs if s != 'DOT'])
                                    if prod_rhs == item_rhs_without_dot:
                                        prod_num = j
                                        break
                            if prod_num != -1:
                                for follow_symbol in self.follow_sets.get(nt, set()):
                                    action = f"r{prod_num}"
                                    if action not in self.parsing_table[i][follow_symbol]:
                                        self.parsing_table[i][follow_symbol].append(action)
                except ValueError:
                    continue
            for nt in self.non_terminals:
                if (i, nt) in self.goto_table:
                    next_state = self.goto_table[(i, nt)]
                    self.parsing_table[i][nt].append(str(next_state))
    
    def parse_input(self, input_string):
        """Parse the input string using the SLR parsing table."""
        tokens = input_string.strip().split()
        tokens.append('$')
        stack = [0]
        pointer = 0
        actions = []
        while True:
            current_state = stack[-1]
            current_token = tokens[pointer]
            if current_token not in self.parsing_table[current_state]:
                actions.append(f"Error: Unexpected token {current_token}")
                return actions, False
            possible_actions = self.parsing_table[current_state][current_token]
            if not possible_actions:
                actions.append(f"Error: No action for state {current_state} and token {current_token}")
                return actions, False
            if len(possible_actions) > 1:
                actions.append(f"Error: Conflict in parsing table for state {current_state} and token {current_token}")
                return actions, False
            action = possible_actions[0]
            if action.startswith('s'):
                next_state = int(action[1:])
                stack.append(current_token)
                stack.append(next_state)
                actions.append(f"Shift {current_token}, go to state {next_state}")
                pointer += 1
            elif action.startswith('r'):
                prod_num = int(action[1:])
                prod_nt, prod_rhs = self.augmented_grammar[prod_num]
                for _ in range(2 * len(prod_rhs)):
                    stack.pop()
                current_state = stack[-1]
                stack.append(prod_nt)
                if prod_nt in self.parsing_table[current_state]:
                    goto_actions = self.parsing_table[current_state][prod_nt]
                    if goto_actions:
                        next_state = int(goto_actions[0])
                        stack.append(next_state)
                        actions.append(f"Reduce by {prod_nt} -> {' '.join(prod_rhs) if prod_rhs else 'ε'}, go to state {next_state}")
                    else:
                        actions.append(f"Error: No goto action for state {current_state} and non-terminal {prod_nt}")
                        return actions, False
                else:
                    actions.append(f"Error: No entry in parsing table for state {current_state} and non-terminal {prod_nt}")
                    return actions, False
            elif action == "acc":
                actions.append("Accept! Input successfully parsed.")
                return actions, True
            else:
                actions.append(f"Error: Invalid action {action}")
                return actions, False
    
    def format_parsing_table(self):
        """Format the parsing table for display without an extra 'State' column."""
        # Sort terminals and non-terminals for consistent display
        sorted_terminals = sorted(self.terminals)
        sorted_non_terminals = sorted(self.non_terminals)
        header = sorted_terminals + sorted_non_terminals
        rows = {}
        for state in range(len(self.canonical_collection)):
            row = []
            for terminal in sorted_terminals:
                actions = self.parsing_table[state].get(terminal, [])
                row.append('/'.join(actions) if actions else '')
            for non_terminal in sorted_non_terminals:
                actions = self.parsing_table[state].get(non_terminal, [])
                row.append('/'.join(actions) if actions else '')
            rows[state] = row
        # Create DataFrame using state numbers as the index
        return pd.DataFrame.from_dict(rows, orient='index', columns=header)
    
    def get_productions(self):
        """Get the list of productions in the format needed for parsing."""
        productions = []
        for i, (nt, rhs) in enumerate(self.augmented_grammar):
            if i == 0:
                continue
            prod_str = f"{i}. {nt} -> {' '.join(rhs) if rhs else 'ε'}"
            productions.append(prod_str)
        return productions
    
    def format_lr_items(self):
        """Format LR(0) items for display along with derivation order."""
        formatted = []
        for i, state in enumerate(self.canonical_collection):
            state_items = []
            for nt, rhs in state:
                formatted_rhs = []
                for symbol in rhs:
                    if symbol == 'DOT':
                        formatted_rhs.append('•')
                    else:
                        formatted_rhs.append(symbol)
                state_items.append(f"{nt} -> {' '.join(formatted_rhs)}")
            formatted.append((i, state_items))
        return formatted

def main():
    st.title("SLR Parser Generator")
    st.header("Grammar Input")
    example_grammar = """
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
    """
    grammar_input = st.text_area("Enter grammar (one production per line, use 'ε' for epsilon):", 
                                 value=example_grammar, height=200)
    parse_button = st.button("Generate SLR Parsing Table")
    if parse_button and grammar_input:
        try:
            parser = SLRParser(grammar_input)
            
            st.header("Grammar Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Terminals")
                st.write(", ".join(sorted(parser.terminals)))
            with col2:
                st.subheader("Non-terminals")
                st.write(", ".join(sorted(parser.non_terminals)))
            
            st.subheader("FIRST Sets")
            first_df = pd.DataFrame({
                'Non-terminal': sorted(parser.non_terminals),
                'FIRST Set': [", ".join(sorted(parser.first_sets.get(nt, []))) for nt in sorted(parser.non_terminals)]
            })
            st.dataframe(first_df)
            
            st.subheader("FOLLOW Sets")
            follow_df = pd.DataFrame({
                'Non-terminal': sorted(parser.non_terminals),
                'FOLLOW Set': [", ".join(sorted(parser.follow_sets.get(nt, []))) for nt in sorted(parser.non_terminals)]
            })
            st.dataframe(follow_df)
            
            st.subheader("Productions")
            for prod in parser.get_productions():
                st.write(prod)
            
            st.subheader("Canonical Collection of LR(0) Items (in order of derivation)")
            for i, items in parser.format_lr_items():
                st.write(f"State {i}:")
                for item in items:
                    st.write(f"  {item}")
                st.write("")
            
            st.subheader("SLR Parsing Table")
            parsing_table_df = parser.format_parsing_table()
            st.dataframe(parsing_table_df)
            
            st.header("Input Parsing Simulation")
            input_string = st.text_input("Enter input string to parse (space-separated tokens):", value="id + id * id")
            if st.button("Parse Input"):
                actions, success = parser.parse_input(input_string)
                st.subheader("Parsing Steps")
                for i, action in enumerate(actions):
                    st.write(f"{i+1}. {action}")
                if success:
                    st.success("Input string accepted!")
                else:
                    st.error("Input string rejected!")
        
        except Exception as e:
            st.error(f"Error in parsing: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()

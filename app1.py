import streamlit as st
import pandas as pd
from collections import defaultdict, deque
import base64
from streamlit_lottie import st_lottie
import requests
import json

# Add custom CSS for better styling
def add_custom_css():
    st.markdown("""
    <style>
    /* Define color scheme that works for both light and dark themes */
    :root {
        --primary-color: #6200EA;
        --primary-color-hover: #5000d0;
        --background-color: rgba(255, 255, 255, 0.05);
        --card-background: rgba(255, 255, 255, 0.1);
        --text-color: inherit;
        --border-color: rgba(120, 120, 120, 0.2);
        --shadow-color: rgba(0, 0, 0, 0.1);
        --highlight-background: rgba(98, 0, 234, 0.1);
        --success-color: #4CAF50;
        --error-color: #F44336;
        --info-color: #2196F3;
        --warning-color: #FFC107;
        --link-color: #FFD54F;
    }
    
    /* Light/dark mode compatible styles */
    .main {
        background-color: var(--background-color);
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    /* Fix for links on colored backgrounds */
    .header-container a, .sidebar-header a, [style*="background-color: var(--primary-color)"] a,
    .download-btn, .card a, .success-box a, .info-box a, .warning-box a, .error-box a {
        color: var(--link-color) !important;
        font-weight: bold;
        text-decoration: underline;
    }
    .header-container a:hover, .sidebar-header a:hover, [style*="background-color: var(--primary-color)"] a:hover,
    .download-btn:hover, .card a:hover {
        color: white !important;
        text-decoration: none;
    }
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 5px var(--shadow-color);
    }
    .stButton>button:hover {
        background-color: var(--primary-color-hover);
        box-shadow: 0 4px 8px var(--shadow-color);
        transform: translateY(-2px);
    }
    .stTextArea>div>div>textarea {
        font-family: 'Courier New', monospace;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 10px;
        background-color: var(--background-color);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: var(--background-color);
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: bold;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
        box-shadow: 0 2px 5px var(--shadow-color);
    }
    .stDataFrame {
        border-radius: 8px;
        box-shadow: 0 2px 8px var(--shadow-color);
        overflow: hidden;
    }
    .stExpander {
        background-color: var(--card-background);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px var(--shadow-color);
        border: 1px solid var(--border-color);
    }
    .card {
        background-color: var(--card-background);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px var(--shadow-color);
        border: 1px solid var(--border-color);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px var(--shadow-color);
    }
    .header-container {
        background: linear-gradient(90deg, var(--primary-color) 0%, rgba(179, 136, 255, 0.8) 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(98, 0, 234, 0.2);
    }
    .sidebar-header {
        background: linear-gradient(90deg, var(--primary-color) 0%, rgba(179, 136, 255, 0.8) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(98, 0, 234, 0.2);
    }
    .info-box {
        background-color: rgba(33, 150, 243, 0.1);
        border-left: 5px solid var(--info-color);
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: rgba(76, 175, 80, 0.1);
        border-left: 5px solid var(--success-color);
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: rgba(255, 193, 7, 0.1);
        border-left: 5px solid var(--warning-color);
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .error-box {
        background-color: rgba(244, 67, 54, 0.1);
        border-left: 5px solid var(--error-color);
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .download-btn {
        display: inline-block;
        background-color: var(--primary-color);
        color: white !important;
        padding: 0.6rem 1.2rem;
        text-decoration: none !important;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px var(--shadow-color);
        border: 2px solid #FFD54F;
    }
    .download-btn:hover {
        background-color: var(--primary-color-hover);
        box-shadow: 0 4px 8px var(--shadow-color);
        transform: translateY(-2px);
        border-color: white;
    }
    /* Token badges */
    .token-badge {
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 3px;
    }
    .terminal {
        background-color: rgba(98, 0, 234, 0.1);
        border: 1px solid var(--border-color);
        color: var(--text-color);
        padding: 10px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
    }
    /* Add specific light/dark mode styles */
    @media (prefers-color-scheme: dark) {
        .token-badge.terminal {
            background-color: rgba(98, 0, 234, 0.3);
            color: white;
        }
        .token-badge.non-terminal {
            background-color: rgba(179, 136, 255, 0.3);
            color: white;
        }
        .card h3, .expander h3, h2, h4 {
            color: #B388FF !important;
        }
        .item-row {
            background-color: rgba(255, 255, 255, 0.05) !important;
        }
    }
    @media (prefers-color-scheme: light) {
        .token-badge.terminal {
            background-color: #E3F2FD;
            color: #1976D2;
        }
        .token-badge.non-terminal {
            background-color: #F3E5F5;
            color: #7B1FA2;
        }
        .item-row {
            background-color: #F5F5F5 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Load Lottie animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --------------------------
# Grammar Parsing and Processing
# --------------------------

def parse_grammar(grammar_input):
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

def process_grammar(grammar):
    """
    Extract terminals, non-terminals, and create augmented grammar.
    Returns: start_symbol, terminals, non_terminals, augmented_grammar.
    """
    start_symbol = list(grammar.keys())[0]
    augmented_start = f"{start_symbol}'"
    # Augmented grammar: list of (LHS, production-tuple)
    augmented_grammar = [(augmented_start, (start_symbol,))]
    
    non_terminals = set(grammar.keys())
    terminals = set()
    
    for nt, productions in grammar.items():
        for prod in productions:
            symbols = prod.split()
            for symbol in symbols:
                if symbol not in non_terminals and symbol != '#':
                    terminals.add(symbol)
            # Add production to augmented grammar
            augmented_grammar.append((nt, tuple(symbols) if prod != '#' else tuple()))
    terminals.add('$')
    return start_symbol, terminals, non_terminals, augmented_grammar

# --------------------------
# FIRST and FOLLOW Sets
# --------------------------

def compute_first_sets(grammar, terminals, non_terminals):
    """Compute FIRST sets for all symbols."""
    first_sets = {}
    # Initialize FIRST sets for non-terminals and terminals.
    for nt in non_terminals:
        first_sets[nt] = set()
    for terminal in terminals:
        first_sets[terminal] = {terminal}
    
    # For any NT with epsilon production
    for nt, productions in grammar.items():
        if '#' in productions:
            first_sets[nt].add('#')
    
    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                if prod == '#':
                    continue
                symbols = prod.split()
                i = 0
                can_derive_epsilon = True
                while i < len(symbols) and can_derive_epsilon:
                    symbol = symbols[i]
                    if symbol in first_sets:
                        non_epsilon = first_sets[symbol] - {'#'}
                        old_len = len(first_sets[nt])
                        first_sets[nt].update(non_epsilon)
                        if len(first_sets[nt]) > old_len:
                            changed = True
                    can_derive_epsilon = ('#' in first_sets.get(symbol, set()))
                    i += 1
                if can_derive_epsilon and i == len(symbols) and '#' not in first_sets[nt]:
                    first_sets[nt].add('#')
                    changed = True
    return first_sets

def compute_follow_sets(grammar, non_terminals, start_symbol, first_sets):
    """Compute FOLLOW sets for all non-terminals."""
    follow_sets = {nt: set() for nt in non_terminals}
    follow_sets[start_symbol].add('$')
    
    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                if prod == '#':
                    continue
                symbols = prod.split()
                for i, symbol in enumerate(symbols):
                    if symbol in non_terminals:
                        if i < len(symbols) - 1:
                            next_seq = symbols[i+1:]
                            seq_first = compute_first_of_sequence(next_seq, first_sets)
                            non_epsilon = seq_first - {'#'}
                            old_len = len(follow_sets[symbol])
                            follow_sets[symbol].update(non_epsilon)
                            if len(follow_sets[symbol]) > old_len:
                                changed = True
                            if '#' in seq_first:
                                old_len = len(follow_sets[symbol])
                                follow_sets[symbol].update(follow_sets[nt])
                                if len(follow_sets[symbol]) > old_len:
                                    changed = True
                        else:
                            old_len = len(follow_sets[symbol])
                            follow_sets[symbol].update(follow_sets[nt])
                            if len(follow_sets[symbol]) > old_len:
                                changed = True
    return follow_sets

def compute_first_of_sequence(symbols, first_sets):
    """Compute FIRST set of a sequence of symbols."""
    if not symbols:
        return {'#'}
    result = set()
    all_epsilon = True
    for symbol in symbols:
        non_epsilon = first_sets[symbol] - {'#'}
        result.update(non_epsilon)
        if '#' not in first_sets[symbol]:
            all_epsilon = False
            break
    if all_epsilon:
        result.add('#')
    return result

# --------------------------
# LR(0) Items, Closure, and Goto
# --------------------------

def closure(items, grammar, non_terminals):
    """Compute the closure of a set of LR(0) items.
       Each item is a tuple (LHS, rhs-tuple) with 'DOT' marking the position.
    """
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
                    if next_symbol in non_terminals:
                        for prod in grammar.get(next_symbol, []):
                            if prod == '#':
                                new_item = (next_symbol, ('DOT',))
                            else:
                                new_item = (next_symbol, tuple(['DOT'] + prod.split()))
                            if new_item not in result:
                                new_items.add(new_item)
                                changed = True
            except ValueError:
                continue
        result.update(new_items)
    return frozenset(result)

def goto(items, symbol, grammar, non_terminals):
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
        return closure(next_items, grammar, non_terminals)
    else:
        return None

def build_canonical_collection(grammar, non_terminals, start_symbol):
    """Build the canonical collection of LR(0) items and the goto table."""
    augmented_start = f"{start_symbol}'"
    initial_item = (augmented_start, ('DOT', start_symbol))
    initial_state = closure({initial_item}, grammar, non_terminals)
    
    canonical_collection = [initial_state]
    goto_table = {}
    
    i = 0
    while i < len(canonical_collection):
        state = canonical_collection[i]
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
            next_state = goto(state, symbol, grammar, non_terminals)
            if next_state and next_state not in canonical_collection:
                canonical_collection.append(next_state)
            if next_state:
                goto_table[(i, symbol)] = canonical_collection.index(next_state)
        i += 1
    return canonical_collection, goto_table

# --------------------------
# Parsing Table Construction
# --------------------------

def construct_parsing_table(canonical_collection, goto_table, terminals, non_terminals, augmented_grammar, grammar, follow_sets, start_symbol):
    """Construct the SLR parsing table."""
    parsing_table = {}
    for i in range(len(canonical_collection)):
        parsing_table[i] = {}
        for symbol in terminals | non_terminals:
            parsing_table[i][symbol] = []
    
    for i, state in enumerate(canonical_collection):
        for item in state:
            nt, rhs = item
            try:
                dot_pos = rhs.index('DOT')
                # Shift action if dot is not at end
                if dot_pos < len(rhs) - 1:
                    next_symbol = rhs[dot_pos + 1]
                    if next_symbol in terminals and (i, next_symbol) in goto_table:
                        next_state = goto_table[(i, next_symbol)]
                        action = f"s{next_state}"
                        if action not in parsing_table[i][next_symbol]:
                            parsing_table[i][next_symbol].append(action)
                # Reduce or accept if dot is at end
                elif dot_pos == len(rhs) - 1 or (len(rhs) == 1 and rhs[0] == 'DOT'):
                    if nt == f"{start_symbol}'" and len(rhs) == 2 and rhs[1] == start_symbol:
                        parsing_table[i]['$'].append("acc")
                    else:
                        prod_num = -1
                        item_rhs = tuple(s for s in rhs if s != 'DOT')
                        for j, (prod_nt, prod_rhs) in enumerate(augmented_grammar):
                            if prod_nt == nt and prod_rhs == item_rhs:
                                prod_num = j
                                break
                        if prod_num != -1:
                            for follow_symbol in follow_sets.get(nt, set()):
                                action = f"r{prod_num}"
                                if action not in parsing_table[i][follow_symbol]:
                                    parsing_table[i][follow_symbol].append(action)
            except ValueError:
                continue
        for nt in non_terminals:
            if (i, nt) in goto_table:
                next_state = goto_table[(i, nt)]
                parsing_table[i][nt].append(str(next_state))
    return parsing_table

# --------------------------
# Parsing Simulation
# --------------------------

def parse_input(input_string, parsing_table, augmented_grammar, canonical_collection):
    """Parse the input string using the SLR parsing table.
       Returns (list of step actions, success flag).
    """
    tokens = input_string.strip().split()
    tokens.append('$')
    stack = [0]
    pointer = 0
    actions = []
    
    while True:
        current_state = stack[-1]
        current_token = tokens[pointer]
        if current_token not in parsing_table[current_state]:
            actions.append(f"Error: Unexpected token {current_token}")
            return actions, False
        possible_actions = parsing_table[current_state][current_token]
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
            prod_nt, prod_rhs = augmented_grammar[prod_num]
            for _ in range(2 * len(prod_rhs)):
                stack.pop()
            current_state = stack[-1]
            stack.append(prod_nt)
            if prod_nt in parsing_table[current_state]:
                goto_actions = parsing_table[current_state][prod_nt]
                if goto_actions:
                    next_state = int(goto_actions[0])
                    stack.append(next_state)
                    rhs_str = ' '.join(prod_rhs) if prod_rhs else '#'
                    actions.append(f"Reduce by {prod_nt} -> {rhs_str}, go to state {next_state}")
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

# --------------------------
# Formatting Functions for Display
# --------------------------

def format_parsing_table(parsing_table, canonical_collection, terminals, non_terminals):
    """Format the parsing table into a DataFrame (without an extra 'State' column)."""
    sorted_terminals = sorted(terminals)
    sorted_non_terminals = sorted(non_terminals)
    header = sorted_terminals + sorted_non_terminals
    rows = {}
    for state in range(len(canonical_collection)):
        row = []
        for terminal in sorted_terminals:
            acts = parsing_table[state].get(terminal, [])
            row.append('/'.join(acts) if acts else '')
        for nt in sorted_non_terminals:
            acts = parsing_table[state].get(nt, [])
            row.append('/'.join(acts) if acts else '')
        rows[state] = row
    return pd.DataFrame.from_dict(rows, orient='index', columns=header)

def get_productions(augmented_grammar):
    """Return a list of productions (excluding the augmented production) as strings."""
    productions = []
    for i, (nt, rhs) in enumerate(augmented_grammar):
        if i == 0:
            continue
        prod_str = f"{i}. {nt} -> {' '.join(rhs) if rhs else '#'}"
        productions.append(prod_str)
    return productions

def format_lr_items(canonical_collection):
    """Format LR(0) items for display with derivation order."""
    formatted = []
    for i, state in enumerate(canonical_collection):
        state_items = []
        for nt, rhs in state:
            formatted_rhs = ['•' if symbol == 'DOT' else symbol for symbol in rhs]
            state_items.append(f"{nt} -> {' '.join(formatted_rhs)}")
        formatted.append((i, state_items))
    return formatted

# --------------------------
# Main Function (Enhanced Streamlit UI)
# --------------------------

def main():
    st.set_page_config(
        page_title="SLR Parser Generator",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    add_custom_css()
    
    # Load Lottie animation
    lottie_coding = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json')
    
    # Header with improved styling
    st.markdown("""
    <div class="header-container">
        <h1 style="margin-top: 0;">SLR Parser Generator</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">
            A powerful tool for generating SLR parsing tables and analyzing context-free grammars
        </p>
        <p><a href="https://github.com/singh-sudhir16/SLR-parse-table-generator" target="_blank">View Source Code</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with improved styling
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h2 style="margin: 0;">Grammar Input</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Add Lottie animation
        st_lottie(lottie_coding, height=200, key="coding")
        
        example_grammar = """
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
        """
        grammar_input = st.text_area(
            "Enter your grammar (one production per line, use '#' for epsilon):",
            value=example_grammar,
            height=200,
            help="Example format: A -> B C | D"
        )
        
        st.markdown("""
        <div class="info-box">
            <h4 style="margin-top: 0;">Tips</h4>
            <ul>
                <li>Use '#' to represent epsilon (empty string)</li>
                <li>The first non-terminal is considered the start symbol</li>
                <li>Separate symbols with spaces</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate Parser", key="generate_btn", use_container_width=True):
                st.session_state.generate_clicked = True
        with col2:
            if st.button("Clear", key="clear_btn", use_container_width=True):
                st.session_state.generate_clicked = False
    
    if st.session_state.get('generate_clicked', False):
        try:
            # Processing
            grammar = parse_grammar(grammar_input)
            start_symbol, terminals, non_terminals, augmented_grammar = process_grammar(grammar)
            first_sets = compute_first_sets(grammar, terminals, non_terminals)
            follow_sets = compute_follow_sets(grammar, non_terminals, start_symbol, first_sets)
            canonical_collection, goto_table = build_canonical_collection(grammar, non_terminals, start_symbol)
            parsing_table = construct_parsing_table(canonical_collection, goto_table, terminals, non_terminals, 
                                                 augmented_grammar, grammar, follow_sets, start_symbol)
            
            # Success message
            st.markdown("""
            <div class="success-box">
                <h3 style="margin-top: 0;">✅ Parser Generated Successfully</h3>
                <p>Your SLR parser has been generated. Explore the results in the tabs below.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create tabs with improved styling
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Grammar Analysis", "📝 Productions", "🔍 LR(0) Items", "📋 Parsing Table", "🧪 Test Parser"])
            
            with tab1:
                st.markdown("""
                <h2 style="border-bottom: 2px solid var(--primary-color); padding-bottom: 8px;">Grammar Analysis</h2>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    <div class="card">
                        <h3 style="margin-top: 0;">Terminals</h3>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
                    """, unsafe_allow_html=True)
                    
                    for terminal in sorted(terminals):
                        st.markdown(f"""
                        <span class="token-badge terminal">{terminal}</span>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="card">
                        <h3 style="margin-top: 0;">Non-terminals</h3>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
                    """, unsafe_allow_html=True)
                    
                    for nt in sorted(non_terminals):
                        st.markdown(f"""
                        <span class="token-badge non-terminal">{nt}</span>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
                
                with st.expander("FIRST Sets", expanded=True):
                    first_df = pd.DataFrame({
                        'Non-terminal': sorted(non_terminals),
                        'FIRST Set': [", ".join(sorted(first_sets.get(nt, []))) for nt in sorted(non_terminals)]
                    })
                    
                    st.markdown("""
                    <div class="card">
                        <h3 style="color: #6200EA; margin-top: 0;">FIRST Sets Table</h3>
                    """, unsafe_allow_html=True)
                    st.dataframe(first_df, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with st.expander("FOLLOW Sets", expanded=True):
                    follow_df = pd.DataFrame({
                        'Non-terminal': sorted(non_terminals),
                        'FOLLOW Set': [", ".join(sorted(follow_sets.get(nt, []))) for nt in sorted(non_terminals)]
                    })
                    
                    st.markdown("""
                    <div class="card">
                        <h3 style="color: #6200EA; margin-top: 0;">FOLLOW Sets Table</h3>
                    """, unsafe_allow_html=True)
                    st.dataframe(follow_df, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            
            with tab2:
                st.markdown("""
                <h2 style="border-bottom: 2px solid var(--primary-color); padding-bottom: 8px;">Productions</h2>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="card">
                    <h3 style="margin-top: 0;">Grammar Productions</h3>
                    <div style="margin-top: 15px;">
                """, unsafe_allow_html=True)
                
                for prod in get_productions(augmented_grammar):
                    st.markdown(f"""
                    <div class="item-row" style="display: flex; align-items: center; margin-bottom: 10px; 
                    padding: 10px; border-radius: 8px;">
                        <div style="background-color: var(--primary-color); color: white; width: 30px; height: 30px; 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        margin-right: 15px;">📌</div>
                        <div class="terminal" style="font-family: 'Courier New', monospace; font-size: 16px;">{prod}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
            
            with tab3:
                st.markdown("""
                <h2 style="border-bottom: 2px solid var(--primary-color); padding-bottom: 8px;">Canonical Collection of LR(0) Items</h2>
                """, unsafe_allow_html=True)
                
                # Create a vertical layout for states instead of a grid
                formatted_items = format_lr_items(canonical_collection)
                
                for i, items in formatted_items:
                    st.markdown(f"""
                    <div class="card">
                        <h3 style="margin-top: 0; display: flex; align-items: center;">
                            <span style="background-color: var(--primary-color); color: white; width: 40px; height: 40px; 
                            border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                            margin-right: 10px; font-size: 1.2rem;">I{i}</span>
                            State {i}
                        </h3>
                    """, unsafe_allow_html=True)
                    
                    if items:  # Only display the container if there are items
                        st.markdown("""
                        <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 8px;">
                        """, unsafe_allow_html=True)
                        
                        for item in items:
                            st.markdown(f"""
                            <div class="terminal" style="font-family: 'Courier New', monospace;
                            display: flex; align-items: center; padding: 10px; border-radius: 6px;">
                                <span style="color: var(--primary-color); margin-right: 10px; font-weight: bold; font-size: 18px;">•</span>
                                <span style="font-size: 16px;">{item}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        # Display a message if there are no items
                        st.markdown("""
                        <div style="margin-top: 15px; padding: 12px; background-color: rgba(98, 0, 234, 0.05); 
                        border-radius: 6px; text-align: center; font-style: italic; color: #666;">
                            No items in this state
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            with tab4:
                st.markdown("""
                <h2 style="border-bottom: 2px solid var(--primary-color); padding-bottom: 8px;">SLR Parsing Table</h2>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="card">
                    <h3 style="margin-top: 0;">Parsing Table</h3>
                    <p>The table below shows the actions and goto functions for each state.</p>
                """, unsafe_allow_html=True)
                
                parsing_table_df = format_parsing_table(parsing_table, canonical_collection, terminals, non_terminals)
                st.dataframe(parsing_table_df, use_container_width=True)
                
                # Add download button for the parsing table
                csv = parsing_table_df.to_csv(index=True)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="parsing_table.csv" class="download-btn">📥 Download Parsing Table</a>'
                st.markdown(href, unsafe_allow_html=True)
                
                st.markdown("""
                <div style="margin-top: 20px;">
                    <h4>Legend:</h4>
                    <ul>
                        <li><strong>sN</strong>: Shift and go to state N</li>
                        <li><strong>rN</strong>: Reduce using production N</li>
                        <li><strong>acc</strong>: Accept the input</li>
                        <li><strong>N</strong> (in goto section): Go to state N</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with tab5:
                st.markdown("""
                <h2 style="border-bottom: 2px solid var(--primary-color); padding-bottom: 8px;">Test Your Parser</h2>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="card">
                    <h3 style="margin-top: 0;">Input String</h3>
                    <p>Enter a string to parse using your generated SLR parser.</p>
                """, unsafe_allow_html=True)
                
                test_input = st.text_input("Enter input string (space-separated tokens):", 
                                          value="id + id * id", 
                                          help="Example: id + id * id")
                
                if st.button("Parse Input", key="parse_btn"):
                    if test_input:
                        actions, success = parse_input(test_input, parsing_table, augmented_grammar, canonical_collection)
                        
                        if success:
                            st.markdown("""
                            <div class="success-box">
                                <h3 style="margin-top: 0;">✅ Parsing Successful</h3>
                                <p>The input string was successfully parsed!</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="error-box">
                                <h3 style="margin-top: 0;">❌ Parsing Failed</h3>
                                <p>The input string could not be parsed. See details below.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div style="margin-top: 20px;">
                            <h4 style="color: #6200EA;">Parsing Steps:</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for i, action in enumerate(actions):
                            if "Error" in action:
                                st.markdown(f"""
                                <div class="error-box" style="padding: 10px; border-radius: 8px; margin-bottom: 8px;">
                                    <strong>Step {i+1}:</strong> {action}
                                </div>
                                """, unsafe_allow_html=True)
                            elif "Accept" in action:
                                st.markdown(f"""
                                <div class="success-box" style="padding: 10px; border-radius: 8px; margin-bottom: 8px;">
                                    <strong>Step {i+1}:</strong> {action}
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="terminal" style="padding: 10px; border-radius: 8px; margin-bottom: 8px;">
                                    <strong>Step {i+1}:</strong> {action}
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.warning("Please enter an input string to parse.")
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        except Exception as e:
            st.markdown("""
            <div class="error-box">
                <h3 style="margin-top: 0;">❌ Error</h3>
                <p>An error occurred while generating the parser.</p>
            </div>
            """, unsafe_allow_html=True)
            st.error(f"Error: {str(e)}")
            import traceback
            with st.expander("Show Error Details"):
                st.code(traceback.format_exc())
    else:
        # Welcome message when no parser is generated yet
        st.markdown("""
        <div class="card">
            <h2 style="margin-top: 0;">Welcome to the SLR Parser Generator</h2>
            <p style="font-size: 1.1rem;">
                This tool helps you analyze context-free grammars and generate SLR parsing tables.
            </p>
            <h3>Getting Started</h3>
            <ol>
                <li>Enter your grammar in the sidebar</li>
                <li>Click "Generate Parser" to analyze your grammar</li>
                <li>Explore the results in the different tabs</li>
                <li>Test your parser with sample input strings</li>
            </ol>
            <div class="info-box">
                <h4 style="margin-top: 0;">What is SLR Parsing?</h4>
                <p>
                    Simple LR (SLR) parsing is a bottom-up parsing technique used for context-free grammars.
                    It builds a parsing table based on the FIRST and FOLLOW sets of the grammar.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
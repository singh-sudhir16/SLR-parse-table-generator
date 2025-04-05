# SLR Parser Generator

This project implements an SLR parser that takes a grammar as input, constructs the canonical collection of LR(0) items, builds the SLR parsing table, and simulates the parsing process. The graphical interface is built using [Streamlit](https://streamlit.io/), allowing users to easily enter grammars, view detailed parsing tables, and step through the parsing process.

---

##  Features

- **Grammar Input & Augmentation**  
  Enter grammar productions (using `#` for epsilon). The parser automatically augments the grammar by creating a new start symbol.

- **FIRST & FOLLOW Set Calculation**  
  Computes FIRST and FOLLOW sets for the grammar, essential for constructing the parsing table.

- **Canonical Collection of LR(0) Items**  
  Constructs and displays the collection of LR(0) items in the order they are derived.

- **SLR Parsing Table Construction**  
  Builds a complete SLR parsing table with shift, reduce, and accept actions. The table is formatted for easy viewing without any extra columns.

- **Parsing Simulation**  
  Simulate the parsing process of an input string step-by-step, with detailed logs showing shift-reduce actions.

- **Streamlit GUI**  
  A user-friendly interface to enter grammars, view analysis results (terminals, non-terminals, FIRST and FOLLOW sets), canonical LR(0) items, and parsing tables. It also allows for testing input strings against the constructed parser.

---

##  How to Enter Grammar Input

The grammar is entered **one production per line** in the following format:

A -> c | d | A


### 🧾 Input Format Rules

- Use `->` (with spaces on both sides) to separate the LHS from RHS.
- Use `|` (with spaces on both sides) to separate multiple productions.
- Use **spaces between all terminals and non-terminals** (e.g., `E -> E + T`).
- Use `#` to denote epsilon (empty string).

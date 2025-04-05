# 📘 SLR Parser Generator

An interactive **SLR(1) parser generator** built with Python and Streamlit. This tool allows users to input a grammar, visualize the construction of LR(0) items, generate the SLR parsing table, and simulate parsing of strings. The entire process is made intuitive through a modern web-based GUI.

> 🚀 [Try it live on Streamlit](https://your-deployed-streamlit-link)  

---

## 🎯 Features

### 🔤 Grammar Input & Augmentation
- Input grammar productions using a simple syntax.
- Automatic augmentation of grammar by adding a new start symbol.
- Supports `#` to represent **epsilon** (empty string).

### 🧮 FIRST & FOLLOW Sets
- Computes **FIRST** and **FOLLOW** sets for non-terminals.
- Core building blocks for SLR table generation.

### 📚 Canonical Collection of LR(0) Items
- Generates and displays LR(0) items.
- Clearly shows state transitions and derivations.

### 📋 SLR Parsing Table
- Constructs the **SLR parsing table**:
  - Shift (`s`), Reduce (`r`), and Accept (`acc`) actions.
- Easy-to-read tabular format for analysis and debugging.

### 🧪 Parsing Simulation
- Step-by-step simulation of the parsing process.
- Detailed logs show shift/reduce decisions at each step.

### 🖥️ Streamlit Web Interface
- Clean and interactive frontend using **Streamlit**.
- Easily enter grammars, view all parsing components, and test strings.
- No installations needed — runs directly in the browser!

---

## 🧾 Grammar Input Format

- Each production should be on a **new line**.
- Use `->` (with spaces) to separate LHS and RHS.
- Use `|` (with spaces) for multiple alternatives.
- Separate all terminals and non-terminals with spaces.
- Use `#` to denote epsilon (empty string).

**Example:**
```
E -> E + T | T  
T -> T * F | F  
F -> ( E ) | id  
```

---

## 🛠️ Installation (Local Run)

```bash
git clone https://github.com/your-username/SLR-Parser-Frontend.git
cd SLR-Parser-Frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Deployment

The app is deployed on **Streamlit Cloud** for public use.  
📍 [Live Demo](https://slr-parse-table-generator.streamlit.app/)

---

## 📂 Project Structure

```
├── app.py                 # Streamlit frontend
├── parser_engine.py       # Core SLR parser logic
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 👨‍💻 Author
- Shahid Sheikh
- Sudhir Singh
- Manas Bhardwaj

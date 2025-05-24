# 🧮 Interactive Math Problem Solver with Claude 4

An interactive terminal-based math problem solver that uses Claude 4's code execution tool to solve mathematical problems step-by-step, generate visualizations, and save detailed reports.

## ✨ Main Features

- **Natural Language Input**: Ask math questions in plain English
- **Real-Time Streaming**: Watch Claude work through problems step by step
- **Step-by-Step Solutions**: Get detailed explanations with code execution
- **Automatic Visualizations**: Plots and charts saved as PNG files
- **Markdown Reports**: Complete solutions saved with code and explanations

## 🚀 Quick Setup

### Prerequisites

1. **Python 3.8+** installed
2. **Anthropic API Key** - Get one from [console.anthropic.com](https://console.anthropic.com)

### Installation

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set your API key**:

   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

3. **Run the solver**:

   ```bash
   python math_solver.py
   ```

## 📱 Usage Example

```bash
$ python math_solver.py

🧮 Interactive Math Problem Solver with Claude 4
============================================================
Ask me any math question and I'll solve it step by step!
Type 'quit', 'exit', or 'q' to end the session.
============================================================

📝 Question #1: Find the derivative of x^2 * sin(x) and plot both functions

🤔 Thinking about: Find the derivative of x^2 * sin(x) and plot both functions
💭 Claude is working...
📝 Response: I'll solve this step by step...
🔧 Using tool: code_execution
✅ Completed: end_turn

📥 Downloading 1 file(s)...
✅ Downloaded: derivative_plot.png
📝 Generating report...

✅ Solution complete!
📄 Report saved: math_solver_output/reports/20250128_143022_derivative.md
🖼️  Visualizations: 1 file(s) saved
```

## 📂 Output Structure

```
math_solver_output/
├── images/          # Generated plots and visualizations
│   └── derivative_plot.png
└── reports/         # Detailed markdown reports
    └── 20250128_143022_derivative.md
```

## 🧪 Demo Problems

Try the demo script to see example problems:

```bash
python demo_problems.py
```

This shows categorized example problems from basic algebra to advanced calculus.

## 🎯 What Can It Solve?

- **Algebra**: Equations, systems, polynomials
- **Calculus**: Derivatives, integrals, limits
- **Statistics**: Data analysis, distributions, regression
- **Geometry**: Areas, volumes, trigonometry
- **Financial Math**: Interest, investments, payments

## 🔧 Next Steps to Enhance

Want to extend this application? Consider adding:

- **Web interface** using Flask or Streamlit
- **Problem history** and session management
- **Custom visualization themes** and styling
- **Export options** (PDF, LaTeX, etc.)
- **Multi-language support** for problem input
- **Advanced plotting** with interactive charts
- **Problem templates** for common question types
- **Integration** with Jupyter notebooks

## 📚 Learn More

- [Claude 4 Documentation](https://docs.anthropic.com/en/docs/models-overview)
- [Code Execution Tool Guide](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/code-execution-tool)
- [Anthropic API Reference](https://docs.anthropic.com/en/api)

---

**Built with Claude 4's Code Execution Tool**

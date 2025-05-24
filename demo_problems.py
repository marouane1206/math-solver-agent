#!/usr/bin/env python3
"""
Demo problems for the Interactive Math Problem Solver

This script contains example problems that showcase different capabilities
of the math solver. You can use this as inspiration for your own questions.
"""

# Sample problems organized by difficulty and topic
DEMO_PROBLEMS = {
    "Beginner": [
        "What is 15% of 240?",
        "Solve for x: 3x + 7 = 22",
        "Find the area of a circle with radius 5",
        "Convert 45 degrees to radians",
        "Calculate the hypotenuse of a right triangle with legs 3 and 4",
    ],
    "Intermediate": [
        "Solve the quadratic equation: 2x^2 + 5x - 3 = 0",
        "Graph y = x^2 - 4x + 3 and find its vertex",
        "Calculate mean, median, and standard deviation of [12, 15, 18, 22, 25, 28]",
        "Find where f(x) = x^3 - 3x^2 + 2 crosses the x-axis",
        "Solve the system of equations: 2x + 3y = 7, x - y = 1",
        "Find the area of a triangle with sides 5, 6, and 7",
        "Calculate compound interest: $1000 at 5% annually for 10 years",
    ],
    "Advanced": [
        "Find the derivative of sin(x) * e^x and plot both functions",
        "Calculate the integral of x^2 from 0 to 5",
        "Use Newton's method to find the root of x^3 - 2x - 5 = 0",
        "Perform linear regression on data points and plot the results",
        "Find the Fourier series of a square wave",
        "Solve the differential equation dy/dx = x*y with initial condition y(0) = 1",
        "Calculate the eigenvalues of a 3x3 matrix",
    ],
    "Statistics & Data Science": [
        "Generate 1000 random normal samples and create a histogram",
        "Calculate correlation between two datasets",
        "Perform a t-test on two groups of data",
        "Create a box plot showing quartiles and outliers",
        "Fit a polynomial regression to noisy data",
        "Generate and visualize a binomial distribution",
    ],
    "Calculus & Analysis": [
        "Find critical points of f(x) = x^4 - 4x^3 + 6x^2 - 4x + 1",
        "Calculate the Taylor series expansion of e^x around x=0",
        "Find the area between curves y = x^2 and y = 2x",
        "Optimize f(x,y) = x^2 + y^2 subject to x + y = 1",
        "Find the limit of (sin(x)/x) as x approaches 0",
        "Plot the convergence of a series",
    ],
    "Geometry & Trigonometry": [
        "Convert complex number 3 + 4i to polar form and visualize",
        "Calculate all angles in a triangle with sides 3, 4, 5",
        "Find the distance between two points in 3D space",
        "Calculate the volume of a sphere with radius 7",
        "Graph sin(x), cos(x), and tan(x) on the same plot",
        "Find the equation of a line passing through two points",
    ],
    "Financial Mathematics": [
        "Compare simple vs compound interest over 20 years",
        "Calculate monthly payments for a $300,000 mortgage at 4.5%",
        "Determine how much to save monthly to reach $100,000 in 15 years",
        "Calculate the present value of future cash flows",
        "Model investment growth with different scenarios",
        "Calculate break-even point for a business model",
    ],
}


def print_demo_problems():
    """Print all demo problems organized by category."""
    print("🧮 Demo Problems for Interactive Math Solver")
    print("=" * 60)
    print("Here are example problems you can try, organized by difficulty:\n")

    for category, problems in DEMO_PROBLEMS.items():
        print(f"### {category}")
        print("-" * (len(category) + 4))
        for i, problem in enumerate(problems, 1):
            print(f"{i:2d}. {problem}")
        print()

    print("💡 Tips:")
    print("   • Copy and paste any question into the math solver")
    print("   • Modify problems to suit your specific needs")
    print("   • Ask follow-up questions to dive deeper")
    print("   • All visualizations and reports will be saved automatically")
    print("\n🚀 Start the solver with: python math_solver.py")


def get_random_problem(category=None):
    """Get a random problem from a specific category or all categories."""
    import random

    if category and category in DEMO_PROBLEMS:
        return random.choice(DEMO_PROBLEMS[category])
    else:
        # Pick from all problems
        all_problems = []
        for problems in DEMO_PROBLEMS.values():
            all_problems.extend(problems)
        return random.choice(all_problems)


def main():
    """Main function to run the demo."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "random":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        problem = get_random_problem(category)
        print(f"Random problem: {problem}")
    else:
        print_demo_problems()


if __name__ == "__main__":
    main()

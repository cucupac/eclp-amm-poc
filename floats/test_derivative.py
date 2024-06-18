import sympy as sp

# Define the symbols
input, reserve_out, λ_sq, f, offset, pc1, pc2, pc3, pc4, pc5 = sp.symbols('input reserve_out λ_sq f offset pc1 pc2 pc3 pc4 pc5')

# Define the eclp function symbolically
xp = pc1 + f * input
xp_sq = xp**2
term_1 = (-xp) * pc2
term_2 = sp.sqrt(pc4 - (xp_sq / λ_sq))
quotient = (term_1 - term_2) / pc3
post_out_bal = quotient + offset
eclp_func = reserve_out - post_out_bal

# Calculate the derivative symbolically
eclp_derivative = sp.diff(eclp_func, input)

# Simplify the result
eclp_derivative_simplified = sp.simplify(eclp_derivative)

# Display the symbolic derivative
print(f"\n\nSymbolic Derivative: {eclp_derivative_simplified}")

# Define the manual derivative for comparison
xp_manual = pc1 + f * input
xp_sq_manual = xp_manual**2
root_term_manual = sp.sqrt(pc4 - (xp_sq_manual / λ_sq))
denominator_manual = λ_sq * root_term_manual

# Substitute pc5 = f / pc3 into the manual derivative
manual_derivative = (f / pc3) * (pc2 - (xp_manual / denominator_manual))

# Simplify the manual derivative
manual_derivative_simplified = sp.simplify(manual_derivative)

# Display the manual derivative
print(f"\n\nManual Derivative: {manual_derivative_simplified}")

# Compare the symbolic and manual derivatives
are_equal = sp.simplify(eclp_derivative_simplified - manual_derivative_simplified) == 0
print(f"\n\nAre the derivatives equal? {are_equal}")



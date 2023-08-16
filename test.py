def calculate_shippable_sculptures(N, X, T, weights):
    shippable_sculptures = []
    for i, weight in enumerate(weights):
        if weight == X:
            shippable_sculptures.append(i)
        elif weight < X:
            time_needed = X - weight
            if time_needed <= T:
                shippable_sculptures.append(i)
                T -= time_needed
        elif weight > X:
            time_needed = weight - X
            if time_needed <= T:
                shippable_sculptures.append(i)
                T -= time_needed
    return shippable_sculptures

# Take input from the user
N, X, T = map(int, input("Enter N, X, T: ").split())
weights = list(map(int, input("Enter sculpture weights: ").split()))

# Calculate the indexes of shippable sculptures
shippable_indexes = calculate_shippable_sculptures(N, X, T, weights)

# Print the result
print("Indexes of shippable sculptures:", shippable_indexes)

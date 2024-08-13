def construction_bonus(t3_count: int, t2_count: int, t1_count: int) -> float:
    bonuses = [
        (t3_count, 0.40, 0.15, 0.06, 0.028),  # T3: base 40% + diminishing coefficients
        (t2_count, 0.25, 0.18, 0.08, 0.040),  # T2: base 25% + diminishing coefficients
        (t1_count, 0.10, 0.20, 0.10, 0.050),  # T1: base 10% + diminishing coefficients
    ]

    # Sort bonuses by base value in descending order
    sorted_bonuses = sorted(bonuses, key=lambda x: x[1], reverse=True)

    total_bonus = 0.0
    applied_bonuses = 0  # Track how many bonuses have been applied
    highest_tier_coeffs = None  # Store the coefficients of the highest tier applied

    for count, base_bonus, *coeffs in sorted_bonuses:
        if count > 0 and highest_tier_coeffs is None:  # Determine the highest tier and use those coefficients
            highest_tier_coeffs = coeffs

        for _ in range(count):
            if applied_bonuses == 0:
                total_bonus += base_bonus  # Full bonus for the first module
            elif applied_bonuses == 1:
                total_bonus += base_bonus * highest_tier_coeffs[0]   # Apply 2nd bonus
            elif applied_bonuses == 2:
                total_bonus += base_bonus * highest_tier_coeffs[1]  # Apply 3rd bonus
            else:
                total_bonus += base_bonus * highest_tier_coeffs[2]  # Apply subsequent bonuses
            applied_bonuses += 1

    return min(total_bonus, 0.50)  # Cap total bonus at 50%


tests = [
    ((0, 0, 1), 10),
    ((0, 0, 2), 12),
    ((0, 0, 3), 13),
    ((0, 1, 0), 25),
    ((0, 1, 1), 27),
    ((0, 1, 2), 28),
    ((0, 1, 3), 28),
    ((0, 2, 0), 30),
    ((0, 2, 1), 30),
    ((0, 2, 2), 31),
    ((0, 2, 3), 31),
    ((0, 3, 0), 32),
    ((0, 3, 1), 32),
    ((0, 3, 2), 32),
    ((0, 3, 3), 33),
    ((1, 0, 0), 40),
    ((1, 0, 1), 42),
    ((1, 0, 2), 42),
    ((1, 0, 3), 43),
    ((1, 1, 0), 44),
    ((1, 1, 1), 44),
    ((1, 1, 2), 45),
    ((1, 1, 3), 45),
    ((1, 2, 0), 45),
    ((1, 2, 1), 46),
    ((1, 2, 2), 46),
    ((1, 2, 3), 46),
    ((1, 3, 0), 46),
    ((1, 3, 1), 46),
    ((1, 3, 2), 47),
    ((1, 3, 3), 47),
    ((2, 0, 0), 46),
    ((2, 0, 1), 47),
    ((2, 0, 2), 47),
    ((2, 0, 3), 47),
    ((2, 1, 0), 48),
    ((2, 1, 1), 48),
    ((2, 1, 2), 48),
    ((2, 1, 3), 48),
    ((2, 2, 0), 48),
    ((2, 2, 1), 49),
    ((2, 2, 2), 49),
    ((2, 2, 3), 49),
    ((2, 3, 0), 49),
    ((2, 3, 1), 49),
    ((2, 3, 2), 49),
    ((2, 3, 3), 49),
    ((3, 0, 0), 48),
    ((3, 0, 1), 49),
    ((3, 0, 2), 49),
    ((3, 0, 3), 49),
    ((3, 1, 0), 49),
    ((3, 1, 1), 49),
    ((3, 1, 2), 50),
    ((3, 1, 3), 50),
    ((3, 2, 0), 50),
    ((3, 2, 1), 50),
    ((3, 2, 2), 50),
    ((3, 2, 3), 50),
    ((3, 3, 0), 50),
    ((3, 3, 1), 50),
    ((3, 3, 2), 50),
    ((3, 3, 3), 50),
]  # Tuple(t3, t2, t1), in-game % value

total_offsets = 0
for t in tests:
    t3, t2, t1 = t[0][0], t[0][1], t[0][2]
    result = round(construction_bonus(t3, t2, t1) * 100)
    total_offsets += 1 if t[-1] - result else 0
    if (t[-1] - result) != 0:
        print(f"Case: {t}, Expected: {t[-1]}, Result: {result}%, Diff: {t[-1] - result}%")

print(total_offsets)

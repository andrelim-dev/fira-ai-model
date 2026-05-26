def determine_risk_profile(monthly_income, monthly_expense, investment_goal, investment_budget, investment_experience):
    # Count savings ratio
    savings = monthly_income - monthly_expense
    savings_ratio = savings / monthly_income

    score = 0

    # Savings ratio
    if savings_ratio < 0.2:
        score += 1
    elif savings_ratio < 0.5:
        score += 2
    else:
        score += 3
    
    # Investment goal
    if investment_goal == 'Capital Preservation':
        score += 1
    elif investment_goal == 'Long-Term Growth':
        score += 2
    elif investment_goal == 'Aggressive Growth':
        score += 3
    
    # Investment budget
    if investment_budget < 1000000:
        score += 1
    elif investment_budget < 5000000:
        score += 2
    else:
        score += 3
    
    # Investment experience
    if investment_experience == 'Beginner':
        score += 1
    elif investment_experience == 'Intermediate':
        score += 2
    elif investment_experience == 'Expert':
        score += 3

    # Determine risk profile
    if score <= 5:
        return 'Conservative'
    elif score <= 8:
        return 'Moderate'
    else:
        return 'Aggressive'
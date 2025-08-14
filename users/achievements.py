ACHIEVEMENTS = {
    "first_quiz": "Completed the first quiz",
    "ten_quizzes": "Completed 10 quizzes",
    "high_scorer": "Achieved a score of 90% or more in a quiz",
    "consistent_scorer": "Maintained an average score of 75% or more",
}

def award_achievements(user, score):
    """
    Awards achievements to a user based on their activity and performance.
    
    """
    user_achievements = set(user.achievements.split(", ")) if user.achievements else set()

    if user.quizzes_completed == 1 and "first_quiz" not in user_achievements:
        user_achievements.add("first_quiz")

    if user.quizzes_completed == 10 and "ten_quizzes" not in user_achievements:
        user_achievements.add("ten_quizzes")

    if score >= 90 and "high_scorer" not in user_achievements:
        user_achievements.add("high_scorer")

    if user.average_quiz_percentage >= 75 and "consistent_scorer" not in user_achievements:
        user_achievements.add("consistent_scorer")

    user.achievements = ", ".join(user_achievements)
    user.save()

from cgpa import CalculateTotalScore

score = CalculateTotalScore(88,88,92,94,5)
print(score.first_formula())
print(score.second_formula())
# best = score.best_score()
# print(best)
total_score = score.best_score()
total = total_score + \
    score.pa_bonus if total_score <= 95 else total_score + \
    (100 - total_score)
grade, point = score.get_grade(total)
print(round(total,2), grade, point)
import numpy as np

subjects = ["Матан", "Физика", "Инфо", "Англ", "История"]

raw = np.array([
    [78,     85,     92,     70,     66],
    [55,     48,     np.nan, 62,     71],
    [91,     88,     95,     84,     79],
    [34,     41,     38,     np.nan, 52],
    [67,     72,     58,     75,     80],
    [np.nan, 65,     70,     68,     59],
    [88,     -1,     81,     90,     94],
    [45,     52,     49,     58,     61],
])

w = np.array([0.30, 0.25, 0.25, 0.10, 0.10])

#1.1
raw_copy = raw.copy()
invalid = np.isnan(raw) | (raw < 0) #Использую |, а не or т.к. работаем с numpy массивамиc
clean = raw.copy()
clean[invalid] = np.nan
assert np.array_equal(raw, raw_copy, equal_nan=True)
print(f'Количество невалидных: {invalid.sum()}')
print(f'Количество невалидных по студентам: {invalid.sum(axis=1)}')#1 т.к. сворачивается по 0 оси и выводит 1
print(f'Количество невалидных по предметам: {invalid.sum(axis=0)}')# так же, как с 0, но наборот

#1.2
rooted = np.full((8, 5), np.nan)
np.sqrt(raw, out=rooted, where=~invalid) #без where могут передаться некоректные значения, которые функция обработая, выведет nan или warning. Нужно работат с данными с примененной инвертированной маской инвалид
np.multiply(rooted, 10, out=rooted)

#2.1
average_subject_score = np.nanmean(clean, axis=0)
average_student_score = np.nanmean(clean, axis=1) #просто mean выдало бы nan во всех колонках/столбцах, где был nan

#2.2
std_subject = np.nanstd(clean, ddof=1, axis=0)
print(std_subject)

#2.3
best_students0 = np.nanargmax(clean, axis=0)
clean_filled = np.where(np.isnan(clean), -np.inf, clean)
best_students1 = np.argmax(clean_filled, axis=0) #2 способ

#3.1
z = (clean-average_subject_score) / std_subject
print(np.shape(z))
print(np.allclose(np.nanmean(z, axis=0), 0))
print(np.allclose(np.nanstd(z, axis=0, ddof=1), 1))

#3.2
try:
    student_mean = np.nanmean(clean, axis=1)
    print(clean - student_mean)
except ValueError as v:
    print(v)
student_mean_kd = np.nanmean(clean, axis=1, keepdims=True)
cntrl_students = clean-student_mean_kd
print(np.allclose(np.nanmean(clean-student_mean_kd, axis=1), 0))

#3.3
w_masked = ~invalid * w
w_normalized = w_masked / w_masked.sum(axis=1, keepdims=True)
wght_average_scores = np.nansum(clean * w_normalized, axis=1)
print(wght_average_scores)

#3.4
D = np.abs(wght_average_scores[:, np.newaxis] - wght_average_scores[np.newaxis, :])
np.fill_diagonal(D, np.nan)
print(D)
smlr_students_idx = np.unravel_index(np.nanargmin(D), D.shape)
print(*smlr_students_idx) #нет, память не коировалась, оси повторяются через 0-ой stride

#4.1
passed = (clean >= 50).astype(float)
passed[np.isnan(raw) | (raw == -1)] = np.nan
print(passed)
prptn_passed = np.nanmean(passed, axis=0)
print(prptn_passed)

#4.2
valid = ~np.isnan(passed)
indices = np.where(np.logical_and(np.all((passed == 1) | ~valid, axis=1), (np.sum(valid, axis=1) >= 4)))[0]

print(indices)

#4.3
mask = np.any((clean < 45) | ~valid, axis=1)
risk_idx = np.where(mask)[0]
print(risk_idx)
print(mask)

#4.4
print(clean == np.nan)
print(np.isnan(clean))# т.к по IEEEкакието цифры nan != nan

#ОТВЕТЫ на вопросы
#1 потому что первое выражение дает вычитания (8, ), broadcasting проихсодит по последней оси, а 8 != 5, а второе выражение дает (,8) а 8 = 8

#2 Оси просто повторяются по 0-вой strides, не занимая память, он обращается к 1 и тем же элементам, просто выстраивает в другом порядке

#3 Они выполнят для целых побитовые операции. Нужно использовать np.logical_and/not/or

#4 Например указание неверное оси в sum


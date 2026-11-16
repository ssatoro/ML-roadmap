import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "дата": [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
        "2026-01-04",
        "2026-01-05",
        "2026-01-06",
        "2026-01-07",
        "2026-01-08"
    ],
    "продажи": [100, 120, 90, 150, 180, 160, 200, 240]
})

df_copy = df.copy()

result = df.copy()
result = result.set_index("дата")
result.index = pd.to_datetime(result.index)
result = result.sort_index()


result["предыдущий_день"] = result["продажи"].shift(1)
result["изменение_%"] = result["продажи"].pct_change(1)*100
result["среднее_за_3_дня"] = result["продажи"].rolling(3).mean()
result["отклонение"] = result["продажи"] - result["среднее_за_3_дня"]

print(result)
result["продажи"].plot()
plt.show()
import pandas as pd
import numpy as np

df_raw = pd.DataFrame({
    " ID заказа ": [
        "O-001", "O-002", "O-003", "O-004",
        "O-005", "O-006", "O-007", "O-008",
        "O-009", "O-010", "O-011", "O-012",
        "O-013", "O-006", "O-014", "O-015",
        "O-016", "O-017"
    ],
    " Клиент ": [
        " Иван Петров ", "Анна Смирнова", "Пётр Волков",
        "Мария Орлова", "Иван Петров", "Елена Ким",
        "Сергей Ли", "Анна Смирнова", "Денис Фролов",
        "Ольга Миронова", "Пётр Волков", "Мария Орлова",
        "Иван Петров", "Елена Ким", "Виктория Смирнова",
        "Алексей Морозов", "Наталья Крылова", "Денис Фролов"
    ],
    " Город ": [
        " Москва ", "Казань", "Москва", "Сочи",
        None, "Казань", "Москва", "Казань",
        "Сочи", "Москва", "Москва", "Сочи",
        "Москва", "Казань", "Тула", "Тула",
        "Сочи", "Сочи"
    ],
    " Email ": [
        " IVAN@MAIL.RU ", "anna@gmail.com", "p.volkov@mail.ru",
        "m.orlova@yandex.ru", "ivan@mail.ru", "ELENA@GMAIL.COM ",
        "sergey@mail.ru", "anna@gmail.com", "denis@mail.ru",
        "olga@mail.ru", "p.volkov@mail.ru", "m.orlova@yandex.ru",
        "ivan@mail.ru", "ELENA@GMAIL.COM ", "victoria@mail.ru",
        "alex@gmail.com", None, "denis@mail.ru"
    ],
    " Категория ": [
        "Электроника", "Аксессуары", "Электроника", "Дом",
        "Электроника", "Электроника", "Дом", "Аксессуары",
        "Электроника", "Дом", " Электроника ", "Дом",
        "Электроника", "Электроника", "Дом", "Электроника",
        "Дом", "Электроника"
    ],
    " Товар ": [
        "Мышь", "Коврик", "Клавиатура", "Лампа",
        "Монитор", "Наушники", "Стул", "Коврик",
        "Мышь", "Лампа", "Клавиатура", "Стул",
        "Монитор", "Наушники", "Чайник", "Мышь",
        "Лампа", "Мышь"
    ],
    " Количество ": [
        "2", "3", "1", "2", "1", "2", "—", "2",
        "1", "1", "1", "2", "1", "1", "2", "4",
        "1", "1"
    ],
    " Цена ": [
        "1 200", "450", "2 500", "900", "18 000",
        "3 200", "4 500", "450", "1 200", "900",
        "2 500", "4 500", "18 000", "3 200",
        "н/д", "1 200", "900", "1 200"
    ],
    " Дата заказа ": [
        "01.11.2025", "02.11.2025", "03.11.2025",
        "04.11.2025", "05.11.2025", "ошибка",
        "06.11.2025", "07.11.2025", "08.11.2025",
        "09.11.2025", "10.11.2025", "11.11.2025",
        "12.11.2025", "13.11.2025", "14.11.2025",
        "15.11.2025", "16.11.2025", "ошибка"
    ],
    " Статус ": [
        "Оплачен", "оплачен ", "В обработке", "Оплачен",
        "Оплачен", "Оплачен", "—", "Отменён",
        "Оплачен", "Оплачен", "оплачен", "Оплачен",
        "Оплачен", "Оплачен", "Оплачен", "PAID",
        "оплачен", "Оплачен"
    ]
})

def check_info(df):
    print(df)
    print(df.shape)
    print(df.dtypes)
    print(df.isna().sum(axis=0))
    print(df["id заказа"].duplicated(keep=False).sum())
    print((~df["id заказа"].duplicated(keep=False)).sum())

df_copy = df_raw.copy()

strp_lwr_clmns = ["email", "категория", "товар", "статус"]

df_copy.columns = df_copy.columns.str.strip().str.lower()
df_copy = df_copy.drop_duplicates(subset=["id заказа"], keep="last")
df_copy["клиент"] = df_copy["клиент"].str.strip().str.title()
df_copy["город"] = df_copy["город"].str.strip().str.capitalize()
df_copy[strp_lwr_clmns] = df_copy[strp_lwr_clmns].apply(lambda col: col.str.strip().str.lower())
df_copy[["количество", "цена"]] = df_copy[["количество", "цена"]].apply(lambda col: pd.to_numeric(col.str.replace(" ", ""), errors="coerce"))
df_copy["дата заказа"] = pd.to_datetime(df_copy["дата заказа"], errors="coerce", format="%d.%m.%Y")
df_copy["статус"] = df_copy["статус"].replace({"—" : pd.NA, "paid": "оплачен"})


df_copy.insert(8, "сумма заказа", df_copy["количество"] * df_copy["цена"])
df_copy.insert(9, "выручка", np.where(df_copy["статус"] == "оплачен", df_copy["сумма заказа"], np.nan))
total_revenue = df_copy["выручка"].sum()
print(df_copy)
print("-----------------")

df_anltc = df_copy.groupby("город", as_index=False, dropna=False).agg(
    выручка=("выручка", "sum"),
    колво_заказов=("статус", lambda x: x.eq("оплачен").sum()),
    колво_заказов_изв_сумм=("выручка", "count"),
    средняя_выручка=("выручка", "mean"))

df_category_anltc = df_copy.groupby("категория", as_index=False).agg(
    выручка=("выручка", "sum"),
    колво_опл_заказов=("статус", lambda x: x.eq("оплачен").sum()),
    колво_заказов_изв_сумм=("выручка", "count"),
    средняя_выручка=("выручка", "mean"),
    общее_колво_товаров=("количество", lambda x: x[df_copy.loc[x.index, "статус"].eq("оплачен")].sum())
)

df_elegible = df_copy.loc[df_copy["выручка"].notna()]
df_big_orders = df_elegible.groupby("город", dropna=False, group_keys=False).apply(
    lambda x: x.nlargest(2, "выручка").assign(город=x.name))[["id заказа", "город", "клиент", "категория", "выручка"]]


mask = (df_copy["статус"].eq("оплачен").fillna(False) & df_copy["выручка"].notna())
df_orders = df_copy.loc[mask, ["id заказа", "город", "выручка"]].copy()
df_orders["ср. выручка по городу"] = df_copy.groupby("город", dropna=False, group_keys=False)["выручка"].transform("mean")
df_orders["отклонение"] = df_orders["выручка"] - df_orders["ср. выручка по городу"]


df_clients = df_copy.groupby("клиент", as_index=False).agg(
    общая_выручка=("выручка", "sum"),
    колво_опл_заказов=("статус", lambda x: x.eq("оплачен").sum()),
    колво_опл_заказов_изв_сумм=("выручка", "count"),
    ср_изв_выручка=("выручка", "mean"),
    уник_категории=("категория", lambda x: x[df_copy.loc[x.index, "статус"].eq("оплачен").fillna(False)].nunique())
)



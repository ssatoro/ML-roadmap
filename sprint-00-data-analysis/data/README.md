# Dataset

## Titanic Dataset

The dataset contains information about Titanic passengers, including passenger class, age, sex, fare, and survival status.

## Source

The dataset is available through the Seaborn example datasets repository.

Source: https://github.com/mwaskom/seaborn-data

## How to Load

The dataset can be loaded directly in a Jupyter Notebook:

```python
import seaborn as sns

df = sns.load_dataset("titanic")
```

This requires an internet connection the first time the dataset is downloaded.

## Storage

The CSV file is not committed to this repository. It can be downloaded automatically by Seaborn when needed.
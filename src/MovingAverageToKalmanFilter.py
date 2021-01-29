# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% [markdown]
# [(単純)移動平均の定義](https://ja.wikipedia.org/wiki/移動平均)
# 移動平均自体は、numpy.convolveを使用して簡単に計算できる。
# 
# [畳み込み積分や移動平均を求めるnumpy.convolve関数の使い方](https://deepage.net/features/numpy-convolve.html)
# 
# %% [markdown]
# 以降で移動平均(Moving Average)を修正してカルマンフィルタの考え方を見るために、移動平均を以下のように計算する。
# 
# ```python
# MA[i] = MA[i-1] + x[i]/N - x[i-N]/N
# ```
# %% [markdown]
# 現時点から離れた時点のデータが入っているのは不自然なので、`x[i-N]`を`MA[i-1]`に置き換える(_modはmodifiedのつもり)。
# 
# ```python
# MA_mod[i] = (1-1/N)*MA_mod[i-1] + x[i]/N 
# ```

# %%




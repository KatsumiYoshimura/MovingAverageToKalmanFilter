# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% [markdown]
#   [(単純)移動平均の定義](https://ja.wikipedia.org/wiki/移動平均)
# 
#   移動平均自体は、numpy.convolveを使用して簡単に計算できる。
# 
#   [畳み込み積分や移動平均を求めるnumpy.convolve関数の使い方](https://deepage.net/features/numpy-convolve.html)
# 

# %%
# 時系列データ
x = np.zeros(100)
for i in range(1,len(x)):
    x[i] = x[i-1] + np.random.normal(loc=0.0,scale=1.0)

# N期間の移動平均を求める
N = 10

# %% [markdown]
#   以降で移動平均(Moving Average)を修正してカルマンフィルタの考え方を見るために、移動平均を以下のように計算する。
# 
#   ```python
#   MA[i] = MA[i-1] + x[i]/N - x[i-N]/N
#   ```

# %%
# 移動平均を入れる箱を準備
MA = np.zeros(len(x))
for i in range(0,len(x)):
    if i <= N-1:
        # N期間分のデータがない、またはN期前のデータがないので、ここまでの平均を移動平均とする
        MA[i] = np.average(x[0:i+1]) # "i+1"に注意
    else:
        # 直前の移動平均に新しいデータを加え、一番古いデータを除く
        MA[i] = MA[i-1] + x[i]/N - x[i-N]/N

# %% [markdown]
#   現時点から離れた時点のデータが入っているのは不自然なので、`x[i-N]`を`MA[i-1]`に置き換える(_modはmodifiedのつもり)。
# 
#   ```python
#   MA_mod[i] = (1-1/N)*MA_mod[i-1] + 1/N*x[i]
#   ```

# %%
# 修正された移動平均を入れる箱を準備
MA_mod = np.zeros(len(x))
for i in range(0,len(x)):
    if i <= N-1:
        # N期間分のデータがない、またはN期前のデータがないので、ここまでの平均を移動平均とする
        MA_mod[i] = np.average(x[0:i+1]) # "i+1"に注意
    else:
        # 直前の移動平均と新しいデータの重み付き平均
        MA_mod[i] = (1-1/N)*MA_mod[i-1] + 1/N*x[i]


# %%
plt.plot( x , label="Original data" )
plt.plot( MA , label="Simple Moving Average" )
plt.plot( MA_mod , label="Modified Moving Average" )
plt.legend()
plt.show()


# %%




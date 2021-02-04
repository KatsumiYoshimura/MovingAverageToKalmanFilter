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
## ランダムウォーク
## x = np.zeros(100)
## for i in range(1,len(x)):
##     x[i] = x[i-1] + np.random.normal(loc=0.0,scale=1.0)

pd_data = pd.read_csv('sample_data.csv',header=None)
x  = np.array(pd_data[0])


# N期間の移動平均を求める
N = 10

# %% [markdown]
#   以降で移動平均(Moving Average)を修正してカルマンフィルタの考え方を見るために、移動平均を以下のように計算する。
# 
#   ```python
#   MA[i] = MA[i-1] + x[i]/N - x[i-N]/N
#   ```

# %%
def GetSimpleMovingAverage( _x_ , _N_ ):
    _MA_ = np.zeros(len(_x_))
    for i in range(0,len(_x_)):
        if i <= _N_-1:
            # _N_期間分のデータがない、または_N_期前のデータがないので、ここまでの平均を移動平均とする
            _MA_[i] = np.average(_x_[0:i+1]) # "i+1"に注意
        else:
            # 直前の移動平均に新しいデータを加え、一番古いデータを除く
            _MA_[i] = _MA_[i-1] + _x_[i]/_N_ - _x_[i-_N_]/_N_
    
    return _MA_

# %% [markdown]
#   現時点から離れた時点のデータが入っているのは不自然なので、`x[i-N]`を`MA[i-1]`に置き換える(_modはmodifiedのつもり)。
# 
#   ```python
#   MA_mod[i] = (1-1/N)*MA_mod[i-1] + 1/N*x[i]
#   ```

# %%
def GetModifiedMovingAverage( _x_ , _N_ ):
    _MA_mod_ = np.zeros(len(_x_))
    for i in range(0,len(_x_)):
        if i <= _N_-1:
            # _N_期間分のデータがない、または_N_期前のデータがないので、ここまでの平均を移動平均とする
            _MA_mod_[i] = np.average(_x_[0:i+1]) # "i+1"に注意
        else:
            # 直前の移動平均と新しいデータの重み付き平均
            _MA_mod_[i] = (1-1/_N_)*_MA_mod_[i-1] + 1/_N_*_x_[i]

    return _MA_mod_

# %%
MA = GetSimpleMovingAverage( x , N )
MA_mod = GetModifiedMovingAverage( x , N )
plt.plot( x , label="Original data" )
plt.plot( MA , label="Simple Moving Average" )
plt.plot( MA_mod , label="Modified Moving Average" )
plt.legend()
plt.show()


# %%
def KalmanFilter( _x_ , _K_ ):
    _KF_ = np.zeros(len(_x_))
    _KF_[0] = _x_[0]
    for i in range(1,len(_x_)):
        _KF_[i] = (1-_K_)*_KF_[i-1] + _K_*_x_[i]

    return _KF_


# %%
KF = KalmanFilter( x , 1./N) 


# %%
fig, (ax1, ax2) = plt.subplots(2,1)

ax1.plot( MA_mod , label="Modified Moving Average")
ax1.legend()
ax2.plot( KF , label="Kalman Filter")
ax2.legend()

plt.show()



# %%
KF13W = KalmanFilter( x , 0.03) 
KF26W = KalmanFilter( x , 0.015) 
KF52W = KalmanFilter( x , 0.007) 

plt.plot( x , label="Original data" )
plt.plot( KF13W , label="13W KF" )
plt.plot( KF26W , label="26W KF" )
plt.plot( KF52W , label="52W KF" )

plt.legend()
plt.show()



import numpy as np

def funOU(n_steps, theta=0.4, sigma=1.0, p_hold=0.8):
    """
    Generate a sequence using the Ornstein–Uhlenbeck process.
    
    Parameters:
    n_steps (int): Number of steps in the sequence.
    theta (float): Mean reversion strength.
    sigma (float): Noise strength.
    p_hold (float): Probability to hold the same value.
    
    Returns:
    np.ndarray: Generated sequence.
    """
    x = np.zeros(n_steps)
    x[0] = 0

    for t in range(1, n_steps):
        if np.random.rand() < p_hold:
            x[t] = x[t-1]  # hold the same value
        else:
            x[t] = x[t-1] - theta * x[t-1] + sigma * np.random.randn()

    # Plot
    # plt.plot(x, marker='o')
    # plt.xlabel('Step')
    # plt.ylabel('Value')
    # plt.grid()
    # plt.show()

    return x

def fun(x, nodes=False):
    """
    Defines the occupancy of a room as a periodic, piecewise linear function of time of day.

    Parameters
    ----------
    x : array_like or scalar
        Time(s) of day (in hours) at which to evaluate occupancy.
    nodes : bool, optional
        If True, returns both occupancy values and node times. If False (default), returns
        only occupancy values at `x`.

    Returns
    -------
    y : ndarray
        Interpolated occupancy values at `x` (or at node times if `nodes=True`).
    x_nodes : ndarray, optional
        Node times (only if `nodes=True`).
    """
    s = np.array([0, 7.5, 8, 12, 12.5, 13.5, 14, 18, 19, 24])
    v = np.array([0, 0, 15, 15, 7, 4, 15, 15, 0, 0])
    v[0] = v[-1]  # Ensure periodicity
    period = 24

    if nodes:
        x_eval = s
    else:
        x_eval = np.asarray(x, dtype=float)

    # Map x into [0, 24)
    x_mod = np.mod(x_eval, period)

    # Perform linear interpolation with periodic nodes
    y = np.interp(x_mod, s, v)

    if nodes:
        return y, s
    else:
        return y

def occupancy(n_days):
    """
    Wrapper for the occupancy function that combines a piecewise linear function with an Ornstein-Uhlenbeck process.

    Parameters
    ----------
    x : array_like or scalar
        Time(s) of day (in hours) at which to evaluate occupancy.

    Returns
    -------
    y : ndarray
        Interpolated occupancy values at `x` (or at node times if `nodes=True`).

    """
    x = np.linspace(0, 24*n_days, 288*n_days)  # 5-minute intervals
    # Get piecewise function values
    y_fun = fun(x)
    # get Ornstein-Uhlenbeck process values
    y_OU  = funOU(n_steps=len(x), theta=0.4, sigma=1.0, p_hold=0.8)

    # Combine  functions 
    y = np.round(y_fun + y_OU)
    y[ y < 0] = 0  # Ensure no negative values
    y[-1] = 0
    
    x_mod = np.mod(x, 24) # Map x into [0, 24)
    for i in range(len(y)):
        if x_mod[i] >= 19:  # 19h 
            y[i] = min(y[i], y[i-1])  # Ensure no increase after 19h
    
    for i in range(len(y)-2, 0, -1):
        if x_mod[i] <= 7.5:  # 7h 
            y[i] = min(y[i], y[i+1])  # Ensure no increase before 7h

    y[ (x_mod < 5) | (x_mod > 23) ] = 0  # Ensure no occupancy before 5h and after 23h    

    return x, y

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    t, y = occupancy(n_days=365)  # Get occupancy values for n_days
    
    t_mod = np.mod(t, 24)
    y_expected = fun(t_mod)
    plt.plot(t, y_expected, color='red', linewidth=1, label='Expected Occupancy')
    plt.bar(t, y, width=0.5, label='Occupancy', color='blue', align='center')
    # Set x-ticks to show time of day (e.g., 0, 6, 12, 18, 24, ...)
    xticks = np.arange(0, t[-1]+1, 6)
    plt.xticks(xticks, [f"{int(x%24):02d}" for x in xticks])
    plt.xlabel('Hour of Day')
    plt.ylabel('Occupancy')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Gerar CSV com ocupação (número de pessoas inteiras) no padrão EnergyPlus
import pandas as pd

dias = 365  # mesmo valor de n_days usado acima
t, y = occupancy(n_days=dias)
y = np.round(y).astype(int)  # garantir número inteiro de pessoas

# Gerar datas e horários
date_range = pd.date_range(start="2025-01-01", periods=288*dias, freq='5min')
df = pd.DataFrame({
    'Date': date_range.strftime('%m/%d'),
    'Time': date_range.strftime('%H:%M:%S'),
    'Occupancy': y
})

df.to_csv("ocupacao.csv", index=False)

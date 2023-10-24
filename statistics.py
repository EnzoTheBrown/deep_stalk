def compute_means(df, windows=3000):
    df['mean_30'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(windows, 1).mean())
    df['std_30'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(windows, 1).std())
    df['pos_30'] = df['mean_30'] + df['std_30']
    df['neg_30'] = df['mean_30'] - df['std_30']
    df['2_pos_30'] = df['mean_30'] + 2*df['std_30']
    df['2_neg_30'] = df['mean_30'] - 2*df['std_30']

    return df

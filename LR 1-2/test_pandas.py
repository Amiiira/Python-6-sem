def test_pandas_mean_vals():
    import pandas as pd

    data = pd.read_csv('MarketingSpend.csv')

    print(data.loc[:1, 'Offline Spend'], data.loc[:1, 'Online Spend'])
    print(data.loc[:, 'Offline Spend'].mean() )
    print(data.loc[:, 'Online Spend'].mean() )    

test_pandas_mean_vals()

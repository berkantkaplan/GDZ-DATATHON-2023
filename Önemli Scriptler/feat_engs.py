def create_datetimes(df, label=None):
    df['date'] = df.Tarih
    df['hour'] = df['date'].dt.hour
    df['dayofweek'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['dayofmonth'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.weekofyear
    
    X = df[['hour','dayofweek','quarter','month','year',
           'dayofyear','dayofmonth','weekofyear']]
    # if label:
    #     y = df[label]
    #     return X, y
    # return X

def create_holiday_weekend(df):
    import holidays
    turkey_holidays = holidays.Turkey()

    def is_holiday(date): 
        return date in turkey_holidays

    df['holiday'] = df['Tarih'].dt.date.apply(is_holiday).astype(int)

    df['weekend'] = df['dayofweek'].apply(lambda x: 1 if x in (5, 6) else 0)
    
def create_electricOutage_timeofDay(df,med):
 
    outage_dates = set(med['Tarih'].dt.date)
    df['date'] = df['Tarih'].dt.date
    df['electrical_outage'] = df['date'].apply(lambda x: 1 if x in outage_dates else 0)
    
    
    conditions = [
    (6 <= df['hour']) & (df['hour'] < 12),
    (12 <= df['hour']) & (df['hour'] < 18),
    (18 <= df['hour']) & (df['hour'] < 24)
    ]
    choices = [1, 2, 3]

    df['timeofday'] = np.select(conditions, choices, default=3)
    df['timeofday'] = df['timeofday'].astype('int')
    
def create_businessDay_cumulativeholidays(df):
    df['business_day'] = df['dayofweek'].apply(lambda x: 1 if x in range(0, 5) else 0)
    df['cumulative_holidays'] = df['holiday'].cumsum()
    

def create_outage_rolling_percentages(df):
    df['outage_percentage'] = (df['electrical_outage'].cumsum() / (df.index + 1)) * 100

    window_size = 24
    df['rolling_outages_24h'] = df['electrical_outage'].rolling(window=window_size).sum()
    
    
    alpha = 0.1
    df['exp_avg_outages_24h'] = df['electrical_outage'].ewm(alpha=alpha).mean()
    df
    

def create_hourly_sin_cos(df):
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    
    
def create_seasons(df):
    def is_spring(ds):
        date = pd.to_datetime(ds)
        if (date.month >= 3) & (date.month <= 5):
            return 1
        else :
            return 0

    def is_summer(ds):
        date = pd.to_datetime(ds)
        if (date.month >= 6) & (date.month <= 8):
            return 1
        else :
            return 0

    def is_autumn(ds):
        date = pd.to_datetime(ds)
        if (date.month >= 9) & (date.month <= 11):
            return 1
        else :
            return 0

    def is_winter(ds):
        date = pd.to_datetime(ds)
        if (date.month >= 12) & (date.month <= 2):
            return 1
        else :
            return 0

    def is_weekend(ds):
        date = pd.to_datetime(ds)
        if date.day_name in ('Saturday', 'Sunday'):
            return 1
        else :
            return 0

    # adding to train set
    df['is_spring'] = df['Tarih'].apply(is_spring)
    df['is_summer'] = df['Tarih'].apply(is_summer)
    df['is_autumn'] = df['Tarih'].apply(is_autumn)
    df['is_winter'] = df['Tarih'].apply(is_winter)
    df['is_weekend'] = df['Tarih'].apply(is_weekend)
    df['is_weekday'] = ~df['Tarih'].apply(is_weekend)

    # adding to test set
    df['is_spring'] = df['Tarih'].apply(is_spring)
    df['is_summer'] = df['Tarih'].apply(is_summer)
    df['is_autumn'] = df['Tarih'].apply(is_autumn)
    df['is_winter'] = df['Tarih'].apply(is_winter)
    df['is_weekend'] = df['Tarih'].apply(is_weekend)
    df['is_weekday'] = ~df['Tarih'].apply(is_weekend)
    


# def create_isramadan(df):
#     hols = pd.read_csv('Calendar.csv', parse_dates=['CALENDAR_DATE'])
#     hols = hols[['CALENDAR_DATE','RAMADAN_FLAG','PUBLIC_HOLIDAY_FLAG']]
#     df['isRamadan'] = np.where((hol['RAMADAN_FLAG'] == 'Y') | (hol['PUBLIC_HOLIDAY_FLAG'] == 'Y'), 'TR-Holidays', 0)

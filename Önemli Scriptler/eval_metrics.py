import pandas as pd
import matplotlib.pyplot as plt

def eval_metrics(y_true , y_pred):
    from sklearn.metrics import r2_score , mean_absolute_error , mean_squared_error , mean_absolute_percentage_error
    
    # MAPE hesaplama
    mape = mean_absolute_percentage_error(y_true, y_pred)
    
    # r2 hesaplama
    r2 = r2_score(y_true , y_pred)
    
    # mae hesaplama
    mae = mean_absolute_error(y_true , y_pred)

    # rmse hesaplama
    mse = mean_squared_error(y_true,y_pred)**0.5
    
    print(f"""
          Mape Score : {mape}
          R2 Score : {r2}
          MAE Score : {mae}
          MSE Score : {mse}
          """)
    
def eval_plot(y_true , y_pred):
    tests = pd.DataFrame(data = y_true , columns=['Real Values'] , index = X_test[:-24].index)
    preds = pd.DataFrame(data = y_pred , columns=['Predicts'] , index = future_data[:-24].index)
    compare = pd.concat([tests[:-24], preds] , axis= 1)
    print(compare.plot())
    
def eval_df (y_true , y_pred):
    compare = pd.DataFrame({'Real Values': y_true, 'Predicts': y_pred}, index=future_data[:-24].index)
    print(compare)
    
def create_submission(future_preds, num):
    submission_df = pd.DataFrame({'Tarih': future_data.index, 'Dağıtılan Enerji (MWh)': future_preds})
    filename = 'submission{}.csv'.format(num)
    submission_df.to_csv(filename, index=False)
    globals()['submission{}'.format(num)] = submission_df
    
def preds_plot(data , future_data , target_data):
    # Gerçek değerleri mavi renkte çizdir
    plt.plot(data, color='blue', label='Gerçek Değerler')

    # Tahmin edilen değerleri yeşil renkte çizdir
    plt.plot(future_data, color='green', label='Tahminler')
    
    # Hedef ayın değerleri kırmızı renkte çizdir
    plt.plot(target_data, color='red', label='Gerçek Değerler')

    # Eksenleri ve grafik başlığını belirle
    plt.title('Gerçek Değerler ve Tahminler')
    plt.xlabel('Saat')
    plt.ylabel('Değer')
    plt.legend()

    # Grafikleri göster
    plt.show()
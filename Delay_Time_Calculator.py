import csv
import numpy as np
print("With One Arduino")
print(" ")
time_data = []

with open('data_log_1_arduino.csv', mode='r', newline='') as file :
    reader = csv.reader(file)

    for line in reader :
        try :
            time_data.append(float(line[0]))
        except :
            pass

delay = []

for i in range(len(time_data)) :
    try :
        delay.append(time_data[i+1] - time_data[i])
    except :
        pass

avg_delay_time = np.mean(delay)
print(f'Time[s] : {avg_delay_time if avg_delay_time else 0}')
print(f'Frequency : {1/avg_delay_time if avg_delay_time else 0}')
print(f'Std : {np.std(delay)}')

delay_10 = []
delay_20 = []
delay_30 = []
delay_40 = []
delay_50 = []
delay_60 = []

for i in range(len(time_data)) :
    if time_data[i] <= 10 :
        try :
            delay_10.append(time_data[i+1] - time_data[i])
        except :
            pass
    elif time_data[i] <= 20 :
        try :
            delay_20.append(time_data[i+1] - time_data[i])
        except :
            pass
    elif time_data[i] <= 30 :
        try :
            delay_30.append(time_data[i+1] - time_data[i])
        except :
            pass
    elif time_data[i] <= 40 :
        try :
            delay_40.append(time_data[i+1] - time_data[i])
        except :
            pass
    elif time_data[i] <= 50 :
        try :
            delay_50.append(time_data[i+1] - time_data[i])
        except :
            pass
    else :
        try :
            delay_60.append(time_data[i+1] - time_data[i])
        except :
            pass

avg_delay_time_10 = np.mean(delay_10)
avg_delay_time_20 = np.mean(delay_20)
avg_delay_time_30 = np.mean(delay_30)
avg_delay_time_40 = np.mean(delay_40)
avg_delay_time_50 = np.mean(delay_50)
avg_delay_time_60 = np.mean(delay_60)
print(f'Delay under 10s : {avg_delay_time_10 if avg_delay_time_10 else 0} / {1/avg_delay_time_10 if avg_delay_time_10 else 0}')
print(f'Delay under 20s : {avg_delay_time_20 if avg_delay_time_20 else 0} / {1/avg_delay_time_20 if avg_delay_time_20 else 0}')
print(f'Delay under 30s : {avg_delay_time_30 if avg_delay_time_30 else 0} / {1/avg_delay_time_30 if avg_delay_time_30 else 0}')
print(f'Delay under 40s : {avg_delay_time_40 if avg_delay_time_40 else 0} / {1/avg_delay_time_40 if avg_delay_time_40 else 0}')
print(f'Delay under 50s : {avg_delay_time_50 if avg_delay_time_50 else 0} / {1/avg_delay_time_50 if avg_delay_time_50 else 0}')
print(f'Delay under 60s : {avg_delay_time_60 if avg_delay_time_60 else 0} / {1/avg_delay_time_60 if avg_delay_time_60 else 0}')
print("-----")
# -----------------
print("With Two Arduino")
print(" ")
time_data = []

with open('data_log_2_arduino.csv', mode='r', newline='') as file :
    reader = csv.reader(file)

    for line in reader :
        try :
            time_data.append(float(line[0]))
        except :
            pass

delay = []

for i in range(len(time_data)) :
    try :
        delay.append(time_data[i+1] - time_data[i])
    except :
        pass

avg_delay_time = np.mean(delay)
print(f'Time[s] : {avg_delay_time if avg_delay_time else 0}')
print(f'Frequency : {1/avg_delay_time if avg_delay_time else 0}')
print(f'Std : {np.std(delay)}')

delay_10 = []
delay_20 = []
delay_30 = []
delay_40 = []
delay_50 = []
delay_60 = []

for i in range(len(time_data)) :
    if time_data[i] <= 10 :
        try :
            delay_10.append(time_data[i+1] - time_data[i])
        except :
            pass
    elif time_data[i] <= 20 :
        try :
            delay_20.append(time_data[i+1] - time_data[i])
        except :
            pass
    elif time_data[i] <= 30 :
        try :
            delay_30.append(time_data[i+1] - time_data[i])
        except :
            pass
    elif time_data[i] <= 40 :
        try :
            delay_40.append(time_data[i+1] - time_data[i])
        except :
            pass
    elif time_data[i] <= 50 :
        try :
            delay_50.append(time_data[i+1] - time_data[i])
        except :
            pass
    else :
        try :
            delay_60.append(time_data[i+1] - time_data[i])
        except :
            pass

avg_delay_time_10 = np.mean(delay_10)
avg_delay_time_20 = np.mean(delay_20)
avg_delay_time_30 = np.mean(delay_30)
avg_delay_time_40 = np.mean(delay_40)
avg_delay_time_50 = np.mean(delay_50)
avg_delay_time_60 = np.mean(delay_60)
print(f'Delay under 10s : {avg_delay_time_10 if avg_delay_time_10 else 0} / {1/avg_delay_time_10 if avg_delay_time_10 else 0}')
print(f'Delay under 20s : {avg_delay_time_20 if avg_delay_time_20 else 0} / {1/avg_delay_time_20 if avg_delay_time_20 else 0}')
print(f'Delay under 30s : {avg_delay_time_30 if avg_delay_time_30 else 0} / {1/avg_delay_time_30 if avg_delay_time_30 else 0}')
print(f'Delay under 40s : {avg_delay_time_40 if avg_delay_time_40 else 0} / {1/avg_delay_time_40 if avg_delay_time_40 else 0}')
print(f'Delay under 50s : {avg_delay_time_50 if avg_delay_time_50 else 0} / {1/avg_delay_time_50 if avg_delay_time_50 else 0}')
print(f'Delay under 60s : {avg_delay_time_60 if avg_delay_time_60 else 0} / {1/avg_delay_time_60 if avg_delay_time_60 else 0}')
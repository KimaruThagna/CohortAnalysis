import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter 

df = pd.read_csv('data/duration.csv')
df['EventType'] = [1 if x == 'SYSTEM ERROR' else 0 for x in df['EventType']]
time_to_event = df['days_to_event']
event = df['EventType']

kmf = KaplanMeierFitter()
kmf.fit(time_to_event, event_observed=event)
kmf.plot(at_risk_counts=True)
plt.title('Kaplan-Meier Curve')
plt.show()


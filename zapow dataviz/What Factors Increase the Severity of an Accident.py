import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(r'C:\Users\TUF GAMING\OneDrive\Desktop\datasets\US_Accidents_March23.csv')

df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
df.dropna(subset=['Start_Time'], inplace=True)

road_features = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit', 
                 'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming', 
                 'Traffic_Signal', 'Turning_Loop']


severe_accidents = df[df['Severity'].isin([3, 4])]
minor_accidents = df[df['Severity'].isin([1, 2])]

severe_counts = severe_accidents[road_features].sum()
minor_counts = minor_accidents[road_features].sum()

severe_percent = (severe_counts / severe_counts.sum()) * 100
minor_percent = (minor_counts / minor_counts.sum()) * 100

comparison_df = pd.DataFrame({
    'Road Feature': road_features,
    'Severe Accidents (%)': severe_percent.values,
    'Minor Accidents (%)': minor_percent.values
}).set_index('Road Feature')

comparison_df = comparison_df.sort_values('Severe Accidents (%)', ascending=True)

plt.figure(figsize=(16, 10))

bar_width = 0.35
index = np.arange(len(comparison_df))
fig, ax = plt.subplots(figsize=(16, 10))


severe_color = '#8B0000'  # Dark Red 
minor_color = '#000066'   # Royal Blue 


bar1 = ax.barh(index - bar_width/2, comparison_df['Severe Accidents (%)'], 
               height=bar_width, color=severe_color, label='Severe Accidents (3-4)', 
               alpha=0.8)
bar2 = ax.barh(index + bar_width/2, comparison_df['Minor Accidents (%)'], 
               height=bar_width, color=minor_color, label='Minor Accidents (1-2)', 
               alpha=0.8)


for bar in bar1:
    width = bar.get_width()
    ax.text(width + 0.3, bar.get_y() + bar.get_height()/2,
            f'{width:.1f}%',
            ha='left', va='center', fontweight='bold')

for bar in bar2:
    width = bar.get_width()
    ax.text(width + 0.3, bar.get_y() + bar.get_height()/2,
            f'{width:.1f}%',
            ha='left', va='center', fontweight='bold')


ax.set_yticks(index)
ax.set_yticklabels(comparison_df.index)
ax.set_xlabel("Percentage of Accidents", fontsize=12, fontweight='bold')
ax.set_ylabel("Road Feature", fontsize=12, fontweight='bold')
ax.set_title("Comparison of Severe vs. Minor Accidents by Road Feature (%)", 
             fontsize=14, fontweight='bold')
ax.legend(title='Accident Severity', loc='lower right')
ax.set_xlim(0, max(comparison_df.max()) + 5) 
ax.grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

print("\nRoad Feature Severity Comparison:")
print(comparison_df)
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(r'C:\Users\TUF GAMING\OneDrive\Desktop\datasets\US_Accidents_March23.csv')
df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
df.dropna(subset=['Start_Time'], inplace=True)

start_date = df['Start_Time'].min().strftime('%Y-%m-%d')
end_date = df['Start_Time'].max().strftime('%Y-%m-%d')

print(f"✅ Data collected from {start_date} to {end_date}")
road_features = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit', 
                 'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming', 
                 'Traffic_Signal', 'Turning_Loop']


road_accidents = df[road_features].sum()

total_road_accidents = road_accidents.sum()

road_accidents_percentage = (road_accidents / total_road_accidents) * 100

road_accidents_df = pd.DataFrame({
    'Road Feature': road_accidents.index,
    'Accident Count': road_accidents.values,
    'Accident Percentage': road_accidents_percentage.values
})

road_accidents_df = road_accidents_df.sort_values(by='Accident Count', ascending=False)

# คำนวณค่าเฉลี่ย ค่ามากสุด ค่าน้อยสุด และค่ามัธยฐานของเปอร์เซ็นต์
stat_summary = {
    'Mean': road_accidents_df['Accident Percentage'].mean(),
    'Median': road_accidents_df['Accident Percentage'].median(),
    'Max': road_accidents_df['Accident Percentage'].max(),
    'Min': road_accidents_df['Accident Percentage'].min(),
    'Total Road Accidents': total_road_accidents
}

print("===== Statistical Breakdown =====")
for key, value in stat_summary.items():
    print(f"{key}: {value:.2f}")

print("\n===== Detailed Data =====")
print(road_accidents_df)

plt.figure(figsize=(12, 6))

bar_color = 'darkblue'

bar_width = 0.6
bar_spacing = bar_width / 2

bars = plt.barh(road_accidents_df['Road Feature'], 
                road_accidents_df['Accident Percentage'], 
                color=bar_color, 
                height=bar_width)

for bar in bars:
    plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, 
             f'{bar.get_width():.2f}%', va='center', fontsize=10)

plt.xlabel("Accident Percentage (%)", fontsize=12)
plt.ylabel("Road Feature", fontsize=12)
plt.title(f"Percentage of Accidents by Road Infrastructure Type ", fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()


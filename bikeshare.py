import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city_data = ['chicago', 'new york city', 'washington']
month_data = ['january', 'february','march', 'april', 'may' , 'june', 'all']
day_data = ['sunday','monday', 'tuesday', 'wednesday', 'thursday','friday', 'saturday','all']
data_choice = ['y','yes']

def get_filters():
    """
    Ask user specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Get user input for city (chicago, new york city, washington).
    print(' Hello! Let\'s explore some US bikeshare data!\n','Which city would you like to see the data for: Chicago, New York City, or Washington?\n')
    city = ''
    while city not in city_data:
        city = input('Enter your city: ').lower()
        if city in city_data:
            city = city.lower()
        else:
            print(" Sorry I cannot recognize it",'\n'
                  ,"your input should be one from: Chicago, New York City or Washington.\n")
        

    # Get user input for month (all, january, february, ... , june).
    print("\n Which month are you interested in?",'\n',"Please input your choice from ( January, February, March, April, May, June or All )\n")
    month=''
    while month not in month_data:
        month = input('Enter your Month: ').lower()
        if month in month_data:
            month = month.lower()
        else:
            print(" Sorry I cannot recognize it",'\n'
                  ,"your input should be one from: ","January, February, March, April, May,June or All\n")


    # Get user input for day of week (all, monday, tuesday, ... sunday).
    print("\n Which day of the week are you interested in?",'\n',"Please input your choice from ( Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All )\n")
    day = ''
    while day not in day_data:
        day = input('Enter your Day: ').lower()
        if day in day_data:
            day = day.lower()
        else:
            print(" Sorry I cannot recognize it",'\n'
                  ,"your input should be one from: ","Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All\n")


    print('='*100)
    print('Please confirm your choices to continue (Y/N): City {}, Month {}, Day {}\n'.format(city,month,day))
    
    choice = ''
    while choice not in data_choice:
        choice = input().lower()
            
        if choice in data_choice:
            print('='*100,'\n')
            return city,month,day
        else:
            print('\nStart again')
            print('='*100,'\n')
            get_filters()  
    
    print('='*100)


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # Load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime.
    df['Start Time']= pd.to_datetime(df['Start Time'])
    
    # Extract month and day of week from Start Time to create new columns.
    df['Month'] = df['Start Time'].dt.strftime('%B').str.lower()
    df['Day'] = df['Start Time'].dt.strftime('%A').str.lower()
    df['Hour'] = df['Start Time'].dt.strftime('%H')
    
    # Filter by month & day if applicable.
    if day != 'all':
        df = df[df['Day'] == day]
        
    if month != 'all':
        df = df[df['Month'] == month]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the statistics on the most frequest times of travel...\n')
    start_time = time.time()

    # Display the most common month.
    period_m = df.groupby('Month').size().idxmax()
    
    # Display the most common day of week.
    period_d = df.groupby('Day').size().idxmax()
    
    # Display the most common start hour.
    period_h = df.groupby('Hour').size().idxmax()
    
    print ('The most common month: "{}" , most common day of the week: "{}" and the most common start hour: "{}" hours'.format(period_m,period_d,period_h))
    print('-'*100)
    print("This took %s seconds." % (time.time() - start_time))
    print('='*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the statistics on the most popular stations and trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    s_station = df.groupby('Start Station').size().idxmax()

    # Display most commonly used end station.
    e_station = df.groupby('End Station').size().idxmax()

    # Display most frequent combination of start station and end station trip.
    c_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    
    print ('The most commonly used start station: {}.\nThe most commonly used end station: {}.\nThe most frequnt combination of stations: {}.'.format(s_station,e_station,c_station))
    print('-'*100)
    print("This took %s seconds." % (time.time() - start_time))
    print('='*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating statistics on the trip durations...\n')
    start_time = time.time()

    # Display total travel time.
    total = df.groupby('Trip Duration').size().sum()
    
    # Display Max travel time.
    maximum = df.groupby('Trip Duration').size().idxmax()

    # Display mean travel time.
    average = df.groupby('Trip Duration').size().mean()
    
    # Display min travel time.
    minmum = df.groupby('Trip Duration').size().idxmin()
    
    print ('The Total Travel Time: {}.\nThe Max Travel Time: {}.\nThe Average Travel Time: {}.\nThe Min Travel Time: {}.'.format(total,maximum,average,minmum))
    print('-'*100)
    print("This took %s seconds." % (time.time() - start_time))
    print('='*100)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating statistics on bikeshare users...\n')
    start_time = time.time()

    # Display counts of user types.
    print(df['User Type'].value_counts())
    print()
    # Display counts of gender.
    
    if 'Gender' in df:
        print(df['Gender'].value_counts())
        print()
    else:
        print ('Gender info not available\n')

    # Display earliest, most recent, and most common year of birth.
    if 'Birth Year' not in df:
        print('Birth year not available.')
    else: 
        birth = df.groupby('Birth Year', as_index=False).count()
        print('Most recent year of birth: {}.'.format(int(birth['Birth Year'].max())))
        print('Earliest year of birth: {}.'.format(int(birth['Birth Year'].min())))
        print('Most common year of birth: {}.'.format(int(birth.iloc[birth['Start Time'].idxmax()]['Birth Year'])))
         
    print('-'*100)
    print("This took %s seconds." % (time.time() - start_time))
    print('='*100)
     
# Request user input for raw data display.
def display_data(df):
    """Displays raw bikeshare data."""
    row_length = df.shape[0]
    for i in range(0, row_length, 5):
        
        yes = input('\nWould you like to display raw data Type \'yes\' or \'no\'\n> ')
        if yes.lower() != 'yes':
            break
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
  

        restart = input('\nWould you like to restart? Enter \'yes\' to confirm or any other entry to shutdown.\n')
        if restart.lower() != 'yes'and restart.lower() != 'Yes'and restart.lower() != 'y'and restart.lower() != 'Y':
            break

if __name__ == "__main__":
    main()
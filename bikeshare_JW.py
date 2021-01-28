import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv'}

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    cities = ['chicago', 'new york city', 'washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    print('Welcome! Let\'s explore some US bikeshare detail!')

    #ask for user to choose the city. Check against the city list defined above:
    while True:
        city = input('What city would you like to analyse? Chicago, New York City, Washington\n').lower()

        if city not in cities:
            print('Sorry, that is not a value choice. Please enter either: Chicago, New York City or Washington')
        else:
            print('You have selected {}'.format(city).title())

            break

    #ask for usre to select the month.  Check against the month list defined above.
    while True:

        month = input('Select a month to look at (January - June). For all months, type "all"\n').lower()

        if month not in months:
            print('Please enter a valid month. Type "all" to view all months\n')

        else:
            print('You have selected {}'.format(month).title())

            break

    #ask for user to choose day of the week. Check against the days list defined above.
    while True:

        day = input('Select a day to look at. For all days, type "all"\n').lower()

        if day not in days:
            print('Please enter a valid day.  Type "all" to view all days\n')
        else:
            print('You have selected {}'.format(day).title())

            break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):


    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':

        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]
    if day != 'all':

        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):

    print('\nCalculating the most frequent times of travel.....\n')
    start_time = time.time()

    #most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]

    print('The month with the most number of travellers is: {}'.format(most_common_month))

    #most common day of the week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    most_common_day = df['day_of_week'].mode()[0]

    print('The day with the most number of travellers is: {}'.format(most_common_day))

    #most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]

    print('The most popular start hour is: {}'.format(most_common_hour))

    print('\nThis took %s seconds.'%(time.time()-start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating the most popular stations and trip.....\n')

    start_time = time.time()

    #most commonly used start station
    df['Start Station'] = df['Start Station'].mode()[0]
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is: {}'.format(most_common_start_station))

    #most commonly used end station
    df['End Station'] = df['End Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]

    print('The most common end station is: {}'.format(most_common_end_station))

    #most frequent combination of start station and end station trip

    frequent_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)

    print('The most frequent combination from start to end is: \n {}'.format(frequent_combination))

    print('\nThis took %s seconds.'%(time.time()-start_time))
    print('-'*40)


def trip_duration_stats(df):
    print('\nCalculating trip duration.....\n')
    start_time = time.time()

    #display total travel time
    total_travel_time = df['Trip Duration'].sum()/60/60/24

    print('The total travel time is: {}'.format(total_travel_time))

    #display the mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60

    print('The mean travel time is: {}'.format(mean_travel_time))


    print('\nThis took %s seconds.'%(time.time()-start_time))
    print('-'*40)


def user_stats(df):
    print('\nCalculating user stats.....\n')

    start_time = time.time()

    #display count of user types
    user_types = df['User Type'].value_counts()
    print('The user base is split amongst the different types:\n{}\n'.format(user_types))

    #display gender count
    if "Gender" in df.columns:
        gender_count = df['Gender'].value_counts()
        print('The gender split of the users is:\n{}\n'.format(gender_count))

    else:
        print('Geneder statistics are unavailable')

    #display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        oldest_year = np.nanmin(df['Birth Year'])
        recent_year = np.nanmax(df['Birth Year'])
        common_year = df['Birth Year'].mode()[0]
        print('The oldest user was born in: {}'.format(oldest_year))
        print('The youngest user was born in: {}'.format(recent_year))
        print('The most common birth year is: {}'.format(common_year))

    else:
        print("Birth Year statistics are unavailable")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    i = 0

    while True:
        raw_data_rows = input('\nWould you like to see 5 rows of raw data? Enter yes or no. \n').lower()
        if raw_data_rows == 'yes':
            rows = df.iloc[:i+5]
            print(rows)
            i = i + 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() !='yes':
            break


if __name__ == "__main__":
    main()

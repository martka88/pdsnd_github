import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    cities = list()
    for i in CITY_DATA.keys():
        cities.append(i.title())
        cities.append(i)

    city = input('Enter the name of the city you would you like to look into: ').lower()
    while not (city in cities):
        city = input('There is no such a city in our data base. Please try again: ').lower()

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all', 'January', 'February', 'March', 'April', 'May', 'June',     'All']
    month = input('Enter the name of the month for which you would like to see the analysis. If you want to see it for all months, please       enter "all": ').lower()
    while not (month in months):
        month = input('There is no such a month. Please try again: ').lower()

    days = ['all', 'All', 'monday', 'Monday', 'tuesday', 'Tuesday', 'wednesday', 'Wednesday', 'thursday', 'Thursday', 'friday', 'Friday', 'saturday', 'Saturday', 'sunday', 'Sunday']
    day = input('Enter the name of the day of the week for which you would like to see the analysis. If you want to see it for all days, please enter "all": ').lower()
    while not (day in days):
        day = input('There is no such a day. Please try again: ').lower()

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most common month:', popular_month)

    df['weekday'] = df['Start Time'].dt.weekday
    popular_weekday = df['weekday'].mode()[0]
    print('Most common day of the week:', popular_weekday)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_st = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popular_start_st)

    # TO DO: display most commonly used end station
    popular_end_st = df['End Station'].mode()[0]
    print('Most commonly used end station:', popular_end_st)

    # TO DO: display most frequent combination of start station and end station trip
    df['Station combi'] = df[['Start Station', 'End Station']].agg('-'.join, axis=1)
    popular_combi = df['Station combi'].mode()[0]
    print('Most frequent combination of start station and end station trip:', popular_combi)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()

    hour = total_time//(60*60)
    m = (total_time-hour*60*60)//60
    s = total_time-(hour*60*60)-(m*60)

    print('Total travel time in seconds:', total_time)
    print('Total travel time in hours, minutes and seconds: {}h, {}m, {}s.'.format(hour, m, s))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    """convert time from seconds to hour and minutes"""
    hour2 = mean_time//(60*60)
    m2 = (mean_time-hour2*60*60)//60
    s2 = mean_time-(hour2*60*60)-(m2*60)

    print('Mean travel time in seconds:', mean_time)
    print('Mean travel time in hours, minutes and seconds: {}h, {}m, {}s.'.format(hour2, m2, s2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()[0]
    print('Counts of user types:', user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()[0]
        print('Counts of gender:', gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()
        print('Earliest year of birth:', earliest)
        print('Most recent year of birth:', most_recent)
        print('Most common year of birth:', most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays 5 first rows of raw data."""
    answer = input('\nWould you like to see the first 5 rows of raw data? Enter yes or no.\n')
    if answer.lower() == 'yes':
        x = 0
        y = 5
        print(df[df.columns[0:]].iloc[0:5])

    """Displays 5 rows more."""
    answer_2 = input('\nWould you like to see 5 rows more? Enter yes or no.\n')
    while answer_2.lower() == 'yes':
        x += 5
        y += 5
        print(df[df.columns[0:]].iloc[x:y])
        answer_2 = input('\nWould you like to see 5 rows more? Enter yes or no.\n')

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
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

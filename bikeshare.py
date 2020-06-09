import time
import pandas as pd
import numpy as np
import random

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

WEEKDAYS =['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! Exit with \"Strg + C\"')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    random_data = str(input('Would you like to see random data? Enter yes or no.\n')).lower()
    if random_data != 'yes':
        city = str(input('Which city do you want to look at? \n')).lower()
        while city not in CITY_DATA:
            city = str(input('City is not in the data. Select other city, or type \"list\" to get an overview \n')).lower()
            if city == 'list':
                print(pd.DataFrame( CITY_DATA.keys()))

        # get user input for month (all, january, february, ... , june)
        month = str(input('Which month do you want to look at? \(all, January, February, etc.\)\n')).lower()
        while month not in MONTHS:
            month = str(input('Not a valid month. Type \"list\" to get an overview \n?')).lower()
            if month == 'list':
                print(pd.DataFrame(MONTHS))

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = str(input('Which weekday are you interested in? \(all, Monday, Tuesday, etc.\)\n')).lower()
        while day not in WEEKDAYS:
            day = str(input('Not a weekday. Try again? \(all, Monday, Tuesday, etc.\)\n')).lower()
    else:
        # get random data for city, month and day
        city = random.choice(list(CITY_DATA.keys()))
        month = random.choice(MONTHS)
        day = random.choice(WEEKDAYS)

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
    print('You are now looking at data for:\n City: {}\n Month: {}\n Day: {}\n\n'.format(city, month, day))

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is: ', df['month'].mode()[0]+1)

    # display the most common day of week
    print('The most common day is: ', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('The most common start hour is: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most popular end station is: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('The most frequently used start-end-station is: ', (df['Start Station']+ ' to ' + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('In total, customers used the bike sharing for: ', (df['Trip Duration'].sum()/3600).round(2),'h')

    # display mean travel time
    print('The mean travel time is: ', (df['Trip Duration'].mean()/60).round(2),'min')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # Display counts of gender
    try: #check if column exists
        df['Gender']
    except KeyError:
        print('no Gender data found')
    else:
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    try: #check if column exists
        df['Birth Year']
    except KeyError:
        print('no Birth data found')
    else:
        print('Our oldest customer is born in: ', int(df['Birth Year'].min()))
        print('Our youngest customer is born in: ', int(df['Birth Year'].max()))
        print('Most commonly, our customers are born in: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        i = 0
        df = pd.DataFrame(df)
        while True:
            if i == 0:
                more = str(input('Would you like to see raw data of your selection? Enter yes or no. \n'))
            else:
                more = str(input('Would you like to see more? Enter yes or no. \n'))

            if more.lower() == 'yes':
                print(df.iloc[i:i+5])
                i = i+5
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

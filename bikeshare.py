import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all','january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    month = ''
    day = ''

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city.lower() not in CITY_DATA:
        city = input("\nWhich city do you want to explore ? (enter 'chicago', 'new york city' or 'washington'): ")
        #Check if input is valid. Not case sensitive thanks to .lower()
        city = city.lower()
        if city in CITY_DATA:
            print("Selected city: {}".format(city.title()))
            break
        else:
            print("Sorry, that doesn't match any of the city names. Please try again.")

    # get user input for month (all, january, february, ... , june)
    while month not in months:
        month = input("\nWhich month do you want to explore ? (enter 'all' or the month's name between January and June): ")
        #Check if input is valid. Not case sensitive thanks to .lower()
        month = month.lower()
        if month in months:
            print("Selected month: {}".format(month.title()))
            break
        else:
            print("Sorry, that doesn't match any of the months. Please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in days:
        day = input("\nWhich weekday do you want to explore ? (enter 'all' or the weekday): ")
        #Check if input is valid. Not case sensitive thanks to .lower()
        day = day.lower()
        if day in days:
            print("Selected weekday: {}".format(day.title()))
            break
        else:
            print("Sorry, that doesn't match any of the weekdays. Please try again.")

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        day = days.index(day)

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    #create hour column
    df['hour'] = df['Start Time'].dt.hour

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()
    # display using month name
    print("Most common month: {}".format(months[common_month[0]].title()))

    # display the most common day of week
    common_day = df['day_of_week'].mode()
    # display using weekday name
    print("Most common day of the week: {}".format(days[common_day[0]].title()))

    # display the most common start hour
    common_hour = df['hour'].mode()
    # display using weekday name
    print("Most common hour: {}".format(common_hour[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()
    print("Most common start station: {}".format(common_start[0]))

    # display most commonly used end station
    common_end = df['End Station'].mode()
    print("Most common end station: {}".format(common_end[0]))

    # display most frequent combination of start station and end station trip
    df['start_end'] = "From " + df['Start Station'] + ", to " + df['End Station']
    common_start_end = df['start_end'].mode()
    print("Most common trip: {}".format(common_start_end[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total travel time in seconds: {}".format(total_time))
    print("Total travel time in minutes: {}".format(total_time/60))
    print("Total travel time in hours: {}".format(total_time/3600))
    days_time = total_time/86400
    print("Total travel time in days: {}".format(days_time))
    if days_time > 30:
        print("*Wow, that's more than one month!*")

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("\nMean travel time in seconds: {}".format(mean_time))
    print("Mean travel time in minutes: {}".format(mean_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types: ")
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        print("\nCounts of gender: ")
        genders_nan = df['Gender'].isnull().sum().sum()
        print("Gender unknown {}".format(genders_nan))
        genders = df['Gender'].value_counts()
        print(genders)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nBirth year data: ")
        byear_nan = df['Birth Year'].isnull().sum().sum()
        byear_count = df['Birth Year'].count()
        print("(Watch out, birth year is unknown for {} users out of {})".format(byear_nan, byear_nan + byear_count))
        common_byear = df['Birth Year'].mode()
        print("Most common year of birth: {}".format(int(common_byear[0])))
        max_byear = df['Birth Year'].max()
        print("Most recent year of birth: {}".format(int(max_byear)))
        min_byear = df['Birth Year'].min()
        print("Earliest year of birth: {}".format(int(min_byear)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#write code to display 5 cpodes of raw code at a time
def print_raw(df):
    """Continues to diplay 5 rows of raw data upon request"""
    n = 0
    mode = 0 #to display initial message

    while True:
        if mode == 0:
                restart = input('\nWould you like to display some raw data? Enter yes or no.\n')
        else:
            restart = input('\nWould you like to display 5 more raws of data? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Stopping display of raw data...")
            break

        print("-"*40)
        print("\nDisplaying rows {} to {}:".format(n,n+5))
        for i in range(n,n+5):
            print("\n",df.iloc[i,0:len(df.columns)-4])
        n+=5
        mode = 1 # to display in process message


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Exiting program...")
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthBegin

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_Choice = ('all', 'january', 'february', 'march' ,'april','may', 'june')
day_Choice = ('All' , 'Monday' ,'Tuesday' , 'Wednesday' , 'Thursday' ,'Friday' ,'Saturday' , 'Sunday')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print()
        city = input("Enter a City from (chicago, new york city, washington) : ")
        if city in CITY_DATA:
            break   
        else:
            print('-'*30 ,'\n')
            print("Invalid input please choose one from the given list.\n\n")

    # get user input for month (all, january, february, ... , june)
    while True:
        print()
        month = input("Enter a Month from (all, january, february, ... , june) : ")
        if month.lower() in month_Choice:
            break   
        else:
            print('-'*30 ,'\n')
            print("Invalid input please choose one from the given list.\n\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    while True:
        print()
        day = input("Enter a Day from (all, monday, tuesday, ... sunday) : ")
        if day.title() in day_Choice:
            break   
        else:
            print('-'*30 ,'\n')
            print("Invalid input please choose one from the given list.\n\n")

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
    df = pd.read_csv(CITY_DATA[city] , parse_dates= ["Start Time", "End Time"])
    df['month'] = df['Start Time'].dt.month
    df['day_name'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # Filter by Month
    if month != 'all' :
        month_Id = month_Choice.index(month.lower())
        df  = df[ df['month'] == month_Id ]
    # Filter by Day
    if day != 'all' :
        df  = df[ df['day_name'] == day.title() ]

    return df


def time_stats(df,month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #! Display Time Stats
    # display the most common month
    month_Count =  df['month'].value_counts()
    print('The Most Comman Month is : {} with a Count = {}'.format(month_Choice[int(month_Count.index[0])] ,month_Count.max()))
    
    # display the most common day of week
    Day_Count =  df['day_name'].value_counts()
    print('The Most Comman Day is : {} with a Count = {}'.format( Day_Count.index[0] ,Day_Count.max()))
    
    # display the most common start hour
    Hour_Count =  df['hour'].value_counts()
    print('The Most Comman Hour is : {} with a Count = {}'.format( Hour_Count.index[0] ,Hour_Count.max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Stat_Count = df['Start Station'].value_counts()
    print('The Most Comman Start Station is : ("{}") with a Count = {}'.format( Start_Stat_Count.index[0] ,Start_Stat_Count.max()))
    # display most commonly used end station
    End_Stat_Count = df['End Station'].value_counts()
    print('The Most Comman End Station is : ("{}") with a Count = {}'.format( End_Stat_Count.index[0] ,End_Stat_Count.max()))

    # display most frequent combination of start station and end station trip
    newdf = df.groupby(['Start Station', 'End Station'])['User Type'].count()
    newdf= newdf.sort_values(ascending= False)
    
    print('The Most Frequent Combination of start station and end station trip is From ("{}")  To ("{}")  with a Count = {}'.format( newdf.index[0][0] ,newdf.index[0][1]  ,newdf.max() ))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The Total Travel Duration is : {}".format( int(df['Trip Duration'].sum())))

    # display mean travel time
    print("The Mean of Travel Duration is : {}".format( int(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count of User Type")
    print(df['User Type'].value_counts() )
    print("-"*40)
    # Display counts of gender
    try:
        print("Count of Each Gender")
        print(df['Gender'].value_counts() )
        print("-"*40)
    except:
        print("No Information About the Gender.\n")
    # Display earliest, most recent, and most common year of birth
    try:
        print( "The Earliest Year Of Birth : {}".format(int(df['Birth Year'].min())))
        print(  "The Most Recent Year Of Birth : {}".format(int(df['Birth Year'].max())))
        print(  "The Most Common Year Of Birth : {}".format(int(df['Birth Year'].mode().values[0])))
    except:
        print("No Information About the Birth Year.\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df , month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

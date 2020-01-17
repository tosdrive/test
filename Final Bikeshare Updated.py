import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def input_data(input_message, input_error, list_compare):
    error = 1
    while (error == 1):
        data = input(input_message).lower()
        if (data in list_compare):
            error = 0
        else:
            print(input_error)
    return data.lower()

def get_filters():
    """
    Prompts user to specify a city, month, and day for analysis.

    Returns:
        (str) city - name of the city for analysis
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). 
    cities = ["chicago", "new york city", "washington"]
    city = input_data("Enter your city: ", "Error, city not valid",cities)
    # TO DO: get user input for month (all, january, february, ... , june)
    months = ["all","january","february","march","april","may","june"]
    month = input_data("Enter the month (all, january, february, ... , june): ","Error, month not valid",months)
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    day = input_data("Enter your day of week (all, monday, tuesday, ... sunday): ", "Error, day not valid", days)
    
    return city, month, day # Return the variables


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
    df = pd.read_csv(CITY_DATA[city.lower()],parse_dates = ['Start Time', 'End Time']) # Read the CSV file and parse the Start Time and End Time fields to dates
    labels = []
    # Check each column
    for column_name in df.columns:
        new_col = column_name.replace(' ', '').lower() # Remove the space
        labels.append(new_col)
    df.columns = labels # Change the column labels
    months = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6}
    days = {"monday":0,"tuesday":1,"wednesday":2,"thursday":3,"friday":4,"saturday":5,"sunday":6}
    # If month and day is all, don't apply filter
    if (month.lower() == "all" and day.lower() == "all"):
        pass
    else:
        # If apply filter to month and day
        if (month.lower() != "all" and day.lower() != "all"):
            month_mask = df['starttime'].map(lambda x: x.month) == months[month.lower()] # Retrieve all information of the month
            day_mask = df['starttime'].map(lambda x: x.weekday()) == days[day.lower()] # Retrieve all information of the day
            df = df[month_mask & day_mask] # Save only the filtered information
        elif (month.lower() != "all"): # Filter by month
            month_mask = df['starttime'].map(lambda x: x.month) == months[month.lower()] # Retrieve all information of the month
            df = df[month_mask] # Save only the filtered information
        elif (day.lower() != "all"):
            day_mask = df['starttime'].map(lambda x: x.weekday()) == days[day.lower()] # Retrieve all information of the day
            df = df[day_mask] # Save only the filtered information
    return df


def time_stats(df):
    """Displays information on the most popular times of travel i.e, occurs most often in the start time."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    try:
        # TO DO: display the most common month
        months = ["January","February","March","April","May","June"]
        print("Most common month " + months[int(df['starttime'].dt.month.mode()) - 1]) # Print the common month, using mode 
        # TO DO: display the most common day of week
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                        'Saturday', 'Sunday']
        print("Most common day of week " + days[int(df['starttime'].dt.dayofweek.mode())]) # Print the common day, using mode

        # TO DO: display the most common start hour
        print("Most common start hour " + str(datetime.time(df['starttime'].dt.hour.mode()))) # Print the common start hour, using mode
    except:
        print("Nothing found!")
        


def station_stats(df):
    """Displays information on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    try:
        # TO DO: display most commonly used start station
        print("Most commonly used start station " + df['startstation'].mode().to_string(index = False)) # Display most commonly start station, using mode and remove index
        # TO DO: display most commonly used end station
        print("Most commonly used end station " + df['endstation'].mode().to_string(index = False)) # Display most commonly end station, using mode and remove index
        # TO DO: display most frequent combination of start station and end station trip
        df['trip'] = df['startstation'].str.cat(df['endstation'], sep=' -> ')
        print("Most frequent combination of start station and end station trip " + df['trip'].mode().to_string(index = False)) # Display most frequent trip, using mode and remove index
    except:
        print("Nothing found!")
        


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    try:
        # TO DO: display total travel time
        print("Total travel time " + str(datetime.timedelta(seconds=int(df['tripduration'].sum())))) # Displays the total travel time
        # TO DO: display mean travel time
        print("Mean travel time " + str(datetime.timedelta(seconds=int(df['tripduration'].mean())))) # Displays the mean travel time
    except:
        print("Nothing found!")
    


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # TO DO: Display counts of user types
        print("Count user type = Suscriber " + str(df.query('usertype == "Subscriber"').usertype.count())) # Counts all the Subscriber
        print("Count user type = Customer " + str(df.query('usertype == "Customer"').usertype.count())) # Counts all the Customer
        # TO DO: Display counts of gender
        
        print("Count user gender = Male " + str(df.query('gender == "Male"').gender.count())) # Count all Male
        print("Count user gender = Female " + str(df.query('gender == "Female"').gender.count())) # Count all Female

        # TO DO: Display earliest, most recent, and most common year of birth
        print("Earliest year of birth " + str(int(df['birthyear'].min()))) # Get the earliest birth year
        print("Most recent year of birth " + str(int(df['birthyear'].max()))) # Get the most recent birth year
        print("Most common year of birth " + str(df['birthyear'].mode().to_string(index = False))) # Get the common birth year
    except:
        print("Nothing found!")
      


def main():
    while True:
        raw_data = input('Want more Data? (yes/no)')
        if (raw_data == "yes"):
            city, month, day = get_filters()
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
               break
        else:
            break
if __name__ == "__main__":
    main()

import datetime as dt
import pandas as pd
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. Multiple values can be assigned for month and day.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month(s) to filter by, or "all" to apply no month filter
        (str) day - name of the day(s) of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
#Ask user to select a city
    city=input("Please enter a city: Chicago, New York or Washington?\n").lower()
    while city not in ("chicago", "new york", 'washington'):
            city=input("Sorry, your input is not valid! Enter a city: Chicago, New York or Washington?\n").lower()
    
#Ask user to define his time selection (month, day, both or none) 
    timech=input("You can filter the data by month, day, both or decide to apply no filter. Please select an option:\nMonth, Day, Both, None\n").lower()
    if timech not in ("month", "day", 'both', "none"):
            timech=input("Sorry, your input is not valid! You can filter the data by month, day, both or decide to apply no filter. Please select an option:\nMonth, Day, Both, None\n").lower()
    
# Function to run in case user wants to select month(s)
    def getmonth():
     month=input("Great! Now select for which month you want to analyze the data for {}. Select one or more between January, February, March, April, May, June. If you enter more than one month, separate them by comma and one space.\n".format(city.title())).title()
     monthLis=month.split("," " ")
     while not all(elem in ["January", "February", "March", "April", "May", "June"] for elem in monthLis):
          month=input("Sorry, your input is not valid! Please select for which month you want to analyze the data for {}. Select one or more between January, February, March, April, May, June. If you enter more than one month, separate them by comma and one space.\n".format(city.title())).title()#split("," " ")
          monthLis=month.split("," " ")
        
     return month
    
# Function to run in case user wants to select day(s)
    def getday():
        day=input("Great! Now select for which day of the week you want to analyze the data for {} in {} months. Please enter the whole name of the day. If you enter more than one day, separate them by comma and one space.\n".format(city.title(), month.title())).title()
        dayLis=day.split("," " ")
        while not all(elem in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] for elem in dayLis):
          day=input("Sorry, your input is not valid! Please select for which day you want to analyze the data for {} in {} months. Please enter the whole name of the day. If you enter more than one day, separate them by comma and one space.\n".format(city.title(), month.title())).title()
          dayLis=day.split("," " ")
     
        return day 
    
# Run appropriate time selection functions based on choice defined in "timech" input
    if timech == "none":
        month = "all"
        day = "all"
   
    if timech == "both":
        month=getmonth()
        day= getday()
    
    if timech == "month":
        day = "all" 
        month = getmonth()           
           
    if timech == "day":
        month = "all"
        day = getday()
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month(s) and day(s) if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month(s) to filter by, or "all" to apply no month filter
        (str) day - name of the day(s) of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    df["Start Time"]=pd.to_datetime(df['Start Time'])
    df["End Time"]=pd.to_datetime(df['End Time'])
      
    df['month'] = df["Start Time"].apply(dt.datetime.strftime, args=("%B",))
    df["dayweek"]=df["Start Time"].apply(dt.datetime.strftime, args=("%A",))
    
    
    if month != 'all':
        monthLis=month.split("," " ")
        df = df[df["month"].isin(monthLis)]
        
    
    if day != 'all':
        dayLis=day.split("," " ")
        df = df[df["dayweek"].isin(dayLis)]
        
    
    return df


def time_stats(df, month, day, city):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        (df) df - the dataframe filtred as appropriate
        (str) month - name of the month(s) to filter by, or "all" to apply no month filter (used to define truth conditions to show appropriate data and to display information)
        (str) day - name of the day(s) of week to filter by, or "all" to apply no day filter (used to define truth conditions to show appropriate data and to display information)
        (str) city - name of the selected city (used to display information)
     
    
    """
    
    start_time = time.time()
    print('\nCalculating The Most Frequent Times of Travel...\n')
    
# Select from Start hour the starting hour and convert it into an integer 
    df['starthour'] = df["Start Time"].dt.hour
    
# Count entries by starting hour and calculate index for highest value, highest value and mean value
    counted_df_sthour=df["starthour"].value_counts()
    popular_sthour=counted_df_sthour.idxmax()
    popular_sthour_count=counted_df_sthour.max()
    mean_users_sthour=counted_df_sthour.mean()
    
# Define strings with selected values, total number of entries in selection and counts by starting hours 
    selection="City: {}\n Months selected: {}\n Days of the week: {} \n\n".format(city.title() ,month.title(), day.title())
    totalcount="Count of entries in selection: {} \n\n".format(df.count()[0])     
    timedata="Most common starting hour in selection: {}\n Count of users starting ride between {}.00 and {}.59 in selection: {}\n Mean number of users per starting hour in selection: {} \n\n".format(popular_sthour,popular_sthour,popular_sthour, popular_sthour_count, round(mean_users_sthour,))
        
    
# Define condition truth to print appropriate output
    monthLis=month.split("," " ")
    dayLis=day.split("," " ")
    
    conditionshowmonth=len(monthLis)>1 or month=="all"
    conditionshowday=len(dayLis)>1 or day=="all" 
    
    
# Print appropriate output based on selection
    if not conditionshowmonth and not conditionshowday:
        print(selection, totalcount, timedata)  
     
    if conditionshowmonth and conditionshowday:
        counthed_df_month=df["month"].value_counts()
        popular_month=counthed_df_month.idxmax()
        popular_month_count=counthed_df_month.max()
        mean_users_month=counthed_df_month.mean()
        counted_df_day=df["dayweek"].value_counts()
        popular_day=counted_df_day.idxmax()
        popular_day_count=counted_df_day.max()
        mean_users_day=counted_df_day.mean()
        datamonth="Most common month in selection: {}\n Count of users in {} in selection: {}\n Mean number of users per month in selection: {} \n\n".format(popular_month.title(),popular_month.title(), popular_month_count, round(mean_users_month,))
        dataday="Most common day in selection: {}\n Count of users on {}s in selection: {}\n Mean number of users per day in selection: {} \n\n".format(popular_day.title(),popular_day.title(), popular_day_count, round(mean_users_day,))
        print(selection, datamonth, dataday, timedata)

    if conditionshowmonth and not conditionshowday:
       counthed_df_month=df["month"].value_counts()
       popular_month=counthed_df_month.idxmax()
       popular_month_count=counthed_df_month.max()
       mean_users_month=counthed_df_month.mean()
       datamonth="Most common month in selection: {}\n Count of users in {} in selection: {}\n Mean number of users per month in selection: {} \n\n".format(popular_month.title(),popular_month.title(), popular_month_count, round(mean_users_month,))
       print(selection, totalcount, datamonth, timedata)

    if not conditionshowmonth and conditionshowday:
        counted_df_day=df["dayweek"].value_counts()
        popular_day=counted_df_day.idxmax()
        popular_day_count=counted_df_day.max()
        mean_users_day=counted_df_day.mean() 
        dataday="Most common day in selection: {}\n Count of users on {}s in selection: {}\n Mean number of users per day in selection: {} \n\n".format(popular_day.title(),popular_day.title(), popular_day_count, round(mean_users_day,))
        print(selection, totalcount, dataday, timedata)
            

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

# Calculate most commonly used start station
    counted_df_ststation=df["Start Station"].value_counts()
    popular_ststation=counted_df_ststation.idxmax()
    popular_ststation_count=counted_df_ststation.max()
    mean_users_ststation=counted_df_ststation.mean()  

# Calculate most commonly used end station
    counted_df_endstation=df["End Station"].value_counts()
    popular_endstation=counted_df_endstation.idxmax()
    popular_endstation_count=counted_df_endstation.max()
    mean_users_endstation=counted_df_endstation.mean()

# Calculate most frequent combination of start station and end station trip
    df["Start+End Station"]="from " + df["Start Station"] + " to " + df["End Station"] 
    counted_df_startendstation=df["Start+End Station"].value_counts()
    popular_startendstation=counted_df_startendstation.idxmax()
    popular_startendstation_count=counted_df_startendstation.max()
    mean_users_startendstation=counted_df_startendstation.mean()

#Print values for most commonly used start, end and combination of start and end stations
    print("Most common start station in the selected period: {}, {} users \n Average user count for start station in the selected period: {} \n".format(popular_ststation, popular_ststation_count, round(mean_users_ststation,)))
    print("Most common end station in the selected period: {}, {} users \n Average user count for end station in the selected period: {} \n".format(popular_endstation, popular_endstation_count, round(mean_users_endstation,)))
    print("Most common combination of start station and end station trip: {}, {} users \n Average user count for other combinations in the selected period: {}".format(popular_startendstation, popular_startendstation_count, round(mean_users_startendstation,)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        (df) df - the dataframe filtred as appropriate
        (str) city - selected city (used to display information)
        
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

# calculate total travel time
    total_travel_time=sum(df["Trip Duration"])
    m, s = divmod(total_travel_time, 60)
    h, m = divmod(m, 60)

# calculate mean travel time    
    mean_travel_time=(df["Trip Duration"]).mean()
    mm, ms = divmod(mean_travel_time, 60)
    
#print total and mean travel time
    print("Total amount of travel time in selection: {} h {}' {}\"".format(h,m, round(s,)))
    print("Average duration of single travel in selection: {}' {}\"".format(round(mm,),round(ms,)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

# Display counts of user types
    user_types = df["User Type"].value_counts()
    print("Breakdown of user types: \n{} \n".format(user_types.reset_index().to_string(header=None, index=None)))
    

# Display counts of gender if available
    if "Gender" in list(df):
        gender = df["Gender"].value_counts()
        print("Breakdown of user by gender: \n{} \n".format(gender.reset_index().to_string(header=None, index=None)))
    else:
        print("Gender data not available for {}.".format(city.title()))

 
# Display earliest, most recent, and most common year of birth if available
    if "Birth Year" in list(df):
        birthyear = df["Birth Year"].value_counts()
        popular_birthyear=int(birthyear.idxmax())
        max_birthyear=int(df["Birth Year"].max())
        min_birthyear=int(df["Birth Year"].min())
        print("Most common user birth year: {} \n Most recent birth year: {} \n Earliest birth year: {}".format(popular_birthyear, max_birthyear, min_birthyear))
    else:
        print("Birth year data not available for {}.".format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip_data (df):
    """
    Give option to visualize the entire df.
    
    """
    ind_confirm=input("You can visualize all the individual entries in the selection by entering ""yes"" (for practical reasons, this  will visualize 1000 rows at time). Otherwise, press Enter. \n").lower()
    x=0
    with pd.option_context('display.max_rows', 1000):
     while ind_confirm == "yes":
        print(df[x:x+999])
        x+=1000
        if x>len(df):
            input("End of the dataframe reached!. Please press Enter") 
            break
        ind_confirm=input("These are 1000 entires. If you want to visualise the following 1000, enter ""yes"". Otherwise, press Enter. \n").lower()
        

        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day,city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        individual_trip_data (df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

# Course Sniper Bot
***
## Description:
  - A discord bot that notifies me when a specific course or courses open up
  - Specifically, the bot uses the index of a course to see if a course is open
  - All indexes are stored in a cloud PostgreSQL server
***  
## Functionality: 
  - Through the discord server, one can add a course that they want the bot to look for
  - To add a course, the following command must be used: `.addCourse {indexNumber}`
***    
## Extracting Data (*main.py*)
  - By using a URL, the program first gets the indexes of all open sections
    - URL: `https://sis.rutgers.edu/soc/api/openSections.json?year=2021&term=9&campus=NB`
***
## Finding the Course (*main.py*)
  - A function called "check_courses" gets the indexes of the open sections and runs a loop that searches for all of the indexes in the database
  - If a match is found, a notification is sent in the discord channel and the found index is removed from the database
  - The function runs every **10 seconds** 
***
## License
  - This project's source code is licensed under BSD-2-clause License

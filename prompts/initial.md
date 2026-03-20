please create the following rules:
- properly architected with oop best practices
- properly commented
- type inferences
- written using TDD, covering edge cases
- written using tkinter


project:
a python gui application that displays a large timer (cyan) in the middle of the screen that the user can start or stop. start and stop are each buttons, different colors (but with complementary font tones to cyan), that should work when the system is in dark mode. when start is clicked, the timer starts. when stop is clicked, the timer stops. 

whenever either button is clicked, a new entry in a json object is created and appended to a json log file for that day (date in the filename title). the json object contains a unique id (and be sequential per file), start_time, stop_time, total_time

additionally, to the top left of the timer, is the button "previous day totals". clicking on this button leads to a new screen where a table-like display is shown with previous dates being the first column and the total time worked (totals from the day's json log) displayed as hh:mm:ss. have a back button to get back to the timer screen. if the timer is running when this button is clicked, the timer should still run even though it's not displayed.

the previous day button should be able to be clicked multiple times and only effect the view, not the timer.
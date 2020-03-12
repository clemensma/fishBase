# fishBase
## Calculating the average fish

### Scrape.py
Opens fishbase.org on a given data group and creates a list of links leading to the actual data.
List of links is then opened one by one an the actual data is scraped out and saved in a pandas data frame.
If a fish has more than one speed listed, the mean is calculated.
A function is builtin to calculate the average speed of all fish.
See toDo.md for current tasks.

### Implementing a progress bar
use http://qpleple.com/add-progress-bars-to-your-python-loops/

### To access specific data in the frame
use https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html instead of df[i][k]

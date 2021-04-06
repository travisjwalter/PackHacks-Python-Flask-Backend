import requests
from bs4 import BeautifulSoup

## This file is the Indeed.com scraper for the Backend PackHacks workshop. This file is set
## up in a extract, transform, and return format, which should be followed for other similar
## scrappers if you are wanting to scrape other sites.
## We import requests and BeautifulSoup from pip install beautifulsoup4 to do the scrapping.
## @author Travis Walter - 3/16/2021

## This extract function extracts the html webpage from the url we are giving it and returning
## it to the caller (using request and BeautifulSoup).
def extract(pageNum):
    ## Found by googling "my user agent" and will be done in workshop as it can be different 
    ## for everyone.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    ## This is the url that we are scrapping from. Some investigation is needed before
    ## parameterizing the url to see how it changes and what each section does. We will go over
    ## this is the workshop.
    url = f'https://www.indeed.com/jobs?q=software+engineer&l=Raleigh-Durham,+NC&radius=50&start={pageNum}'

    ## This is the HTTP GET request call that pulls all the website data from the url into the
    ## script and places it into the r var.
    r = requests.get(url, headers)

    ## This is where we call the BeautifulSoup library for parsing the content from the webpage.
    ## Invoking .content on the request gives us the bytes that we can parse. We are parsing the
    ## webpage's html so we are going to user 'html.parser', but we could've also used 'xml.parser'
    ## if we were parsing xml content. BeautifulSoup returns the html content parsed from the
    ## request. We place that return value to the soup var.
    soup = BeautifulSoup(r.content, 'html.parser')

    ## Return the html parsed content to the caller.
    return soup

## This transform function pulls the information from the html content extracted
## by the extract function. We pull all the information we want from the html here and add a job
## dictionary to a joblist list.
def transform(jobList, soup):
    ## Indeed structures its job information into divs named 'jobsearch-SerpJobCard'. We will show
    ## you how to find this div while on the Indeed Job Search page and where to find the others
    ## below. For this, we are finding all the job search cards by div from the soup by invoking
    ## find_all on the soup parameter. For Indeed, this should return a list (of len 15) of cards
    ## that we can further search through.
    allDivs = soup.find_all('div', class_ = 'jobsearch-SerpJobCard')

    ## For each loop to loop through all cards in the list to parse information from each.
    for item in allDivs:
        ## Investigating the Indeed webpage, we can see that the title is held within the first
        ## 'a' block. We find the first instance of 'a' in the card and get the striped text.
        ## This text is the title of the job we are scraping for, thus, we place it into the title
        ## var. We invoke find instead of find_all because we don't want a list of all 'a' blocks.
        title = item.find('a').text.strip()

        ## Investigating the Indeed webpage, we can see that the name of the company is held
        ## within the first 'span' field in the class 'company'. We invoke find here with
        ## 'span', looking in the class_ 'company' to get the text, which is the stripped then
        ## assigned to the company var.
        company = item.find('span', class_ = 'company').text.strip()

        ## This try except block is for the salary field in a job. Indeed doesn't force
        ## employers to add the salary to the job posting, but if they do, we want to catch it.
        ## Find a posting that has a salary and investigate it like we did for the previous two
        ## fields. The salary is held within the first 'span' field in the class 'salaryText'.
        ## We invoke find here with 'span', looking in the class_ 'salaryText' to get the text.
        ## If it exists, it is stripped then assigned to the salaray var. If it doesn't exist
        ## then set the salary var to be empty ('').
        try:
            salary = item.find('span', class_ = 'salaryText').text.strip()
        except:
            salary = ''

        ## Investigating the Indeed webpage, we can see that the job summary of the listing is
        ## held within the the first div in the class 'summary'. We invoke find here with
        ## 'div', looking in the class_ 'summary' to get the text, which is then stripped.
        ## While developing this system the summary appeared to have a lot of unneeded new line
        ## characters, so we replaced the new line character with the '' character by invoking
        ## replace. Once this is all done, we assign the text to the summary var.
        summary = item.find('div', class_ = 'summary').text.strip().replace('\n', '')

        ## We don't want anymore information, so it's time to compile everything into a dictionary
        ## and append it to the job list.
        ## To do this, we create a dictionary following to structure below. This will be how the
        ## information will appear to the frontend as well.
        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary
        }

        ## Add the job dictionary to the list
        jobList.append(job)

    ## Return. MAKE SURE IT'S OUTSIDE THE FOR EACH LOOP OR YOU WILL ONLY GET ONE JOB
    return jobList


## This getList function is the frontfacing function for this file. This function is called
## by the Flask endpoint to get the full list of job dictionaries.
def getList():
        
    ## Initiate the jobList var to an empty list.
    jobList = []

    ## Indeed handles pages in groups of 10s by the url but there are 15 jobs on each page.
    ## This for loop gets 75 jobs (15 * 5) for 5 pages. You can increase the middle value
    ## by 10 to get 15 more jobs. Range here is used to do a for each loop so that we can pass
    ## the page number to the extract function. Range(0, 50, 10) returns a list of 0, 10, 20,
    ## 30, 40, and 50 that the loop loops through.
    for i in range(0, 50, 10):
        ## This is the caller to the extract the page with the page number provided by the for
        ## each loop. The soup value is returned and assigned to the var content which will be
        ## used to pass to the transform function.
        content = extract(i)

        ## Transform the content with the transform function.
        transform(jobList, content)

    ## Return the jobList after all the functions have run.
    return jobList

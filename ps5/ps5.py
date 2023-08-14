# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory (object):
    def __init__ (self, guid, title, description, link, pubdate=None):
        '''
        Initializes a NewsStory object
                
        guid (string): the global unique identifier
        title (string): The title of the article
        description (string): a paragraph or so description of the article
        link (string): links to the additional content surrounding the article
        pubdate (datetime): the publication date of the article, defaults to none if no date

        A NewsStory object has five attributes:
            self.guid (string, determined by input guid)
            self.title (string, determined by input title)
            self.description (string, determined by input description)
            self.link (string, determined by input link)
            self.pubdate(datetime, determined by input pubdate)
        '''

        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        '''
        Used to safely access self.guid outside of the class
        
        Returns: self.guid
        '''
        
        return self.guid
    
    def get_title(self):
        '''
        Used to safely access self.title outside of the class
        
        Returns: self.title
        '''
        
        return self.title
    
    def get_description(self):
        '''
        Used to safely access self.description outside of the class
        
        Returns: self.description
        '''
        
        return self.description
    
    def get_link(self):
        '''
        Used to safely access self.link outside of the class
        
        Returns: self.link
        '''
        
        return self.link
    
    def get_pubdate(self):
        '''
        Used to safely access self.pubdate outside of the class
        
        Returns: self.pubdate
        '''
        
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

class PhraseTrigger (Trigger):
    def __init__(self, phrase):
        """
        Initializes a PhaseTrigger object

        phrase (string): The phrase to use for the trigger

        A PhraseTrigger has one attribute:
            self.phrase (string, determined by input text)
        """

        self.phrase = phrase.lower()

    def in_text(self, text):
        """
        Checks whether self.phrase is in the inputted text

        Returns: True or False
        """

        tempString = text.lower()

        for puncs in string.punctuation:
            # each punctuation is replaced with a space
            # note: strings are immutable, this is inefficient
            tempString.replace(puncs, " ")
            
        # splits tempString into list of words
        strippedWords = tempString.split(" ")
        # splits the phrase into a list of words
        splitPhrase = self.phrase.split(" ")

        # if any of the phrase words aren't in the list, there's no match
        if splitPhrase[0] not in strippedWords:
            return False
        # otherwise there could be a match
        else:
            # for each word in the given text
            for textWords in strippedWords:
                # if any word is the first word of our phrase
                if textWords == splitPhrase[0]:
                    # get this words index and begin checking the rest of the phrase
                    index = strippedWords.index(textWords)
                    # start a loop count at 1, so as to check the 2nd element of splitPhrase first
                    for i in range(1, len(splitPhrase)):
                        index += 1
                        if splitPhrase[i] == strippedWords[index]:
                            # if the last word of the phrase string has been reached
                            # the full phrase is in the text
                            if (i+1) == len(splitPhrase):
                                return True
            
            # if this point is reached there was no matches
            return False




            

# Problem 3
# TODO: TitleTrigger

# Problem 4
# TODO: DescriptionTrigger

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6
# TODO: BeforeTrigger and AfterTrigger


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

# Problem 8
# TODO: AndTrigger

# Problem 9
# TODO: OrTrigger


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    return stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

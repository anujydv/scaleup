import os
import re

# USER DEFINED CLASS
import logging
from src.logger.logger import standardLogger
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(standardLogger().get_console_handler())


##This class is used to apply various cleansing steps.
#It has five functions as below:-
#, read_words_from_file()
#, singularize()
#, remove_stop_words()
#, ngrams()
#, apply()
class Cleaner(object):

    ## The constructor. to load the required resources.
    #@param self The object pointer
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        try:
            self.stops = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            nltk.download('punkt')
            nltk.download('wordnet')
            self.stops = set(stopwords.words('english'))
        self.stops.remove("it")

    ## This function is used to read the data from given file.
    #  @param self The object pointer.
    #  @param filepath is actual file path
    def read_words_from_file(self, filepath):
        data = []
        if os.path.isfile(filepath):
            data = [line.strip() for line in open(filepath, 'r')]
        return set(data)

    ## This function is used to singularize the tokens in a string.
    #  @param self The object pointer.
    #  @param string is input text
    def singularize(self, string):
        tokens = nltk.word_tokenize(string)
        new_tokens = []
        for token in tokens:
            if len(token) > 3:
                token = self.wnl.lemmatize(token, 'n')
            new_tokens.append(token)
        return ' '.join(new_tokens)

    ## This function is used to remove stopwords from input text
    #  @param self The object pointer.
    #  @param string is input text.
    #  @param replacement have a value which will be replaced with stopwords
    def remove_stop_words(self, string, replacement=None):
        tokens = string.split()
        processed_tokens = []
        for token in tokens:
            if token not in self.stops:
                processed_tokens.append(token)
            elif replacement:
                processed_tokens.append(replacement)
        string = ' '.join(processed_tokens).strip()
        return string

    ## This function generate NGrams from a list of tokens.
    #  @param self The object pointer.
    #  @param text: list of words from text.
    #  @param display: list of display words
    #  @param n: NGram length in terms of words
    def ngrams(self, text, display, n):
        output = []
        for i in range(len(text) - n + 1):
            output.append(" ".join(text[i:i + n]))
            display.append(" ".join(display[i:i + n]))
        return output

    ## This is a main function to apply all cleaning steps.
    #  @param self The object pointer.
    #  @param string The actual raw text.
    def apply(self, string):
        string = re.sub("[^a-zA-Z0-9\+\.\#]+", " ", string)
        string = self.remove_stop_words(string)
        string = self.singularize(string)
        return string

# **cs5293sp22-project1**
# **Author: Varshitha Choudary Vasireddy**

## Description of the project:
The Redactor is a program for hiding sensitive information such as Names, and places from the public. Whenever sensitive information is shared with the public, the data must go through a redaction process. That is, all sensitive names, places, and other sensitive information must be hidden. Documents such as police reports, court transcripts, and hospital records all containing sensitive information. Redacting this information is often expensive and time consuming. In this project, we will use our knowledge of Python and Text Analytics to design a system that accept plain text documents then detect and redact “sensitive” items.

## Packages used in Project are
- argparse
- glob
- sys
- os
- commonregex
- nltk
- re
- pyap
- spacy

## 1. main.py
This file consists of 6 functions. Each function redacts different entities.  
Below packages are to be imported and downloaded in order for the main.py to run successfully.
~~~
import nltk
from commonregex import CommonRegex
import pyap
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, sent_tokenize
import re
import spacy
nlp = spacy.load("en_core_web_lg")
from nltk.corpus import wordnet
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('punkt', quiet=True)
~~~
### i. redact_names(data)
In this function, the names will be redacted from the data file. By using Nltk the data is word tokenized, then the words are classified into parts of speech and labeling is done, then chuncking is done on the classified data to give chunk tags. Then subtress is selected with label as 'PERSON' or 'GPE'
~~~
def redact_names(data):
    words = nltk.word_tokenize(data)
    tag = nltk.pos_tag(words)
    tree = nltk.ne_chunk(tag)
    #names_list = [ent[0][0] for ent in list(tree.subtrees()) if ent.label() in ['PERSON']]
    names_list = [ent[0][0] for ent in list(tree.subtrees()) if ent.label() in ['PERSON','GPE']]
    for item in names_list:
        data = data.replace(item, '\u2588'* len(item))
    return data, names_list
~~~
I am redacting all names of persons and geopolitical and geographical entities, like country and city names as well.
This function gives the data that is redacted and the list of names that got redacted.

### ii.redact_dates(data)
I changed the redacting dates functions. I now used spacy to redact dates.
I also included regex equation inorder to pull all dates which will not detected by spacy
~~~
def redact_dates(data):
    data1 = nlp(data)
    dates_ent_list = []
    for i in [ent.text.split('\n') for ent in data1.ents if ent.label_ == "DATE"]:
        for j in i:
            dates_ent_list.append(j)
    pattern = '(\d{1,4}/\d{1,2}/\d{1,4})'
    dates_re_list = re.findall(pattern,data)
    dates_list = set(dates_ent_list + dates_re_list)
    for items in dates_list:
        data = data.replace(items,'\u2588'* len(items))
    return data,dates_list
~~~
I am first converting the data into nlp and creating a list called "dates_ent_list" when labels are "DATE". A pattern of regex expression which matches dates in the format "yyyy/mm/dd" or "dd/mm/yyyy" is written i.e **'(\d{1,4}/\d{1,2}/\d{1,4})'** and the data is checked with that pattern and a new list called **dates_re_list**. The lists are then added and in order to avoid duplicates "set" datatype is used and then set is iterated and each element of set is redacted. Words like "day, tomorrow and yesterday" are also getting recognized by spacy as DATES, so I removed them from the set and then redacted the remaining recognized dates

Referred: https://github.com/madisonmay/CommonRegex

### iii. redact_phones(data)
This function will redact phone numbers. Used a package called **commonregex** to do this. The data is firstly changed into Regex data and then a method called phones is applied to the data to extract phone numbers.
~~~
def redact_phones(data):
    data1 = CommonRegex(data)
    phones_list = data1.phones
    for item in phones_list:
        data = data.replace(item,'\u2588'* len(item))
    return data, phones_list
~~~
the phone numbers gets replaced by block character, impling it will be redacted from the data.  
Data and list of phone numbers that got redacted are returned.

Referred: https://github.com/madisonmay/CommonRegex

### iv. redact_genders(data)
This function will redact gender revealing terms. I wrote a list of gender revealing words. Data undergoes word tokenization and then all words are converted in lower case and that word is passed to Lemmatization process so that plural of the words can be changed into singular tense of that word. These words are taken and are compared with the gender revealing list that I prepared, if the word is in the list then the word is replaced with block character impling it gets redacted from the data. 
~~~ 
    tokens = word_tokenize(data)
    lemmaterizer = WordNetLemmatizer()
    for tok in tokens:
        if lemmaterizer.lemmatize(tok.lower()).replace('.', '') in list_gender:
            genders_list = genders_list + [tok]
            data = re.sub(r'\b{0}(\'s)?\b'.format(tok.replace('.', '')), '\u2588'* len(tok), data)
~~~
I wrote regular expression substitute equation with word boundary so that only the word gets redacted but the word which contains the word in list doesn't get redacted ex he is redacted he in 'them' will not be replaced by subtitute function as word boundary(\b) is mentioned. And also if a word is present with **'s** to the gender revealing term then even **'s** is to be redacted, for example I redacted the whole father's word in the data file.  
Data file and gender revealing words that got redacted are brought into a list and are returned.

Referred: https://www.regular-expressions.info/wordboundaries.html, https://www.geeksforgeeks.org/nlp-synsets-for-a-word-in-wordnet/

### v. redact_address(data)
The address in the data file gets redacted. Used **pyap** package to detect the address among the data.  
Data is parsed using below command to get the addresses which are specific to US country.
> addresses = pyap.parse(data,country = 'US')
address is converted into string and it is split by ',' and the starting index of the address is taken by using str[0].  
ending index of the address is found by str[-1]
strip() function is used to remove any white spaces before and after the string.
~~~
def redact_address(data):
    address_list = []
    addresses = pyap.parse(data,country = 'US')
    for address in addresses:
        start_index = data.index(str(address).split(',')[0].strip())
        end_index = data.index(str(address).split(',')[-1].strip()) + len(str(address).split(',')[-1].strip())
        address_list.append(data[start_index:end_index])
        data = data[:start_index] + '\u2588'* len(str(address)) + data[end_index:]
    return data, address_list
~~~
The address list is appended with the list data that starts with start index till end index that is extracted. And that list data is blocked.   
Data that is redacted and the list of redacted addresses is returned.

referred: https://github.com/vladimarius/pyap

### vi. redact_concept(data,concepts)
In this function the whole sentence which contains the concepts argument word will be redacted. Synonyms for the concepts arguments will be taken with the help of **wordnet.synsets(concepts)** and **.name()** for the lemmation will give synonyms list. The word is converted into lower case and then synonyms of it are taken.  
The data is converted into sentences using **sent_tokenize(data)** and then into words. And each word is checked with the synonyms list and if any word is matching the synonym list then the entire sentence of that particular word is replaced by blocked character.
~~~
def redact_concept(data,concepts):
    synonyms = []
    concept_redacted_list = []
    for concept in concepts:
        for syn in wordnet.synsets(concept.lower()):
            synonyms += [l.name() for l in syn.lemmas()]
    l = WordNetLemmatizer()
    sentences = sent_tokenize(data)
    for s in sentences:    
        tokens = word_tokenize(s)
        list2 = []
        for words1 in tokens:
            list2.append(words1.lower())
        tok_lemmas = [l.lemmatize(token) for token in list2]
        
        for tok_lemma in tok_lemmas:
            if tok_lemma.lower() in synonyms:
                concept_redacted_list = concept_redacted_list + [s]
                data = data.replace(s, '\u2588'* len(s))
                continue    
    
    return data, concept_redacted_list 
~~~
Data file after redaction and the list of redacted sentences are returned.

Referred: https://www.geeksforgeeks.org/nlp-synsets-for-a-word-in-wordnet/

## 2. redactor.py
Packages to be imported for redactor.py file are argparse, glob, sys and os.  
Multiple input arguments are accepts by this python file. main.py file is imported into this file and function operations are performed according to the arguments that are passed. 

By using the argparser package we create a object **"parser"** and input arguments are added by add_argument method  
Below are the input arguments that are added by the add_argument method.
- --input
- --names
- --gender
- --date
- --concept
- --output
- --stats  

Firstly 2 empty dictionaries are considered namely "redact_counts" and "redact_list" to count redacted words/sentences for a particular argument and to write the redacted words/sentences data for a particular argument respectively for each function.
### --input
Extension of the files is given as part of this argument. Ex: "*.txt". This is a required argument.  
glob.glob is taken to pull all the files with the given input extension.

data from the extension file is read into **data** file. If data from the file is not readable it gives error stating that it can't be readable or reductable. The code is
~~~
try:
    with open(raw_file, 'r') as f:
        data = f.read()
except:
    print(f"{raw_file} that is given cant be read and so it can't be redacted\n")
    continue
~~~

### --names
If this argument is given, all names present in the data file will be redacted. redact_names function will be called and the data and redacted list output is taken in redact_list dictionary and redact_count dictionary respectively.

### --dates
If this argument is given, then all dates in the data file will be redacted. redact_dates function will be called, output is stored in the dictionaries that are mentioned above.

### --phones
If this argument is given, then all phone numbers in the data file will be redacted. redact_phones function will be called, output is stored in the dictionaries that are mentioned above.

### --genders
If this argument is given, then all gender revealing words in the data file are to be redacted. redact_genders function will be called output is stored in the dictionaries that are mentioned above.

### --address
If this argument is given, then addresses in the data file are to be redacted. redact_address function will be called, output is stored in the dictionaries that are mentioned above.

### --concept
If this argument is given, then sentences having any word matching with the meaning of concept argument in the data file are to be redacted. redact_concept function will be called, output is stored in the dictionaries that are mentioned above.

### --output
It tells about how the output of the data is to be display. if given "stdout" or "stderr" then output should be displayed directly to the screen console, else the output will be taken as the input_files path and ".redacted" as extension. Below command is used to write data to screen console
>sys.stdout.write(data)

To write output into the input_files path and the same name as input_file below code is used.
~~~
def write_to_files(raw_file, data):
    if not os.path.exists(args.output):
        os.mkdir(args.output)
    
    out_file_name = f"{raw_file}.redacted"

    sub_folders = out_file_name.split('/')[:-1]
    for sub_folder in sub_folders:
        sub_folder_path = os.path.join(args.output, sub_folder)
        if not os.path.exists(sub_folder_path):
            os.mkdir(sub_folder_path)

    with open(os.path.join(args.output, out_file_name), 'w') as f:
        f.write(data)

    print(f"Saved to {os.path.join(args.output, out_file_name)}")
~~~
I changed the code so that the file name is taken and .redacted is added to it, if input is given from the subfolders then the output also has to be created in that subfolder so "/" is used for split. Then also naming the file and making sure that it is created in the correct path, the redacted data is written into it.

### --stats
If this argument is given then stats file has to be created and it tells on how that stats file has to be displayed or saved into another file by giving the file name. If stdout or stderr is given in argument, then stats file is displayed on console, else stats summary is sent into file where file name is specified in the console. And stats is written for each input file that is given to the program.

~~~
def write_to_files_stats(raw_file, stats):
    raw_file_path = os.path.join(os.getcwd(), raw_file)

    with open(raw_file_path, 'w') as f:
        f.write(stats)

    print(f"Stats to {raw_file_path}")
    print("\n")
~~~

I also wrote another function for stats which tells about the summary of the redactions that are done to the given input file. It is named as **redact_stats**, arguments, the redacted words/sentences list and the count of the redacted items are taken as the input arguments. Input Arguments are checked and summary is written accordingly. **redact_counts** and **redact_list** are used in the stats file to give the summary.

Below is the redact_stats function.
~~~
def redact_stats(args, redact_counts, redact_list):
    stats_list = []

    if vars(args)['names']:
        stats_list.append(f"In total {redact_counts['names_count']} names got redacted.")
        stats_list.append(f"\tThe names that got redacted are {redact_list['names_list']} ")
    if vars(args)['dates']:
        stats_list.append(f"In total {redact_counts['dates_count']} dates got redacted.")
        stats_list.append(f"\tThe dates that got redacted are {redact_list['dates_list']} ")
    if vars(args)['phones']:
        stats_list.append(f"In total {redact_counts['phones_count']} phone numbers got redacted.")
        stats_list.append(f"\tThe phones that got redacted are {redact_list['phones_list']} ")
    if vars(args)['genders']:
        stats_list.append(f"In total {redact_counts['genders_count']} genders got redacted.")
        stats_list.append(f"\tThe genders that got redacted are {redact_list['genders_list']} ")
    if vars(args)['address']:
        stats_list.append(f"In total {redact_counts['address_count']} address/es got redacted.")
        stats_list.append(f"\tThe address/es that got redacted are {redact_list['address_list']} ")
    if vars(args)['concept']:
        stats_list.append(f"In total {redact_counts['concept_count']} concept sentences got redacted.")
        stats_list.append(f"\tThe concept statements that got redacted are {redact_list['concept_list']} ")
    return "\n".join(stats_list)
~~~

### Functions calling placement
When calling functions, I am first calling **redact_address** so that address gets redacted first and then later functions are called and redactions takes place. If the address is "1619 George Washington Lane", then if redact_names function is called first, it redacts George and when redact_address function tries to check address, it is not considered as address and hence that doesn't get redacted. But if address is called first after redacting all addresses later names will be detected and redacted.

## 3. tests
Written 6 different test files for 6 different function that I wrote in main.py file. 

All the test cases have below format

~~~
import pytest

#redacting function is called
from project1.main import redact_function

#testdata to check redact_function is specified below
#Giving the input data, expected redacted data and count of 
#that redactes data file words/sentences according to the functionality of the redact_function.
testdata = [
    (input_data,expected_redacted_data,Redacted_data_count)
]

#parameters given are input data, expected redacted data and count of redacted words/sentences.
#This text is to be carried out on testdata
@pytest.mark.parametrize("input_data,expected_redacted_data,Redacted_data_count", testdata)
def test_word(input_data,expected_redacted_data,Redacted_data_count):
    #From the redact_function, the text that is redacted is taken, and the list of redacted words/sentences #is taken. 
    actual_text, word_list = redact_function(input)
    print(actual_text)

    #Output text of redact_function is cheked with expected redact_function output
    assert actual_text == expected_redacted_data
    assert len(word_list) == Redacted_data_count
~~~
So for every different redact_function it is imported into the test file, and an input file is given and according to the redact_function expected output file is taken. And the output file after processing from redact_function is checked with expected output file to give the results of test cases.

Only for redact_concept function, the whole sentence of data in which word related to concept is redacted, in other redact functions words of the data are redacted.

6 test files test_names.py,test_phones.py,test_address.py,test_genders.py, test_dates.py, test_concept.py are written as above file. The expected output is written according to the functionality of that redact_function to the given input and they are compared to give the test results.

**test_phones.py** examples is as below:
~~~
import pytest

from project1.main import redact_phones

testdata = [
    ("My Phone no. is +1(469)604-6217, +919553340279", "My Phone no. is ███████████████, █████████████", 2)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = redact_phones(input)
    print(actual_text)

    assert actual_text == expected_text
    assert len(word_list) == expected_count
~~~


## 4. Assumptions/Bugs
- Few names which matches with english language Adjectives or nouns doesn't get redacted for example in name Christian Varshitha, only Varshitha gets redacted. Jasmine is not considered as name by the nltk module.
- My code can only detect US mailing addresses. Addresses from other countries can't be detected with this code.
- Spacy recognizes absolute or relative dates or periods, so it also recognizes "Early 19's, half a century ago, 2nd semester, ago 20, age 19"  also as dates and redacted them. 
- Few surnames are not getting redacted. Few names are not getting redacted, so except this erros in the project.

## **Steps to Run project1**

- **Step1**  
Clone the project directory using below command

~~~json
git clone https://github.com/VarshithaCVasireddy/cs5293sp22-project1
~~~
  
-**Step2**
Run below command to install pipenv
> pip install pipenv
  
- **Step3**  
Navigate to directory that we cloned from git and run the below command to install dependencies

~~~
pipenv install nltk, numpy, commonregex, pyap, pytest
~~~

- **Step4**  
Then run the below command by providing URL
~~~
 pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --genders --address\
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr
~~~
- **Step5** 

Then run the below command to test the testcases. 

> pipenv run python -m pytest -v
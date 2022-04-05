# **cs5293sp22-project1**
# **Author: Varshitha Choudary Vasireddy**


## Setting up the initial installations
Below packages are to be installed in the project's virtual environment to successfully run the project. The below command has to be followed.
~~~
pipenv install nltk, numpy, commonregex, pyap, pytest
~~~

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

## 1. main.py
This file consists of 6 functions. Each function redacts different entities.
### i. redact_names(data)
In this function, the names will be redacted from the data file. By using Nltk the data is word tokenized, then the words are classified into parts of speech and labeling is done, then chuncking is done on the classified data to give chunk tags. Then subtress is selected with label as 'PERSON'.
~~~
def redact_names(data):
    words = nltk.word_tokenize(data)
    tag = nltk.pos_tag(words)
    tree = nltk.ne_chunk(tag)
    names_list = [ent[0][0] for ent in list(tree.subtrees()) if ent.label() in ['PERSON']]
    #names_list = [ent[0][0] for ent in list(tree.subtrees()) if ent.label() in ['PERSON','GPE']]
    for item in names_list:
        data = data.replace(item, '\u2588'* len(item))
    return data, names_list
~~~
This gives names of persons. And the words with the 'PERSON' tag will be redacted by a block character. I am only assuming person's names are to be dedacted from this function, I am not redacting Geopolitical/geographical entities.
This function gives the data that is redacted and the list of names that got redacted.

### ii.redact_dates(data)
This function will redact dates. Used a package called **commonregex** to do this. The data is firstly changed into Regex data and then a method called dates is applied to the data to extract dates.
~~~
    data1 = CommonRegex(data)
    dates_list = data1.dates
    for item in dates_list:
        data = data.replace(item,'\u2588'* len(item))
    return data, dates_list
~~~
the dates gets replaced by block character, impling it will be redacted from the data.  
Data and list of dates that got redacted are returned.

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

### vi. redact_concept(data,concepts)
In this function the whole sentence which contains the concepts argument word will be redacted. Synonyms for the concepts arguments will be taken with the help of **wordnet.synsets(concepts)** and **.name()** for the lemmation will give synonyms list.  
The data is converted into sentences using **sent_tokenize(data)** and then into words. And each word is checked with the synonyms list and if any word is matching the synonym list then the entire sentence of that particular word is replaced by blocked character.
~~~
def redact_concept(data,concepts):
    synonyms = []
    concept_redacted_list = []
    for concept in concepts:
        for syn in wordnet.synsets(concept):
            synonyms += [l.name() for l in syn.lemmas()]
    l = WordNetLemmatizer()
    sentences = sent_tokenize(data)
    for s in sentences:
        tokens = word_tokenize(s)
        tok_lemmas = [l.lemmatize(token) for token in tokens]
        
        for tok_lemma in tok_lemmas:
            if tok_lemma in synonyms:
                concept_redacted_list = concept_redacted_list + [s]
                data = data.replace(s, '\u2588'* len(s))
                continue    
    
    return data, concept_redacted_list
~~~
Data file after redaction and the list of redacted sentences are returned.

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

Firstly 2 empty dictionaries are considered namely "redact_counts" and "redact_list" to count redacted words/sentences for a particular argument and to write the redacted words/sentences data for a particular argument respectively. 
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

raw_file is the input file, and it is split after . and "redacted" is added as extension. if input is given from the subfolders then the output also has to be created in that subfolder so "/" is used for split and then same is done as discussed above.
~~~
out_file_name = '.'.join(raw_file.split('.')[:-1] + ['redacted'])
    sub_folders = out_file_name.split('/')[:-1]
    for sub_folder in sub_folders:
        sub_folder_path = os.path.join(args.output, sub_folder)
        if not os.path.exists(sub_folder_path):
            os.mkdir(sub_folder_path)

    with open(os.path.join(args.output, out_file_name), 'w') as f:
        f.write(data)
~~~

### --stats
If this argument is given then stats file has to be created and it tells on how that stats file has to be displayed or saved into another file by giving the file name. If stdout or stderr is given in argument, then stats file is displayed on console, else stats summary is sent into file where file name is specified in the console.


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
- My code doesn't redact geopolitical/geographical entity names like country names or location names. It also doesn't redact organization names. So if you want even them to be redacted then my code fails.
- My code can only detect US mailing addresses. Addresses from other countries can't be detected with this code.

## **Steps to Run project0**

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
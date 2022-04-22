## File name not re-assigned correctly
File names not re-assigned correctly --- I corrected the code so that the file names are re-assigned correctly.
I rewritten the code as below
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

## Dates redaction
I changed the redacting dates functions. I now used spacy to redact dates.
I also included regex equation inorder to pull all dates which will not detected by spacy
~~~
def redact_dates(data):
    data1 = nlp(data)
    dates_ent_list = []
    for i in [ent.text.split('\n') for ent in data1.ents if ent.label_ == "DATE"]:
        for j in i:
            dates_ent_list.append(j)
    pattern = r'(\d{1,4}/\d{1,2}/\d{1,4})'
    dates_re_list = re.findall(pattern,data)
    dates_list = set(dates_ent_list + dates_re_list)
    list_to_excluded = ["day", "tomorrow","yesterday","today","Day","Today","Tomorrow"]
    for i in list_to_excluded:
        if i in dates_list:
            dates_list.remove(i)
    for items in dates_list:
        data = data.replace(items,'\u2588'* len(items))
    return data,dates_list
~~~
I am first converting the data into nlp and creating a list called "dates_ent_list" when labels are "DATE". A pattern of regex expression which matches dates in the format "yyyy/mm/dd" or "dd/mm/yyyy" is written i.e **'(\d{1,4}/\d{1,2}/\d{1,4})'** and the data is checked with that pattern and a new list called **dates_re_list**.
The lists are then added and in order to avoid duplicates "set" datatype is used and then set is iterated and each element of set is redacted.
Words like "day, tomorrow and yesterday" are also getting recognized by spacy as "dates" so I removed them from the set and then redacted the remaining recognized dates


## Assumptions:
Spacy recognizes absolute or relative dates or periods, so it also recognizes "Early 19's, half a century ago, 2nd semester, ago 20, age 19, etc"  also as dates and redactes them.

## Results of changes
Output files not stored in respective folder --- I corrected the code so the files are outputed and correctly saved in the output folder.
Since the files are not saved correctly you were not able to see the results properly, but with proper saving of the output, will enable you to see the results as expected.

## **Steps to Run project1**

- **Step1**  
Clone the project directory using below command

~~~json
git clone https://github.com/VarshithaCVasireddy/cs5293sp22-project1
~~~
- **Step2**
Navigate to directory that we cloned from git and run the below command to install dependencies

~~~
pipenv install
~~~

- **Step3**  
Then run the below command by providing URL
~~~
 pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --genders --address\
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr
~~~
- **Step4** 

Then run the below command to test the testcases. 
~~~
pipenv run python -m pytest -v
~~~
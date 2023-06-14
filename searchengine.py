"""
File: searchengine.py
---------------------
File to implement a search engine that looks for terms in a list of files
To run it use py searchengine.py folder -s
The user specify the argumens: 
       # folder with the text files where to look 'folder'
       # -s indicates that wants to do a search (optional)
When -s is included as argument, the program as the user for a 'query' to search for
   # If the query is lowercase string with no punctuation at the begining or end: 
       the program returns a list of files where the terms of the query were found
       and ask for a new query
   # If the query is empty: the program stops

"""


import os
import sys
import string


def create_index(filenames, index, file_titles):
    """
    This function is passed:
        filenames:      a list of file names (strings)

        index:          a dictionary mapping from terms to file names (i.e., inverted index)
                        (term -> list of file names that contain that term)

        file_titles:    a dictionary mapping from a file names to the title of the article
                        in a given file
                        (file name -> title of article in that file)

    The function will update the index passed in to include the terms in the files
    in the list filenames.  Also, the file_titles dictionary will be updated to
    include files in the list of filenames.

    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test1.txt'], index, file_titles)
    >>> index
    {'file': ['test1.txt'], '1': ['test1.txt'], 'title': ['test1.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt'], 'carrot': ['test1.txt']}
    >>> file_titles
    {'test1.txt': 'File 1 Title'}
    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test2.txt'], index, file_titles)
    >>> index
    {'file': ['test2.txt'], '2': ['test2.txt'], 'title': ['test2.txt'], 'ball': ['test2.txt'], 'carrot': ['test2.txt'], 'dog': ['test2.txt']}
    >>> file_titles
    {'test2.txt': 'File 2 Title'}
    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test1.txt', 'test2.txt'], index, file_titles)
    >>> index
    {'file': ['test1.txt', 'test2.txt'], '1': ['test1.txt'], 'title': ['test1.txt', 'test2.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt', 'test2.txt'], 'carrot': ['test1.txt', 'test2.txt'], '2': ['test2.txt'], 'dog': ['test2.txt']}
    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test1.txt', 'test2.txt', 'test2.txt'], index, file_titles)
    >>> index
    {'file': ['test1.txt', 'test2.txt'], '1': ['test1.txt'], 'title': ['test1.txt', 'test2.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt', 'test2.txt'], 'carrot': ['test1.txt', 'test2.txt'], '2': ['test2.txt'], 'dog': ['test2.txt']}
    >>> file_titles
    {'test1.txt': 'File 1 Title', 'test2.txt': 'File 2 Title'}
    >>> index = {'file': ['test1.txt'], '1': ['test1.txt'], 'title': ['test1.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt'], 'carrot': ['test1.txt']}
    >>> file_titles = {'test1.txt': 'File 1 Title'}
    >>> create_index([], index, file_titles)
    >>> index
    {'file': ['test1.txt'], '1': ['test1.txt'], 'title': ['test1.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt'], 'carrot': ['test1.txt']}
    >>> file_titles
    {'test1.txt': 'File 1 Title'}
    """
    for i in range(len(filenames)):
        filename = filenames[i]
        # open file
        with open(filename) as f:
            # read first line and add it to file_titles
            first_line = f.readline()
            first_line = first_line.strip()
            first_line = first_line.strip(string.punctuation)
            add_to_index(filename, first_line, index)
            file_titles[filename] = first_line
            for line in f: 
                add_to_index(filename, line, index)
                

        
          
def add_to_index(file_name,line, index):
    '''
    This function strip a text line in terms (string separeted by spaces)
    and add  the term to the index dictionary and the filename were it was found
        # If the term is already in the dictionary it just add the filename, 
        # if the term is repeated in the same file, no modification is made in the
        index dictionary
    file_name : string with the path of the file from where the line was extracted
    line : string with 1 text line
    index : dictionary were the terms and the filename where the terms are found are stored
    
    '''
    # split the text from the file        
    terms_in_line = line.split()
    # remove punctuation 
    format_text(terms_in_line)
    # add to the dictionary
    for i in range(len(terms_in_line)):   
        # check if the therm is in the index dictionary
        if terms_in_line[i]  in index:
            term = terms_in_line[i] 
            # check if the term was already found in this file
            if file_name in index[term]:
                pass
            else:
                index[term].append(file_name)
        else:
            term = terms_in_line[i] 
            index[term] = [file_name]
    
    
def format_text(list_of_terms):
    '''This function delete punctuation symbols from the begining and end of the
    terms and change upercase for lowercase
    input: list of strings
    '''
    for i in range(len(list_of_terms)):
        list_of_terms[i] = list_of_terms[i].strip(string.punctuation)
    # remove empty strings from the list
    while '' in list_of_terms:
        list_of_terms.remove('')
        # transform to lowercase
    for i in range(len(list_of_terms)):
        list_of_terms[i] = list_of_terms[i].lower()
    

def search(index, query):
    """
    This function is passed:
        index:      a dictionary mapping from terms to file names (inverted index)
                    (term -> list of file names that contain that term)

        query  :    a query (string), where any letters will be lowercase

    The function returns a list of the names of all the files that contain *all* of the
    terms in the query (using the index passed in).

    >>> index = {}
    >>> create_index(['test1.txt', 'test2.txt'], index, {})
    >>> search(index, 'apple')
    ['test1.txt']
    >>> search(index, 'ball')
    ['test1.txt', 'test2.txt']
    >>> search(index, 'file')
    ['test1.txt', 'test2.txt']
    >>> search(index, '2')
    ['test2.txt']
    >>> search(index, 'carrot')
    ['test1.txt', 'test2.txt']
    >>> search(index, 'dog')
    ['test2.txt']
    >>> search(index, 'nope')
    []
    >>> search(index, 'apple carrot')
    ['test1.txt']
    >>> search(index, 'apple ball file')
    ['test1.txt']
    >>> search(index, 'apple ball nope')
    []
    """
    # create a list of terms from the query
    terms_in_query = query.split()
    num_terms = len(terms_in_query)
    # for each term, check in the index in which files is found
    # save it in a dictionary
    found_terms = {}
    for i in range(num_terms):
       found_terms[terms_in_query[i]] = check_in_index(terms_in_query[i], index)
    list_of_files = found_terms[terms_in_query[0]]
    # check overlapping 
    for i in range(len(found_terms)):
        list_of_files = common(list_of_files, found_terms[terms_in_query[i]])
    return list_of_files
    

def common(list1, list2):
    """
    This function is passed two lists and returns a new list containing
    those elements that appear in both of the lists passed in.
    >>> common(['a'], ['a'])
    ['a']
    >>> common(['a', 'b', 'c'], ['x', 'a', 'z', 'c'])
    ['a', 'c']
    >>> common(['a', 'b', 'c'], ['x', 'y', 'z'])
    []
    >>> common(['a', 'a', 'b'], ['a', 'a', 'x'])
    ['a']
    """
    result_list = []
    for element in list1:
        if (element in list2) and element not in result_list:
            result_list.append(element)
    return result_list

def check_in_index(term, index):
    ''' 
    This function check if a term is stored in the index dictionary.
    if the term is in index, return a list of files were the term is found
    inputs:
        term: one term string
        index: dictionary were each term is a key associated to a list of
        strings that indicate the files were the term is found
    '''
    if term in index:
        term_location = index[term]
        return term_location
    else:
        return []
        


##### YOU SHOULD NOT NEED TO MODIFY ANY CODE BELOW THIS LINE (UNLESS YOU'RE ADDING EXTENSIONS) #####


def do_searches(index, file_titles):
    """
    This function is given an inverted index and a dictionary mapping from
    file names to the titles of articles in those files.  It allows the user
    to run searches against the data in that index.
    """
    while True:
        query = input("Query (empty query to stop): ")
        query = query.lower()                   # convert query to lowercase
        if query == '':
            break
        results = search(index, query)

        # display query results
        print("Results for query '" + query + "':")
        if results:                             # check for non-empty results list
            for i in range(len(results)):
                title = file_titles[results[i]]
                print(str(i + 1) + ".  Title: " + title + ",  File: " + results[i])
        else:
            print("No results match that query.")


def textfiles_in_dir(directory):
    """
    DO NOT MODIFY
    Given the name of a valid directory, returns a list of the .txt
    file names within it.

    Input:
        directory (string): name of directory
    Returns:
        list of (string) names of .txt files in directory
    """
    filenames = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filenames.append(os.path.join(directory, filename))

    return filenames


def main():
    """
    Usage: searchengine.py <file directory> -s
    The first argument specified should be the directory of text files that
    will be indexed/searched.  If the parameter -s is provided, then the
    user can interactively search (using the index).  Otherwise (if -s is
    not included), the index and the dictionary mapping file names to article
    titles are just printed on the console.
    """
    
    # Get command line arguments
    args = sys.argv[1:]  # uncoment at the end
    #args = ['.\small' , '-s']  # added to test in spyder. comment at the end

    num_args = len(args)
    if num_args < 1 or num_args > 2:
        print('Please specify directory of files to index as first argument.')
        print('Add -s to also search (otherwise, index and file titles will just be printed).')
    else:
        # args[0] should be the folder containing all the files to index/search.
        directory = args[0]
        if os.path.exists(directory):
            # Build index from files in the given directory
            files = textfiles_in_dir(directory)
            index = {}          # index is empty to start
            file_titles = {}    # mapping of file names to article titles is empty to start
            create_index(files, index, file_titles)

            # Either allow the user to search using the index, or just print the index
            if num_args == 2 and args[1] == '-s':
                do_searches(index, file_titles)
            else:
                print('Index:')
                print(index)
                print('File names -> document titles:')
                print(file_titles)
        else:
            print('Directory "' + directory + '" does not exist.')


if __name__ == '__main__':
    main()

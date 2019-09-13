#*****************************************************************************
#       Copyright (C) 2010 Jonathan Hanke
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#
###############################################################################################################
##
## Package Description:
##     Some classes and routines for encoding/decoding text to/from numbers, 
##     computing letter statistics, and applying some classical ciphers. 
##
## Instructions:  
##     To use these, put them in the directory you run Sage from and use: 
##
##         load "crypto.sage" 
##
##     at the Sage prompt.  To find the current directory, you can type 'pwd' at Sage the prompt.
##
## TO DO:
##     - Add some classical cipher decryption tools (n-graph stats, kasiski, known keysize, genetic algorithms)
##     - Letter statistics attacks
##     - Known plaintext attacks, possibly with known dictionaries
##     - Add Vigenere, OTP, Playfair, LFSR boxes, ENIGMA
##
###############################################################################################################



def letter_stats(input_text, fragment_length=1, starts_with="", ends_with="", show_at_most=None):
    """
    Computes the letter statistics for text fragments of size
    fragment_length within the given input text string.  All 
    text is converted to uppercase, and all non-alphabetic 
    characters (including punctuation and spaces) are removed.

    The default fragment length is 1, which counts single letters.
    If strings for starts_with and ends_with are specified, then the
    counts are restricted fragments which start and end with these.  
    If show_at_most is specified, then only that many fragments 
    will be printed (but all fragments will be returned).  The 
    default is to show all fragments.  To silence the printed 
    output, use show_at_most=0.

    INPUT:
        input_text -- a string
	fragment_length -- an integer >= 1
	starts_with, ends_with -- a string
	show_at_most -- None or an integer >=0 

    OUTPUT:
	a list of two element lists of the form [string, number] 
	which says (in decreasing order) how many times that string 
	appeared in the text, subject to the specified constraints.

    EXAMPLES:
	sage:  T = "Hello. My Name is Inigo Monotoya. You killed my father. Prepare to die."
        sage: T1 = letter_stats(T)
	E -- 7 -- 12.7%
	O -- 7 -- 12.7%
	I -- 5 -- 9.1%
	A -- 4 -- 7.3%
	M -- 4 -- 7.3%
	L -- 4 -- 7.3%
	Y -- 4 -- 7.3%
	N -- 3 -- 5.5%
	R -- 3 -- 5.5%
	T -- 3 -- 5.5%
	D -- 2 -- 3.6%
	H -- 2 -- 3.6%
	P -- 2 -- 3.6%
	G -- 1 -- 1.8%
	F -- 1 -- 1.8%
	K -- 1 -- 1.8%
	S -- 1 -- 1.8%
	U -- 1 -- 1.8%
	sage: len(T1)
	18

	sage: T1__4 = letter_stats(T, show_at_most=4)
	E -- 7 -- 12.7%
	O -- 7 -- 12.7%
	I -- 5 -- 9.1%
	A -- 4 -- 7.3%
	sage: T1__4
	[['E', 7],
	 ['O', 7],
	 ['I', 5],
	 ['A', 4],
	 ['M', 4],
	 ['L', 4],
	 ['Y', 4],
	 ['N', 3],
	 ['R', 3],
	 ['T', 3],
	 ['D', 2],
	 ['H', 2],
	 ['P', 2],
	 ['G', 1],
	 ['F', 1],
	 ['K', 1],
	 ['S', 1],
	 ['U', 1]]


	sage: T2 = letter_stats(T, 2, starts_with="E")
	EL -- 1 -- 16.7%
	EI -- 1 -- 16.7%
	ED -- 1 -- 16.7%
	ET -- 1 -- 16.7%
	EP -- 1 -- 16.7%
	ER -- 1 -- 16.7%
	sage: T2
	[['EL', 1], ['EI', 1], ['ED', 1], ['ET', 1], ['EP', 1], ['ER', 1]]

	sage: T2 = letter_stats(T, 2, ends_with="E")
	RE -- 2 -- 28.6%
	HE -- 2 -- 28.6%
	ME -- 1 -- 14.3%
	LE -- 1 -- 14.3%
	IE -- 1 -- 14.3%
	sage: T2
	[['RE', 2], ['HE', 2], ['ME', 1], ['LE', 1], ['IE', 1]]


	sage: T2 = letter_stats(T, 2, starts_with="E", ends_with="E")
	sage: T2 = letter_stats(T, 2, starts_with="L", ends_with="L")
	LL -- 2 -- 100.0%

    """
    ## If the text passed is a valid filename, load text from the file
    import os.path 
    if os.path.isfile(input_text):
        new_file = open(input_text, "r")
        text = new_file.read()
        new_file.close()
    else:
        text = input_text



    ## Initialize the count dictionary
    count_dictionary = {}
    N = fragment_length

    ## Clean the text to remove all non-alphabet 
    ## characters and capitalize the others
    clean_text = ""
    for i in range(len(text)):
        if text[i].isalpha():
            clean_text += text[i].upper()

    ## Clean the message fragments
    starts_with_caps = starts_with.upper()
    ends_with_caps = ends_with.upper()

    ## Count the fragments
    total = 0
    for i in range(len(clean_text) - N + 1):
        tmp_key = clean_text[i:i+N]
        if tmp_key.startswith(starts_with_caps) \
                and tmp_key.endswith(ends_with_caps):
            try:
                count_dictionary[tmp_key] += 1
            except:
                count_dictionary[tmp_key] = 1    
            total += 1


    ## Make a sorted list of statistics
    L = [[k, count_dictionary[k]]  for k in count_dictionary.keys()]
    import operator
    L1 = sorted(L, key=operator.itemgetter(1), reverse=True)
    

    ## Decide how many results to print
    if show_at_most == None:
        show_range = range(len(L1))
    else:
        show_range = range(min(len(L1), show_at_most))


    ## Print the totals and percentages
    for i in show_range:
        print L1[i][0] + " -- " + str(L1[i][1]) + " -- " + str(round(100.0 * L1[i][1] / total, 1)) + "%"

    ## Return the dictionary
    return L1







class CodeForAlphabet(SageObject):
    """
    A code which translates from tuples of characters
    in a given alphabet to numbers.
    """

    def __init__(self, alphabet_string, word_length=1):
        """
        If word_length=1, each character of alphabet_string gets encoded to its index in the string.


	Takes a string of characters, and matches each word 
	(of the specified word length) to a given number.  
	We start with 


	EXAMPLES:
	    sage: C = code("ABCDE")
	    sage: C
	    A code of word length 1 based on the string: ABCDE
	
	    sage: C.encode("AAABCEE")
            [0, 0, 0, 1, 2, 4, 4]

	    sage: C.decode(C.encode("AAABCEE"))
	    'AAABCEE'

        """
        self.__codeword_length = word_length
        self.__alphabet_string = alphabet_string
        
        #print self.__codeword_length
        #print self.__alphabet_string

        ## TO DO: Check that there are no repeated characters in the defining string!

    
    def __repr__(self):
        return "A code of word length " + str(self.__codeword_length) + " based on the string: " + self.__alphabet_string 



    def encode(self, text_str):
        """
        Use the code to translate text_str from letters to a list of numbers.
        """
        if self.__codeword_length != 1:
            raise NotImplementedError, "Need to add support for word length > 1."

        num_list = []
        for i in range(len(text_str)):
            num_list.append(self.__alphabet_string.index(text_str[i]))
        return num_list


    def decode(self, num_list):
        """
        Use the code to translate num_list from numbers to letters.
        """
        if self.__codeword_length != 1:
            raise NotImplementedError, "Need to add support for word length > 1."

        new_string = ""
        for i in range(len(num_list)):
            new_string += self.__alphabet_string[num_list[i]]
        return new_string








class HillCipher(SageObject):
    """
    Apply the Hill cipher given by left multiplication of column 
    vectors by an n x n matrix over Z/NZ.

    EXAMPLES:
        sage: A = Matrix(ZZ, 2, 2, [1, 2, 3, 4])
	sage: H = HillCipher(A, 3)
	sage: PT = [0, 0, 0, 1, 1, 1, 2, 2]
	sage: CT = H.encrypt(PT); CT
	[0, 0, 2, 1, 0, 1, 0, 2]
	sage: H.decrypt(CT) == PT
	True
	sage: H.encryption_key()
	[1 2]
	[0 1]
	sage: H.decryption_key()
	[1 1]
	[0 1]
	sage: H.modulus()
	3
	sage: H.block_size()
	2


	sage: A3 = Matrix(IntegerModRing(3), 2, 2, [1, 2, 3, 4])
	sage: H3 = HillCipher(A3)
	sage: PT = [0, 0, 0, 1, 1, 1, 2, 2]
	sage: CT = H3.encrypt(PT); CT
	[0, 0, 2, 1, 0, 1, 0, 2]
	sage: H3.decrypt(CT) == PT
	True

    """

    def __init__(self, arg1, arg2=None, pass_decryption_key=False):
        """
	Define a Hill Cipher using either a square (encryption)
	matrix over ZZ and a modulus, or an (encryption) matrix 
	over Z/NZ.
        """
	## Initialize from a square (encryption) matrix over Z/NZ
	if arg2 == None:
	    N = arg1.base_ring().characteristic()
	    if N == 0:
	        raise TypeError, "The matrix is not defined over a finite ring, but no modulus is specified."

	    mod_matrix = arg1

	## Initialize from a square matrix over ZZ and a modulus
	else:
	    N = arg2
	    mod_matrix = arg1.base_extend(IntegerModRing(N))
	    

	## Check that the encryption matrix is invertible, and find its inverse
	try:
	    mod_matrix_inv = mod_matrix.inverse()
	except:
	    raise RuntimeError, "Cannot find the inverse of the matrix ", mod_matrix_inv


	## Store the keys and modulus
	if pass_decryption_key == False:
	    self.__encryption_matrix = mod_matrix
	    self.__decryption_matrix = mod_matrix_inv
       	    self.__modulus = N
	else:
	    self.__encryption_matrix = mod_matrix_inv
	    self.__decryption_matrix = mod_matrix
       	    self.__modulus = N
	


    def  __repr__(self):
        n = str(self.block_size())
        N = str(self.__modulus)
        return "The Hill cipher given by (left) matrix multiplication by a matrix in GL_" + n + "(Z/" + N + ")."



    def modulus(self):
	return deepcopy(self.__modulus)


    def block_size(self):
	return self.__encryption_matrix.nrows()


    def encryption_key(self):
	return deepcopy(self.__encryption_matrix)


    def decryption_key(self):
	return deepcopy(self.__decryption_matrix)



    def encrypt(self, plaintext_num_list, padding_char=""):
        """
        Encrypt the plaintext.
        """
	return self.__apply_Hill_matrix__(self.__encryption_matrix, plaintext_num_list, padding_char="")


    def decrypt(self, ciphertext_num_list, padding_char=""):
	"""
	Decrypt the Ciphertext with the decryption key.
	"""
	return self.__apply_Hill_matrix__(self.__decryption_matrix, ciphertext_num_list, padding_char="")



    def __apply_Hill_matrix__(self, key_matrix, plaintext_num_list, padding_char=""):
        """
        Encrypt the given text by left-multiplying by the key_matrix.
        """
        n = self.block_size()
        N = self.__modulus


        R = IntegerModRing(N)
        MS = MatrixSpace(R, n, n) 
        A = MS(key_matrix)

        CT_num_list = []
        for word_index in range(0, len(plaintext_num_list), n):
            PT_word = plaintext_num_list[word_index: word_index + n]

            if len(PT_word) != n:
                if len(padding_char) != 1:
                    raise RuntimeError, "Additional padding is needed for the word: " + str(PT_word) + "."
                else:
                    PT_word += (n - len(PT_word)) * padding_char

            

            CT_word_mod = A * vector(PT_word) 
            CT_num_list += [c.lift() for c in CT_word_mod]


        return CT_num_list






def PermutationCipher(key_list, plaintext, padding_char="X"):
    """
    Apply a permutation given by a list reordering of the numbers 0 through n-1.

    EXAMPLES:
        sage: perm_key = [2, 1, 0]
	sage: PermutationCipher(perm_key, "HelloThere")
	'leHTolrehXXe'


    TO DO:
	- Write this as a class.
        - Make this into something that takes a permutation as well.

    """
    n = len(key_list)
    CT_str = ""
    for word_index in range(0, len(plaintext), n):
        PT_word = plaintext[word_index: word_index + n]
        
        if len(PT_word) != n:
            if len(padding_char) != 1:
                raise RuntimeError, "Additional padding is needed for the word: " + str(PT_word) + "."
            else:
                PT_word += (n - len(PT_word)) * padding_char

        CT_word = ""
        PT_word_list = list(PT_word)
        for i in range(n):
            CT_word += PT_word[key_list[i]]

        CT_str += CT_word


    return CT_str







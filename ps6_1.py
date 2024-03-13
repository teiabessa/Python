import string

### DO NOT MODIFY THIS FUNCTION ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

### DO NOT MODIFY THIS FUNCTION ###
def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\'")
    return word in word_list

### DO NOT MODIFY THIS FUNCTION ###
def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    ### DO NOT MODIFY THIS METHOD ###
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        """
        Creates a dictionary that maps each letter to its shifted counterpart.

        Args:
            shift (int): The amount by which to shift each letter.

        Returns:
            dict: A dictionary mapping a letter (string) to another letter (string).
        """
        import string
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase

        shift_dict = {}
        #print("message",self.message_text)
        for char in lowercase_letters:            
            #print("build shift:",self.shift_letter(char, shift))
            shifted_char = self.shift_letter(char, shift)
            shift_dict[char] = shifted_char

        for char in uppercase_letters:
            shifted_char = self.shift_letter(char, shift)
            shift_dict[char] = shifted_char

        #print("shift_dict=",shift_dict) 
        return shift_dict

    def shift_letter(self, char, shift):
        """
        Shifts a single letter by the specified amount.

        Args:
            char (str): The letter to be shifted.
            shift (int): The amount by which to shift the letter.

        Returns:
            str: The shifted letter.
        """
        if char.isalpha():
            is_uppercase = char.isupper()          
            char = char.lower()
            shifted_index = (ord(char) - ord('a') + shift) % 26          
            shifted_char = chr(shifted_index + ord('a'))
            #print(shifted_char)
            return shifted_char.upper() if is_uppercase else shifted_char
        else:
            return char
       
    def apply_shift(self, shift):
        """
        Applies the Caesar Cipher to self.message_text with the input shift.

        Args:
            shift (int): The shift with which to encrypt the message.

        Returns:
            str: The encrypted message.
        """
        shift_dict = self.build_shift_dict(shift)
        encrypted_message = ""
        for char in self.message_text:
            if char.isalpha():
                encrypted_message += shift_dict.get(char, char)
            else:
                encrypted_message += char
        return encrypted_message

class PlaintextMessage(Message):
    def __init__(self, text, shift):
  
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less 
        code is repeated
        '''
           # Call the parent class constructor
        Message.__init__(self, text)
       
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
         '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
         return self.shift

    def get_encrypting_dict(self):
        #Return a copy of the encrypting_dict to prevent mutation of the original dictionary.
        return self.encrypting_dict.copy()
    
          

    '''
    def get_message_text_encrypted(self):
        encrypted_text = ""
        for char in self.text:
            if char.isalpha():
                encrypted_char = self.encrypting_dict[char]
                encrypted_text += encrypted_char
            else:
                encrypted_text += char
        return encrypted_text
    '''


    
    def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class
        
        Returns: a COPY of self.encrypting_dict
        '''
        return self.encrypting_dict.copy()
    
    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.apply_shift(self.shift)
    

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        pass #delete this line and replace with your code here

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        pass #delete this line and replace with your code here

#Example test case (PlaintextMessage)
plaintext = PlaintextMessage('hello', 2)
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.get_message_text_encrypted())
    
#Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq')
print('Expected Output:', (24, 'hello'))
print('Actual Output:', ciphertext.decrypt_message())

message_text = "Hello, World!"
message = Message(message_text)
shift = 3
encrypted_message = message.apply_shift(shift)

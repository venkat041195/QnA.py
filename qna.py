import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
import wikipedia
import re
from nltk.chunk import tree2conlltags
from nltk.corpus import stopwords


question= input("This is a QA system by YourName. It will try to answer questions that start with Who, What, When or Where. Enter 'exit' to leave the program.")

def main():
    question_tokens=word_tokenize(question)
    stop_words = set(stopwords.words('english')) 
    final_question=[]
    fin_question=[]
    other_stop_words=['?', '!']
    for w in question_tokens:
        if w not in stop_words:
            final_question.append(w)
    for x in final_question:
        if x not in other_stop_words:
            fin_question.append(x)       
    ne_tree = tree2conlltags(ne_chunk(pos_tag(word_tokenize(question))))
    print(ne_tree)
    if 'born' in question_tokens:
        if 'when' in question_tokens:    
            if 'B-PERSON' or 'I-PERSON' in ne_tree[2]:
                person=person_name(question)
                dob=date_of_birth(person)
                print(person[1] + ' was born on ' + dob[0])
        else:
            print("I am sorry, I don't know the answer.")
            
    elif 'what' in question_tokens:
        if 'B-PERSON' or 'I-PERSON' in ne_tree[2]:
            print("I am sorry, I don't know the answer.")
        else:    
            info=info_objects(fin_question)
            print(fin_question[0] + ' ' + info)
        
    elif 'who'  in question_tokens:
        if 'B-PERSON' or 'I-PERSON' in ne_tree[2]:
             person=person_name(question)
             person_full_name=person[1]
             p_info=person_info(person_full_name)
             print(person_full_name + ' ' + p_info)
        else:
          print("I am sorry, I don't know the answer.")   
    
    elif 'where'  in question_tokens:
        if 'B-GPE' in ne_tree[2]:
            info=info_objects(fin_question)
            print(fin_question[0] + ' ' + info)
        
        elif 'B-PERSON' or 'I-PERSON' in ne_tree[2]: 
            print("I am sorry, I don't know the answer") 

            
    else:
        print("I am sorry, I don't know the answer")    

def person_name(question):
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(question))):
        if hasattr(chunk, 'label'):
            full_name=chunk.label(), ' '.join(c[0] for c in chunk)
    
    return full_name   

def date_of_birth(person):
    page = wikipedia.page(person)
    date = re.findall(r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4}", page.content)
    if len(date)==0:
        date = re.findall(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}", page.content)
    return date

def info_objects(fin_question):
    wikidata=wikipedia.summary(fin_question)
    info=re.findall(r'\bis [^.]*',wikidata)[0]
    return info

def person_info(person_full_name):
    wikidata=wikipedia.page(person_full_name)
    
    personal_info=re.findall(r'(?<=\d\d\d\d\))[^.]+',wikidata.content)[0]
    return personal_info

  
main()

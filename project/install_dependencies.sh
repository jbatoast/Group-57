#Installs all dependencies for the CS132 project. Assumes that Python is installed.

python -m ensurepip --upgrade
pip install -U pandas numpy matplotlib snscrape spacy nltk gensim wordcloud pyLDAvis 
python -m spacy download en_core_web_sm
read -p "Press any key to continue"
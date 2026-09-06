from bs4 import BeautifulSoup

soup = BeautifulSoup(open('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_3.html', 'r', encoding='utf-8').read(), 'html.parser')
c5 = soup.find(id='ex5-l3-card')
c6 = soup.find(id='ex6-l3-card')

print("c5 parent:", c5.parent.name, c5.parent.get('class'))
print("c5 parent parent:", c5.parent.parent.name, c5.parent.parent.get('class'))
print("c6 parent:", c6.parent.name, c6.parent.get('class'))

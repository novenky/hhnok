import re
from collections import Counter
from datetime import datetime,timedelta

pattern0 = re.compile('(N)?OK')
pattern1 = re.compile('NOK')
pattern2 = re.compile('[12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])(\s)*([01][0-9]|2[0-3]):[0-5]\d')

# на вход лист с датами, на выход первое и последнее время логфайла в виде тапла. 
def take_start_and_end_time(l:list[str])->(str,str):
    return (" ".join(f3(l[0]).split())," ".join(f3(l[-1]).split()))

# функция удаляет лишние пробелы   
def remove_empty_spaces(s:list[str])->list[str]: 
    return [" ".join(i.split()) for i in s]

#функция форматирует строку по регулярке pattern2 см. выше
def f3(x:str)->str:
    return pattern2.search(x)[0]

#на вход поступют строки со временем начала в тексте лог файла и временем, когда логфайл закончил записываться, а на выход словарик
# с ключами в виде ДатаВремя интервал минута и значением NOK раным нулю
def dict_producer(ss:str,se:str)->dict[str,int]:
    start = datetime.strptime(ss, '%Y-%m-%d %H:%M')
    end = datetime.strptime(se, '%Y-%m-%d %H:%M')
    date_generated = [start + timedelta(minutes=x) for x in range(0, int((end-start).total_seconds()/60)+1)]
    d={} 
    for date in date_generated:
        d[(date.strftime("%Y-%m-%d %H:%M"))]=0
#    print(d)
    return d   

#читаем логфайл целиком
with open('events.log') as f:
    lines = [i for i in f.readlines() if bool(pattern0.search(i))]

#формируем хорошо отформатированный лист убирая лишние пробелы, пустые строки etc   
filtered_list = list(map(f3,(filter(lambda e:bool(pattern1.search(e)),lines))))    

#формируем два словарика- один от начального времени записи логфайла до конечного с интервалом
#минута в виде ключа и нулевым значение для каждого ключа, а второй со временем, когда
#были ненулевые NOK в качестве ключа и  количества NOK в эту минуту и далее объединяем эти
#словари и печатаем
ko1=dict(Counter(remove_empty_spaces(filtered_list)))
ko2=dict_producer(take_start_and_end_time(lines)[0],take_start_and_end_time(lines)[1])
#ko2|ko1
#print(ko1)
print({**ko2,**ko1})




import bank

conn = bank.Connector('localhost', user='user', passwd='password', db='init')

print ("**************** print all persons in database****************")
# perform query and get results
result = conn.query('SELECT * FROM person')
for item in result:
  person = item.wrap(bank.Person)
  print("Hi my name is {0.name} with {0.person_id}".format(person))

print ("\n**************** print person that has id = 1 ****************")
# retrieves the person SQL table that has id 1
result = conn.query("select * from person where person_id = 1");
first = list(result)[0]
person1 = first.wrap(bank.Person);
print ("Person 1 has id {0.person_id} and has name {0.name}".format(person1));

import inspect
import MySQLdb as mysql

class Result:
  def __init__(self, data):
    self.__dict__ = data

  def wrap(self, instance):
    """
    Wrap attributes into
    custom class instance
    """
    if not inspect.isclass(instance):
      raise AttributeError("Instance is not a class!")
    wrapper = instance()
    for attr in self.__dict__:
      if hasattr(self, attr) and hasattr(wrapper, attr):
        setattr(wrapper, attr, getattr(self, attr, None))
    return wrapper

  @staticmethod
  def AttrPropery(name, _type):
    """ Generate getter/setter for type """
    def getter(self):
      return getattr(self, '__' + name)
    def setter(self, value):
      setattr(self, '__' + name, _type(value))
    return property(getter, setter)

  @staticmethod
  def Object(instance):
    """ Make class instance Result force types """
    new_dict = {}
    for key, value in instance.__dict__.items():
      if isinstance(value, type):
        new_dict['__' + key] = None
        value = Result.AttrPropery(key, value)
      new_dict[key] = value
    new_dict['__dict__'] = new_dict
    return type(instance) \
      (instance.__name__, instance.__bases__, new_dict)

class Connector:
  def __init__(self, host=None, user=None, passwd=None, db=None):
    """ setup config and connect to database """
    self.config = {'host':host, 'user':user, 'pass':passwd, 'db':db}
    for field in self.config:
      if field is None:
        raise ValueError("{} is empty!".format(field))
    self.closed = True
    self.conn = mysql.connect(
      host=host, user=user, passwd=passwd, db=db)
    self.cursor = self.conn.cursor()
    self.closed = False

  def close(self):
    """ Close the database connection """
    if not self.closed:
      if self.cursor is not None:
        self.cursor.close()
        self.cursor = None
      if self.conn is not None:
        self.conn.close()
        self.conn = None
      self.closed = True

  def query(self, query, *args):
    """
    Perform an sql query
    and return results as generator
    """
    # convert arguments to tuple if not
    args = (args,) if len(args) > 1 else args
    # add arguments to query
    query = (query,) + (args if len(args) > 0 else ())
    # execute command and gather results
    self.cursor.execute(*query)

    # iterate through the fond results
    for i in range(self.cursor.rowcount):
      row    = self.cursor.fetchone()
      info   = self.cursor.description
      result = {info[x][0]:row[x] for x in range(len(row))}
      yield Result(result)

###############################################
######             Usage                  #####
###############################################

# create the connection
conn = Connector('localhost','root','password', 'test')

# custom class to wrap in
@Result.Object
class Person:
  id = int
  name = str
  balance = float

# perform query and get results
result = conn.query('SELECT * FROM test')
for item in result:
  person = item.wrap(Person)
  print("Hi my name is {0.name} with {0.id} and I have ${0.balance}".format(person))

@Result.Object
class Account:
    id = int
    person_id = int
    type = string

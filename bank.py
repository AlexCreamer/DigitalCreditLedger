import inspect
import logging
import pymysql.cursors

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
    self.conn = pymysql.connect(
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
      """ Perform an sql query and return results as generator """

      # unpack arguments into a single tuple
      if len(args) == 1 and isinstance(args[0], tuple):
          args = args[0]
      args = [(a,) if not isinstance(a, tuple) else a for a in args]
      args = tuple([arg for a in args for arg in a])

      # combine query with arguments tuple
      query = (query,) + ((args,) if len(args) > 0 else ())

      # execute command and get column names
      self.cursor.execute(*query)
      info = self.cursor.description

      # yield fetched results one by one
      for _ in range(self.cursor.rowcount):
          row = self.cursor.fetchone()
          result = {info[i][0] : row[i] for i in range(len(row))}
          yield Result(result)

# create the connection
conn = Connector('localhost', user='user', passwd='password', db='init')

# custom class to wrap in
@Result.Object
class Person:
  person_id = int
  name = str
  account_id = int

@Result.Object
class Account:
    account_id = int
    acount_type = str
    person_id = int
    balance = int

    def transfer(from_account_id, to_account_id, amount):
        from_amount = get_balance(from_account_id)
        to_amount = get_balance(to_account_id)

        if from_amount - amount <= 0:
            if logger.isEnabledFor(logging.INFO):
                logging.info(
                "Unable to withdraw from database with account id " +
                from_account_id + " due to insufficient funds");
            return False

        else:
            update_balance(from_account_id, from_account - amount)
            update_balance(to_account_id, to_amount + amount)
            return True

    def transfer_to_other(self, other_account_id, amount):
        if transfer(self.account_id, other_account_id, amount):
            self.amount = self.amount - amount
            return True
        return False

    def transfer_from_other(self, from_account_id, amount):
        if transfer(from_account_id, self.account_id, amount):
            self.amount = self.amount + amount
            return True
        return False

    def put(self, amount):
        self.amount = self.get_self_balance()
        self.update_balance(self.account_id, amount)

    def take(self, amount):
        self.amount = self.get_self_balance()

        ##Check if the account transfering from has sufficient funds
        if self_amount <= 0:
            if logger.isEnabledFor(logging.INFO):
                logging.info(
                "Unable to withdraw from database with account id " +
                self.account_id + " due to insufficient funds");

    # Get the balance of the current account
    def get_self_balance(self):
        query_str = 'SELECT balance FROM account where account_id=%s';
        result = conn.query(query_str, self.account_id)
        return next(result).balance

    # Gets the balance of the account transfering funds from
    def get_balance(self, account_id):
        query_str = 'SELECT balance FROM account where account_id=%s';
        result = conn.query(query_str, account_id)
        return next(result).balance

    def update_self_balance(self, amount):
        query_str = "UPDATE account SET balance = %s from account where account_id = %s"
        conn.query(query_str, amount, self.account_id)

    def update_balance(self, account_id, amount):
        query_str = "UPDATE account SET balance = %s from account where account_id = %s"
        conn.query(query_str, amount, account_id)

def deposit(account_id, amount):
    print ("amount %s" % amount)

    query_str = 'SELECT balance FROM account where `account_id`=%s';
    result = conn.query(query_str, account_id)

    balance = next(result).balance
    print ("balance %s" % balance)
    query_str = "UPDATE account SET balance = %s from `account` where `account_id` = %s"
    result = conn.query(query_str, int(balance) + int(amount), account_id)

    print(list(result)[0].__dict__)


def get_balance(account_id):
    query_str = 'SELECT balance FROM account where account_id=%s';
    result = conn.query(query_str, account_id)
    return next(result).balance

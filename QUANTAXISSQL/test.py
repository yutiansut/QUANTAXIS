from QASQL.qasql import Base
test_db_name = 'test_database'

first_record_id = 0
filter_db = Base(test_db_name, save_to_file=False)
filter_db.create('unique_id', 'name', "active", mode="override")
filter_db = filter_db


db = Base('dummy', save_to_file=False)
db.create('name', 'age', 'size')
db.insert(name='homer', age=23, size=1.84)


print(db.get_unique_ids('name'))
print(db.get_unique_ids('age'))
print(db.get_group_count('name'))
print(db.mode)
print(db.get_indices())
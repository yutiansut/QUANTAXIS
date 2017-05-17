from QASQL.qasql import Base
test_db_name = 'test_database'
def setUp(self):  # NOQA
    self.first_record_id = 0
    filter_db = Base(test_db_name, save_to_file=False)
    filter_db.create('unique_id', 'name', "active", mode="override")
    self.filter_db = filter_db
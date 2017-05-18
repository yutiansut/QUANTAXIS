# conversions between PyDbLite and other formats
# currently supported : csv

import os

import QASQL.qasql as qasql


def to_csv(pdl, out=None, write_field_names=True):

    import csv
    if out is None:
        file_name = os.path.splitext(pdl.name)[0] + ".csv"
        out = open(file_name, "wb")
    fields = ["__id__", "__version__"] + pdl.fields
    writer = csv.DictWriter(out, fields)
    # write field names
    if write_field_names:
        writer.writerow(dict([(k, k) for k in fields]))
    # write values
    writer.writerows(pdl())
    return file_name


def from_csv(csvfile, out=None, fieldnames=None, fmtparams=None, conv_func={}, empty_to_none=[]):

    import csv
    import time
    import datetime

    if out is None:
        out = os.path.splitext(csvfile)[0] + ".pdl"

    if fieldnames is None:
        # read field names in the first line of CSV file
        reader = csv.reader(open(csvfile))
        fieldnames = reader.next()

    reader = csv.DictReader(open(csvfile), fieldnames, fmtparams)
    reader.next()  # skip first line

    db = qasql.Base(out)

    conv_func.update({"__id__": int})
    auto_id = "__id__" not in fieldnames
    fieldnames = [f for f in fieldnames if f not in ("__id__")]

    kw = {"mode": "override"}
    db.create(*fieldnames, **kw)
    print(db.fields)

    next_id = 0
    records = {}
    while True:
        try:
            record = reader.next()
        except StopIteration:
            break
        if auto_id:
            record["__id__"] = next_id
            next_id += 1
        # replace empty strings by None
        for field in empty_to_none:
            if not record[field]:
                record[field] = None
        # type conversion
        for field in conv_func:
            if not isinstance(conv_func[field], (tuple, list)):
                record[field] = conv_func[field](record[field])
            else:
                # date or datetime
                date_class, date_fmt = conv_func[field]
                if not record[field]:
                    record[field] = None
                else:
                    time_tuple = time.strptime(record[field], date_fmt)
                    if date_class is datetime.date:
                        time_tuple = time_tuple[:3]
                    record[field] = date_class(*time_tuple)
        records[record["__id__"]] = record
    db.records = records
    db.commit()
    print(len(db))
    return db

if __name__ == "__main__":
    os.chdir(os.path.join(os.getcwd(), 'test'))
    pdl = qasql.Base("test.pdl").open()
    csvfile = to_csv(pdl)
    db = from_csv(csvfile, out="test_copy.pdl")

    ok = nok = 0
    for r1 in pdl:
        try:
            r2 = db[r1["__id__"]]
            ok += 1
        except:
            nok += 1
    print(ok, nok)
    print(r1, r2)
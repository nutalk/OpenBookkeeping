

def trans_data(data: list) -> dict:
    data_rec = {}
    for rec in data:
        type_id, name, amount = rec
        if data_rec.get(type_id) is None:
            data_rec[type_id] = {'amount': amount, 'recs': [rec]}
        else:
            data_rec[type_id]['amount'] += amount
            data_rec[type_id]['recs'].append(rec)
    return data_rec


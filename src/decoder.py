def decode_trace(cover, dictionary):
    po = PartialOrder()
    for pid in cover:
        po.merge(dictionary[pid])
    return po


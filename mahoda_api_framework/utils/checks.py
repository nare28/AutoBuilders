def hasAllFields(metadata, fields):
    if metadata is not None:
        for ele in fields:
            if ele not in metadata:
                print("Field :%s not found" %(ele))
                return False
        return True
    else:
        return False

def checkAllFields(metadata, fields):
    if metadata is not None and len(metadata) > 0:
        miss_fileds = ''
        for ele in fields:
            if ele not in metadata:
                print("Field :%s not found" %(ele))
                miss_fileds = miss_fileds + ele + ", "
        return miss_fileds
    else:
        return "All Fieeds"

def hasAnyFields(metadata, fields):
    if metadata is not None:
        for ele in fields:
            if ele in metadata:
                return True
    return False

def testHasAllFields():
    metadata = {"a1":"1111", "a2":"2222", "a3":"3333"}
    print(hasAllFields(metadata, ["a1", "a2", "a3"]))
    print(hasAllFields(metadata, ["a1", "a4", "a3"]))
    print(hasAnyFields(metadata, ["a1", "a2" ]))


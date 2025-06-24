from bson import ObjectId
from conections.mongo import conection_mongo

def user_publications(user_id):
    db = conection_mongo()
    collection = db["Publications"]

    publications = list(collection.find({
        "Id_user": user_id,
        "Status": {"$ne": 0}
    }))

    for pub in publications:
        pub["_id"] = str(pub["_id"])
        if "Datepublish" in pub:
            pub["Datepublish"] = str(pub["Datepublish"])

    return publications

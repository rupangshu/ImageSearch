from pymongo import MongoClient
class MongoPersist:
    def getConnection(self):
        conn = None
        try:
            conn = MongoClient()
            print("Database Connection successful")
        except:
            print("could not connect to Mongo db")
        return conn


    def insertIntoMongodb(self,data):
        conn = MongoPersist().getConnection()
        db = conn.database
        collection = db.imageCollection
        result = collection.insert(data)

        return result


    def searchMongodb(self, input):
        conn = MongoPersist().getConnection()
        db = conn.database
        collection = db.imageCollection
        cursor = collection.find({"keyword":{ '$regex': input}})
        for output in cursor:
            print(output)
        print(output)
        return output


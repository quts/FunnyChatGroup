from firebase import firebase

class firebaseWrapper(object):
    def __init__(self, url):
        self.fb     = firebase.FirebaseApplication(url, None)
        self._db    = 'default'

    def set_db(self, db):
        self._db = db

    def put_one(self, dict_data):
        if not self.has_one('/%s/%s'%(self._db,dict_data['type']), '%s'%dict_data['key']):
            return self.fb.put('/%s/%s'%(self._db,dict_data['type']), '%s'%dict_data['key'], dict_data)

    def update_one(self, dict_data):
        return self.fb.patch('/%s/%s/%s'%(self._db,dict_data['type'], dict_data['key']), dict_data)

    def delete_one(self, path, key):
        return self.fb.delete(path, key)

    def has_one(self,path,key):
        if self.fb.get('%s/%s'%(self._db, path), key):
            return True
        return False

    def get_key(self, key):
        return self.fb.get(self._db, key)


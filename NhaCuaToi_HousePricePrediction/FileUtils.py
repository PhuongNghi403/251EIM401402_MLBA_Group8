import pickle

class FileUtils:
    @staticmethod
    def savemodel(model, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(model, f)
            return True
        except Exception as e:
            print(f"Save model error: {e}")
            return False

    @staticmethod
    def loadmodel(filename):
        try:
            with open(filename, 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            print(f"Load model error: {e}")
            return None
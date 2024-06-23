from data_extractor import get_data_from_document
from deepface import DeepFace 

#Function that check if the person is already in the database and returns all documents with the same face.
def get_person_document(image):
    imgs = DeepFace.find(img_path = image, db_path = "./data/documents", enforce_detection = False, detector_backend="mtcnn")
    if imgs[0].empty:
        return []
    ids = set(imgs[0]['identity'].values.tolist())
    results = get_data_from_document(ids)
    return results
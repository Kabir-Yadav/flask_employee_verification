import pickle
from scipy.spatial.distance import cosine
from PIL import Image as PILImage
from fastai.vision.all import *

# Load the trained model and embeddings
learn = load_learner(r'models\face_recognition_model.pkl')
with open(r'models\embeddings.pkl', 'rb') as f:
    embeddings_db = pickle.load(f)

def get_embedding(img_path):
    """Get the embedding for a given image using the provided model."""
    img = PILImage.create(img_path)
    img_dl = learn.dls.test_dl([img])
    img_batch = img_dl.one_batch()
    pred = learn.model(img_batch[0])
    return pred[0].detach().numpy().flatten()

def verify_employee(img_path, employee_id):
    """Verify the employee by comparing image embeddings."""
    new_embedding = get_embedding(img_path)
    
    if employee_id not in embeddings_db:
        return False

    stored_embeddings = embeddings_db[employee_id]
    for stored_embedding in stored_embeddings:
        similarity = 1 - cosine(new_embedding, stored_embedding)
        if similarity > 0.8:
            return True
    
    return False

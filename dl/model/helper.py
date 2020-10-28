import numpy as np

from keras.utils import Sequence
from keras.preprocessing.image import load_img
from keras.utils import to_categorical


class Helper(Sequence):
    """
    Helper to iterate over the data (as Numpy arrays).
    Source: https://keras.io/examples/vision/oxford_pets_image_segmentation/
            https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly
            https://stackoverflow.com/questions/43884463/how-to-convert-rgb-image-to-one-hot-encoded-3d-array-based-on-color-using-numpy
            https://stackoverflow.com/questions/54011487/typeerror-unsupported-operand-types-for-image-and-int
    """
    def __init__(self, batch_size, img_size, input_img_paths, target_img_paths):
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def __len__(self):
        return len(self.target_img_paths) // self.batch_size

    def __getitem__(self, idx):
        """Returns tuple (input, target) correspond to batch #idx."""
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i: i + self.batch_size]
        batch_target_img_paths = self.target_img_paths[i: i + self.batch_size]

        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="float32")
        for j, path in enumerate(batch_input_img_paths):
            img = load_img(path, target_size=self.img_size)
            x[j] = np.asarray(img) / 255

        y = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")
        for j, path in enumerate(batch_target_img_paths):
            img = load_img(path, target_size=self.img_size, color_mode="grayscale")
            y[j] = np.expand_dims(img, 2)

        # y = to_categorical(y.astype('float32'))

        return x, y


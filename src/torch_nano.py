import sys, json
from torchvision import datasets, models, transforms
from PIL import Image

# This path should match the path in ../scripts/provision.sh
sys.path.insert(0, '/home/jetson/python-envs/env/lib/python3.6/site-packages/torchvision')


def run_inference(frame):
    """Test"""

    # Prepare the labels
    with open("imagenet-simple-labels.json") as f:
        labels = json.load(f)

    # First prepare the transformations: resize the image to what the model was trained on and convert it to a tensor
    data_transform = transforms.Compose([transforms.Resize((300, 300)), transforms.ToTensor()])

    # Should we normalize?
    # https://pytorch.org/docs/stable/torchvision/models.html#video-classification

    # Load the image
    image = Image.open(frame)
    # Apply the transformation, expand the batch dimension, and send the image to the GPU
    image = data_transform(image).unsqueeze(0).cuda()

    # Download the model if it's not there already. It will take a bit on the first run, after that it's fast
    mobilenet = models.mobilenet_v2(pretrained=True)
    # Send the model to the GPU
    mobilenet.cuda()
    # Set layers such as dropout and batchnorm in evaluation mode
    mobilenet.eval()

    # Get the 1000-dimensional model output
    out = mobilenet(image)
    # Find the predicted class
    res = "Predicted class is: {}".format(labels[out.argmax()])

    # TODO : Run a live image frame by frame through PyTorch. Capture the result in a variable and print on the image.
    # TODO: Draw a bounding box over the image with the predicted result.
    # TODO : Return the results in this function


if __name__ == "__main__":
    test_image = '../test/MVIMG_20171225_090953.jpg'
    run_inference(test_image)

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

    # TODO: Should we normalize?
    # https://pytorch.org/docs/stable/torchvision/models.html#video-classification

    # Load the image
    image = Image.fromarray(frame)
    # Apply the transformation, expand the batch dimension, and send the image to the GPU
    image = data_transform(image).unsqueeze(0).cuda()

    # Download the model if it's not there already. It will take a bit on the first run, fast in subsequent runs
    mobilenet = models.mobilenet_v2(pretrained=True)
    # Send the model to the GPU
    mobilenet.cuda()
    # Set layers such as dropout and batchnorm in evaluation mode
    mobilenet.eval()

    # Get the 1000-dimensional model output
    out = mobilenet(image)
    # Find the predicted class
    res = "Predicted class is: {}".format(labels[out.argmax()])
    return res

    # TODO: Draw a bounding box over the image with the predicted result.


if __name__ == "__main__":
    test_image = '../test/shark.jpg'
    res = run_inference(test_image)
    print(res)

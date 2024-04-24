# Import dependencies
import cv2
import torch
import matplotlib.pyplot as plt
import numpy as np
import os

def download_midas(small=True):
    if small:
        model = "MiDaS_small"
    else:
        model = "DPT_Large"

    midas = torch.hub.load('intel-isl/MiDaS', model)
    midas.to('cpu')
    midas.eval()

    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

    if small:
        transform = midas_transforms.small_transform
    else:
        transform = midas_transforms.dpt_transform
    
    return midas, transform


def process_image(image):
    cv2_image = cv2.imread(image)
    #Color Local Contrast Enhancement
    lab_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l_channel_enhanced = clahe.apply(l_channel)
    lab_image_enhanced = cv2.merge([l_channel_enhanced, a_channel, b_channel])
    image_enhanced = cv2.cvtColor(lab_image_enhanced, cv2.COLOR_LAB2BGR)

    #Conversion en RGB
    image_RGB = cv2.cvtColor(image_enhanced, cv2.COLOR_BGR2RGB)
    return image_RGB


def predict(img, midas, transform):
    imgbatch = transform(img).to('cpu')
    # Make a prediction
    with torch.no_grad():
        prediction = midas(imgbatch)
        prediction = torch.nn.functional.interpolate(
        prediction.unsqueeze(1),
        size = img.shape[:2],
        mode='bicubic',
        align_corners=False
    ).squeeze()

    output = prediction.cpu().numpy()
    return output

def plot(output, name_graph, surface_plot=False, save_plot=True, plot_dir='images/depth_map'):
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    if surface_plot:
        x = np.arange(output.shape[1])
        y = np.arange(output.shape[0])
        X, Y = np.meshgrid(x, y)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, output, cmap='viridis')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_axis_off()  # Supprimer les axes et les échelles dans la branche if surface_plot
    else:
        fig = plt.figure()
        plt.imshow(output)
        plt.axis('off')  # Supprimer les axes et les échelles dans la branche else

    if save_plot:
        plt.savefig(os.path.join(plot_dir, name_graph))
    else:
        plt.show()




#midas
# midas, transform = download_midas(small=False)

# #CV2
# image_path = "images/plante/photo1_first_plan.png"


# img = process_image(image_path)
# prediction = predict(img=img,midas=midas,transform=transform)

# plot(output=prediction, name_graph="test.png", surface_plot=False)
# plot(output=prediction,surface_plot=True)
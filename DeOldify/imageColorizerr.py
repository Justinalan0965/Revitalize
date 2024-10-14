from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import *



def colorize(filepath):
    device.set(device=DeviceId.GPU0)

    plt.style.use('dark_background')
    torch.backends.cudnn.benchmark=True
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")


    colorizer = get_image_colorizer(artistic=True)

    render_factor=35

    source_url= None
    source_path = filepath
    result_path = None

    if source_url is not None:
        result_path = colorizer.plot_transformed_image_from_url(url=source_url, path=source_path, render_factor=render_factor, compare=True)
    else:
        result_path = colorizer.plot_transformed_image(path=source_path, render_factor=render_factor, compare=True)



colorize("..\\GFPGAN\\results\\restored_imgs\\beardless-man.jpg")

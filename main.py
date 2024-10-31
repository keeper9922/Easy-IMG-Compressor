import time
from pathlib import Path
from tkinter.filedialog import askopenfilenames

from PIL import Image


def convert_files(files, startFileExtension: str = "jpg", finalDirectory: str = "output",
                  finalFileExtension: str = "png", compressionModifier: float = 0.8, unColor: bool = True,
                  rotateResult: bool = False) -> None:
    """
    Function to convert images to reduce their size.
    :param files: Initial files
    :param startFileExtension: Initial extension. Supported: jpg, jpeg, png, jfif, webp, raw, tiff, heif.
    :param finalDirectory: Final directory.
    :param finalFileExtension: Final extension. Supported: jpg, jpeg, png, jfif, webp, raw, tiff,
    heif.
    :param compressionModifier: How much we want to compress the image?
    :param unColor: convert to Black and White?
    :param rotateResult: Rotate?
    :return: None.
    """
    if 0 == compressionModifier > 1:
        print("This compression unavailable in current decade.")
        return
    if not Path(finalDirectory).exists():
        print("There is no final directory, creating.")
        Path(finalDirectory).mkdir(parents=True, exist_ok=True)
        print("Directory created: %s" % finalDirectory)
    available_extensions = ['png', 'jpg', 'jpeg', 'jpe', 'jfif', 'jif', 'jfi', 'webp', 'raw', 'tiff', 'bmp', 'psd',
                            'tif', 'heif']
    if startFileExtension.lower() not in available_extensions or finalFileExtension.lower() not in available_extensions:
        raise ValueError("Unsupported extension: %s" % available_extensions)
    # try:
    #     start_path = Path(startDirectory).glob(f'*{startFileExtension.lower()}')
    # except Exception as e:
    #     print("Error occurred while operating:\n", e)
    #     input()
    #     exit(77)
    k = 0
    for path in files:
        print(f"> {path}")
        # image = str(path).split("\\")[1]
        image_file = Image.open(path)  # open colour image
        iw, ih = image_file.width, image_file.height
        ifw, ifh = round(iw * compressionModifier), round(ih * compressionModifier)
        # print(iw, ih, ifw, ifh)

        image_file = image_file.resize((ifw, ifh))
        image_file = image_file.resize((iw, ih))
        if unColor:
            image_file = image_file.convert('1')  # convert image to black and white
            # print("> converted to black and white")
        if rotateResult:
            image_file = image_file.rotate(-90, expand=True)
            print("> rotated")
        try:
            # image_file.show()
            image_file.save(f'{finalDirectory}/{k}_{time.time()}.{finalFileExtension.lower()}')
            print(f"Successfully saved {k}_{time.time()} - {path} in .{finalFileExtension.lower()} format.")
        except Exception as e:
            print(f"Error saving file {k}_{time.time()} - {path} in {finalFileExtension.lower()} "
                  f"format. Error message:\n", e)
        k += 1


choose_wisely = {
    "Y": 1,
    "N": 0,
}
clr = input("Should we turn image into black and white? Y/N: ")
cmp = int(input("How much we want to compress our images in %? (recommended 85)\n: "))
print("Choose files.")
convert_files(files=askopenfilenames(),
              unColor=choose_wisely[clr],
              compressionModifier=cmp / 100)

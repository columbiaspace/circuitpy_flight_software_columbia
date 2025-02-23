import board
import sdioio
import storage
import camera


class Sp_Camera():
        def __init__(self):
                # Initialize SD card storage
                self.sd = sdioio.SDCard(
                    clock=board.SDIO_CLOCK,
                    command=board.SDIO_COMMAND,
                    data=board.SDIO_DATA,
                    frequency=25000000)
                self.vfs = storage.VfsFat(sd)
                storage.mount(vfs, '/sd')

                # Set up camera, assign picture attributes, and take picture 
                # Write picture data to file `buffer`.
                self.cam = camera.Camera()

                #Counter for images
                self.counter = 0

        def take_picture(self, file_name="image_") -> None:
            buffer = bytearray(512 * 1024)
            path = "/sd/" + file_name + ".jpg"
            file = open(path,"wb")
            size = self.cam.take_picture(buffer, width=1920, height=1080, format=camera.ImageFormat.JPG)
            file.write(buffer, size)
            file.close()
            
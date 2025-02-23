import board
import sdioio
import storage
import camera
import os


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

        #Deletes a picture and if it can't it returns -1
        def delete_picture (self, file_name = "") -> int:
               #File can't be deleted because it wasn't passed in
            if file_name == "":
                    return -1
               
            file_path = "/sd/" + file_name
            if os.path.exists(file_path):
                os.remove(file_path)   
                return 1
            else: 
                  return -1
            

        
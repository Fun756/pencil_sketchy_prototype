# pencil_sketchy_prototype
The old prototype of my university project that generate the sketch image based on the photo using Image Processing written in Python.
The performance is not very effective and may experience bugs in the prototype.


# Software and Library Requirements
- Python version 3.0 or newer
- numpy Python library.
- cv2 Python library.

# Instruction
Run project2_en.py to run the english version of this prototype.


![image](https://user-images.githubusercontent.com/86656188/174429309-c71e14d9-40dc-4707-8dae-4185dd009739.png)


There're 6 major functions in the prototype once you run it.

  1.  Upload Your Photo Here!
      -   A field to browse a photo in your local disc.

  2.  Denoising Value
      -   Reduces noise in the photo. Higher the value stonger noise reduces.(Default: 5)

  3.  Histogram Clipping
      -   The percent threshold to Remove some edge of the photo's histogram that's too dark and too bright then apply auto brightness function.
          the value (Default: 1)

  4.  Sobel Size
      -   Mask size for the Sobel Filter. (Default: 3)

  5.  Gaussian Size
      -   Mask size for the gaussian blur function. (Default: 15)

  6.  CV Pencil Sketch
      -   Apply the additional algorithm for enhancing a photo's details. (Default: Disabled) 



After the major functions are set, clicking "Sketch!" will generate the sketch image based on a photo you browsed and values of major functions along with the original photo for comparsion. The generated image file is located at the same directory of the prototype.

While the output is shown you can't interact with the major functions until you close both original photo tab and generated image tab.

To close the prototype, just close the major function tab.

# Sample
![example2](https://user-images.githubusercontent.com/86656188/174429285-aac33c4a-75bf-4654-bb5d-35af38e7786f.jpg)
![output](https://user-images.githubusercontent.com/86656188/174429289-3c9dc041-e4db-4486-8009-603edbc8e46d.jpg)
